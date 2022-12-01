import json
import math
from typing import Literal

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
today_str = "2022-11-28"

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
) -> float:
    all_card_scores = card["player"]["latestFinalFixtureStats"]
    last_game: PlayerInFixtureStatusIconType = all_card_scores[2]["status"][
        "statusIconType"
    ]
    card_average: int = card["player"]["tenGameAverage"]
    team: str = card["team"]["fullName"]
    if player_name in game_decision_players and (
        last_game == "NO_GAME" or last_game == "DID_NOT_PLAY"
    ):  # 如果在game_decision，但上一比赛没上的，就不要上了
        return 0
    next_matches: int = len(
        list(filter(lambda m: m["away"] == team or m["home"] == team, matches))
    )  # 下一周的比赛场数
    if next_matches == 0 or player_name in out_players:  # 去掉下周没有比赛的球员和确定受伤不打的球员
        return 0
    total_bonus: float = card["totalBonus"]
    all_card_scores: list[NBAPlayerInFixture] = card["player"][
        "latestFinalFixtureStats"
    ]
    card_scores: list[NBAPlayerInFixture] = list(
        filter(
            lambda g: g["status"]["statusIconType"] != "NO_GAME",
            all_card_scores[2 : 2 + compute_by_recent_n_weeks_games],  # 取最近7周比赛
        )
    )
    stats_arr: list[float] = list(
        map(
            lambda s: divide(s["score"] - s["tenGameAverage"], s["tenGameAverage"]),
            card_scores,
        )
    )  # 计算每场比赛的表现变化率，应该0上下浮动
    clean_stats_arr: list[float] = exclude_best_and_worst(stats_arr)
    if len(clean_stats_arr) == 0:  # 如果没有比赛数据，直接返回0
        return 0
    ewma_: list[float] = ewma(clean_stats_arr, 0.5)  # 用ewma平滑结果，系数可以调整，该数值越小，历史数据的影响越小
    mu: float = np.mean(ewma_).__float__()
    sigma: float = np.std(ewma_, ddof=1).__float__()
    if math.isnan(sigma):  # 如果标准差为0，直接返回0
        return 0
    if player_name in game_decision_players:
        mu += mu_of_game_decision

    match_join: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )
    k_list: list[float] = []
    bonus: float = 0
    # 1. 获取对手攻防实力，按标准化加成
    if len(match_join) == 0:
        return 0
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
    return future_performance.mean


if __name__ == "__main__":
    all_stats_dist_list: list[SelectCard] = []

    for card in avaliable_cards:
        player_name: str = card["player"]["displayName"]
        # ------------check single player--------------
        # if (
        #     player_name != "Bones Hyland"
        # ):  # TODO 类似Paul Reed这种连续爆发后，平均分已经上来了，预期表现会被计算过高，同理MVP球员 Giannis Antetokounmpo 的分数会被估计低，需要修改算法。Bryce McGowens这种突然爆发的列入研究。球员算法也提取成函数。Marcus Morris Sr.没打？
        #     continue

        future_performance: float = predict(card)

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
    df["outperform"] = (df["expect"] - df["average"]).astype(int)
    print(df.sort_values(by="outperform", ascending=False).to_string())

    # user input Y to continue
    input(
        "Press any key to continue (You can press Ctrl+C to stop program and set suggest or blacklist card in config): "
    )

    result_lines = []
    used_cards = []

    for tournaments in all_tournaments:
        # TODO: check suggest_player is valid

        select_cards: list[SelectCard] = []
        stats_dist_list: list[SelectCard] = all_stats_dist_list.copy()
        high_rarity_count: int = 0

        allowed_rarities: list[CardRarity] = [
            t.value for t in tournaments["allowedRarities"]
        ]
        allow_mvp: bool = tournaments["allowMVP"]
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

        avaliable_cards_with_condition: list[SelectCard] = list(
            filter(
                lambda c: c["rarity"] in allowed_rarities
                and c not in used_cards
                and c["id"] not in blacklist_players[tournaments["name"]],
                stats_dist_list,
            )
        )

        tmp_best_card: SelectCard | None = None  # type: ignore
        if allow_mvp:  # 选择mvp
            best_card: SelectCard = max(
                avaliable_cards_with_condition,
                key=lambda c: c["expect"] and c["average"] >= mvp_threshold,
            )
            if best_card["rarity"] == min_rarity and min_rarity != None:  # TODO check mvp is work
                high_rarity_count += 1
            select_cards.append(best_card)
            used_cards.append(best_card)
            tmp_best_card: SelectCard = best_card

        # exclude used cards
        card_pool: list[SelectCard] = list(
            filter(lambda c: c not in used_cards, avaliable_cards_with_condition)
        )
        to_select_card_count: Literal[4, 5] = 4 if tournaments["allowMVP"] else 5
        possible_group: list[tuple[SelectCard]] = []
        for possible in combinations(card_pool, to_select_card_count):
            # check total points
            total_point: int = sum([card["average"] for card in possible])
            if total_point > tournaments["tenGameAverageTotalLimit"]:
                continue

            # check card rarity min count
            rarities_count: int = (
                5
                if is_common
                else len(
                    list(
                        filter(
                            lambda card: card["rarity"] == min_rarity.value, possible  # type: ignore
                        )
                    )
                )
            )
            if rarities_count + high_rarity_count < min_count:
                continue

            # check player duplicate
            players: list[str] = []
            other_players: list[str] = list(map(lambda card: card["name"], possible))
            players = (
                [tmp_best_card["name"]] + other_players
                if tmp_best_card != None
                else other_players
            )
            unique_players: int = len(set(players))
            if unique_players != len(players):
                continue

            possible_group.append(possible)

        if len(possible_group) == 0:
            result_lines.append(f"{tournaments['name']} no possible lineup")
            continue

        sorted_possible_group = sorted(
            possible_group,
            key=lambda p: sum([card["expect"] for card in p]),
            reverse=True,
        )

        group_to_select = []

        if len(possible_group) > suggestion_count:
            group_to_select = sorted_possible_group[:suggestion_count]
        else:
            group_to_select = sorted_possible_group

        print(f"Selecting {tournaments['name']}")
        for index, group in enumerate(group_to_select):
            print(f"Group: {index}, total: {sum([card['average'] for card in group])}")
            for card in group:
                print(
                    f"{card['name']}({card['rarity']},{card['average']}) {show_opposite_team(card['team'])}"
                ) 
            print("\n")

        group_index = -1
        while True:
            group_index = input("Please select group (input Group number): ")
            if group_index.isdigit() and int(group_index) < len(group_to_select):
                break
            else:
                print("Invalid group index")

        for card in group_to_select[int(group_index)]:
            select_cards.append(card)
            used_cards.append(card)

        if len(select_cards) == 5:
            result_lines.append(f"{tournaments['name']}")
            expect_sum = 0
            for card in select_cards:
                result_lines.append(
                    f"{card['name']}({card['rarity']},{card['average']})"
                )
                expect_sum += card["expect"]
            result_lines.append(f"expect: {expect_sum:.2f}")
        else:
            result_lines.append(f"{tournaments['name']} no possible lineup")

        result_lines.append("\n")

    # write result lines to file
    with open(f"data/result-{today_str}.txt", "w") as f:
        f.writelines(result_lines + "\n" for result_lines in result_lines)
        print("compute done, save in data/result.txt")
