import json
import math

import numpy as np
from pandas import DataFrame
from statistics import NormalDist
from datetime import datetime
from itertools import combinations
from types_ import *

from pytz import timezone
from utils import ewma, divide, exclude_best_and_worst
from config.config import *
import warnings

warnings.filterwarnings("ignore")


today: datetime = datetime.now(timezone("US/Eastern"))
today_str: str = today.strftime("%Y-%m-%d")

with open(f"data/cards-{today_str}.json", "r") as f:
    cards: list[NBACard] = json.load(f)

with open(f"data/injure-{today_str}.json", "r") as g:
    injure: list[Injure] = json.load(g)

with open(f"data/next-week-{today_str}.json", "r") as h:
    matches: list[Match] = json.load(h)

with open(f"data/team-rank-{today_str}.json", "r") as i:
    team_rank: TeamRank = json.load(i)

common_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "common", cards))
limited_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "limited", cards))
rare_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "rare", cards))
super_rare_cards: list[NBACard] = list(
    filter(lambda c: c["rarity"] == "super_rare", cards)
)

print(
    f"Load {len(common_cards)} common, {len(limited_cards)} limited, {len(rare_cards)} rare, {len(super_rare_cards)} super rare cards."
)

out_players: list[str] = list(
    map(lambda j: j["player"], filter(lambda i: not i["game_time_decision"], injure))
)
game_decision_players: list[str] = list(
    map(lambda j: j["player"], filter(lambda i: i["game_time_decision"], injure))
)
avaliable_cards: list[NBACard] = list(
    filter(
        lambda t: t["player"]["displayName"] not in out_players,
        cards,
    )
)


def show_opposite_team(team: str) -> str:
    matches_join: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )
    info = ""
    if len(matches_join) == 0:
        info = "No match"
        return info
    match_info = []
    for match in matches_join:
        at_home = match["home"] == team
        off_team = match["away"] if at_home else match["home"]
        is_away_b2b = match["away"] == team and match["away_is_b2b"]
        is_home_b2b = match["home"] == team and match["home_is_b2b"]
        match_info.append(
            f"{'back to back ' if is_away_b2b or is_home_b2b else ''}vs {off_team} on {match['date']} {'at home' if at_home else 'at away'}"
        )
    info = " and ".join(match_info)
    return info


def predict(
    card: NBACard,
    game_decision_players: list[str] = game_decision_players,
    out_players: list[str] = out_players,
    matches: list[Match] = matches,
    team_rank: TeamRank = team_rank,
) -> NormalDist:
    all_card_scores: list[NBAPlayerInFixture] = card["player"][
        "latestFinalFixtureStats"
    ]
    # get first not pending index
    last_game_index: int = next(
        (
            i
            for i, v in enumerate(all_card_scores)
            if v["status"]["statusIconType"]
            != PlayerInFixtureStatusIconType.pending.value
        )
    )
    last_game: str = all_card_scores[last_game_index]["status"]["statusIconType"]
    card_average: int = card["player"]["tenGameAverage"]
    team: str = card["team"]["fullName"]
    if player_name in game_decision_players and (
        last_game == PlayerInFixtureStatusIconType.no_game.value
        or last_game == PlayerInFixtureStatusIconType.did_not_play.value
    ):  # 如果在game_decision，但上一比赛没上的，就不要上了
        return NormalDist(0, 0)
    next_matches: int = len(
        list(filter(lambda m: m["away"] == team or m["home"] == team, matches))
    )  # 下一周的比赛场数
    if next_matches == 0 or player_name in out_players:  # 去掉下周没有比赛的球员和确定受伤不打的球员
        return NormalDist(0, 0)
    total_bonus: float = card["totalBonus"]
    card_scores: list[NBAPlayerInFixture] = list(
        filter(
            lambda g: g["status"]["statusIconType"] != "NO_GAME",
            all_card_scores[
                last_game_index : last_game_index + compute_by_recent_n_weeks_games
            ],  # 取最近7周比赛
        )
    )
    stats_arr: list[float] = list(
        map(
            lambda s: divide(
                s["score"] - s["tenGameAverage"],
                all_card_scores[last_game_index]["tenGameAverage"],
            ),
            card_scores,
        )
    )  # 计算每场比赛的表现变化率，应该0上下浮动
    clean_stats_arr: list[float] = exclude_best_and_worst(stats_arr)
    if len(clean_stats_arr) == 0:  # 如果没有比赛数据，直接返回0
        return NormalDist(0, 0)
    ewma_: list[float] = ewma(clean_stats_arr, 0.5)  # 用ewma平滑结果，系数可以调整，该数值越小，历史数据的影响越小
    mu: float = np.mean(ewma_).__float__()
    sigma: float = np.std(ewma_, ddof=1).__float__()
    if math.isnan(sigma):  # 如果标准差为0，直接返回0
        return NormalDist(0, 0)
    if player_name in game_decision_players:
        mu += mu_of_game_decision

    match_join: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )
    k_list: list[float] = []
    bonus: float = 0
    # 1. 获取对手攻防实力，按标准化加成
    # TODO 改为按位置分类，如果是打攻击弱的C、F加成，打防守弱的F、G加成；反之亦然
    if len(match_join) == 0:
        return NormalDist(0, 0)
    for match in match_join:
        opponent: str = match["away"] if match["home"] == team else match["home"]
        offense_rank: int = team_rank["team_offense_rank"].index(opponent)
        defense_rank: int = team_rank["team_defense_rank"].index(opponent)
        k: float = (
            (offense_rank - 15) / 30 + (defense_rank - 15) / 30
        ) * mu_of_max_rank_team_bonus_ratio
        k_list.append(k)
    opponent_bonus: float = sum(k_list) / len(k_list) if len(k_list) != 0.0 else 0.0
    # 2. 主客场加成
    home_bonus: float = 0
    for match in match_join:
        if match["home"] == team:
            home_bonus += mu_of_home_bonus
    # 3. 背靠背
    b2b_bonus: float = 0
    for match in match_join:
        if (
            match["away"] == team and match["away_is_b2b"] and not match["home_is_b2b"]
        ):  # 客场背靠背且对手不是背靠背
            b2b_bonus -= mu_of_away_b2b
        if match["home"] == team and match["home_is_b2b"] and not match["away_is_b2b"]:
            b2b_bonus -= mu_of_home_b2b
    # 4. 比赛场数
    match_count_bonus: float = 0
    if len(match_join) == 1:
        match_count_bonus += mu_of_single_game_bonus
    if len(match_join) > 2:
        match_count_bonus += mu_of_multiple_games_bonus
    bonus = opponent_bonus + home_bonus + b2b_bonus + match_count_bonus
    mu += bonus

    future_performance: NormalDist = (
        NormalDist(mu, sigma) * card_average + card_average
    ) * (1 + total_bonus)
    return future_performance


if __name__ == "__main__":
    all_stats_dist_list: list[SelectCard] = []

    for card in avaliable_cards:
        player_name: str = card["player"]["displayName"]
        # ------------check single player--------------
        # if player_name != "Bryce McGowens":
        #     continue

        future_performance: NormalDist = predict(card)

        card_dist: SelectCard = {
            "name": player_name,
            "average": card["player"]["tenGameAverage"],
            "rarity": card["rarity"],
            "expect": future_performance,
            "team": card["team"]["fullName"],
            "id": card["id"],
        }
        all_stats_dist_list.append(card_dist)

    # convert all_stats_dist_list to dataframe
    df: DataFrame = DataFrame(all_stats_dist_list)
    df["mean"] = df["expect"].apply(lambda x: x.mean)
    print(df.sort_values(by="mean", ascending=False).to_string())

    # user input Y to continue
    input(
        "Press any key to continue (You can press Ctrl+C to stop program and set suggest or blacklist card in config): "
    )

    result_lines = []
    used_cards = []

    for tournaments in all_tournaments:
        # TODO: check suggest_player is valid
        if tournaments["name"] in suggest_players:
            suggest_players_id: list[str] = suggest_players[tournaments["name"]]
            pre_select: int = len(suggest_players_id)
        else:
            pre_select = 0

        stats_dist_list: list[SelectCard] = all_stats_dist_list.copy()

        pre_select_cards: list[SelectCard] = (
            list(filter(lambda c: c["id"] in suggest_players_id, stats_dist_list))
            if pre_select != 0
            else []
        )

        allowed_rarities: list[str] = [t.value for t in tournaments["allowedRarities"]]
        allow_mvp: bool = tournaments["allowMVP"]
        target: int = tournaments["target"]
        allowed_conference: NBAConference | None = tournaments["allowedConference"]
        is_common: bool = tournaments["minRarity"] is None
        min_rarity: CardRarity | None = (
            None if is_common else tournaments["minRarity"]["rarity"]  # type: ignore
        )
        min_count: int = (
            5 if is_common else tournaments["minRarity"]["minCount"]  # type: ignore
        )

        if allowed_conference != None:
            if allowed_conference == "WESTERN":
                stats_dist_list = list(
                    filter(
                        lambda c: c["team"] in western_teams,
                        all_stats_dist_list,
                    )
                )
            else:
                stats_dist_list = list(
                    filter(
                        lambda c: c["team"] not in western_teams,
                        all_stats_dist_list,
                    )
                )

        card_pool: list[SelectCard] = list(
            filter(
                lambda c: c["rarity"] in allowed_rarities
                and c not in used_cards
                and c["id"] not in blacklist_players[tournaments["name"]]
                and c not in pre_select_cards,
                stats_dist_list,
            )
        )

        to_select_card_count: int = 5 - pre_select
        possible_group: list[list[SelectCard]] = []
        for possible in combinations(card_pool, to_select_card_count):
            all_5_cards: list[SelectCard] = list(possible) + pre_select_cards

            # check total points
            total_point: int = (
                sum([card["average"] for card in all_5_cards])
                if not allow_mvp
                else sum(
                    [
                        card["average"]
                        for card in sorted(
                            all_5_cards, key=lambda c: c["average"], reverse=True
                        )[1:]
                    ]
                )
            )
            if total_point > tournaments["tenGameAverageTotalLimit"]:
                continue

            # check card rarity min count
            rarities_count: int = (
                5
                if is_common
                else len(
                    list(
                        filter(
                            lambda card: card["rarity"] == min_rarity.value,  # type: ignore
                            all_5_cards,
                        )
                    )
                )
            )
            if rarities_count < min_count:
                continue

            # check player duplicate
            players: list[str] = list(map(lambda card: card["name"], all_5_cards))
            unique_players: int = len(set(players))
            if unique_players != len(players):
                continue

            possible_group.append(all_5_cards)

        if len(possible_group) == 0:
            result_lines.append(f"{tournaments['name']} no possible lineup")
            continue

        group_index_to_cdf: dict[int, float] = {}

        for index, group in enumerate(possible_group):
            total_dist: NormalDist = NormalDist(0, 0)
            for card in group:
                total_dist += card["expect"]
            p_of_reach_target = total_dist.cdf(target)
            if p_of_reach_target < 0.99:
                group_index_to_cdf[index] = p_of_reach_target

        group_to_select: list[list[SelectCard]] = []
        sorted_possible_group: list[tuple[int, float]] = sorted(
            group_index_to_cdf.items(), key=lambda item: item[1]
        )
        if len(sorted_possible_group) > suggestion_count:
            group_to_select = list(
                map(
                    lambda item: possible_group[item[0]],
                    sorted_possible_group[:suggestion_count],
                )
            )
        else:
            group_to_select = list(
                map(lambda item: possible_group[item[0]], sorted_possible_group)
            )
        print(f"\n")
        print(f"Selecting {tournaments['name']}")
        for index, group in enumerate(group_to_select):
            print(f"Group: {index}, total: {sum([card['average'] for card in group])}")
            for select_card in group:
                print(
                    f"{select_card['name']}({select_card['rarity']},{select_card['average']}) {show_opposite_team(select_card['team'])}"
                )
            print("\n")

        group_index: str = "-1"
        while True:
            group_index = input("Please select group (input Group number): ")
            if group_index.isdigit() and int(group_index) < len(group_to_select):
                break
            else:
                print("Invalid group index")

        select_cards: list[SelectCard] = []
        for select_card in group_to_select[int(group_index)]:
            select_cards.append(select_card)
            used_cards.append(select_card)

        if len(select_cards) == 5:
            result_lines.append(f"{tournaments['name']}")
            expect_sum: float = 0.0
            for select_card in select_cards:
                result_lines.append(
                    f"{select_card['name']}({select_card['rarity']},{select_card['average']})"
                )
                expect_sum += select_card["expect"].mean
            for select_card in select_cards:
                result_lines.append(f'"{select_card["id"]}"')
            result_lines.append(f"expect: {expect_sum:.2f}")
        else:
            result_lines.append(f"{tournaments['name']} no possible lineup")

        result_lines.append("\n")

    # write result lines to file
    with open(f"data/result-{today_str}.txt", "w") as f:
        f.writelines(result_lines + "\n" for result_lines in result_lines)
        print("compute done, save in data/result.txt")
