import json
from pandas import DataFrame
from numpy import array
from statistics import NormalDist
from datetime import datetime
from itertools import combinations
from types_ import *
from scipy.stats import t
from pytz import timezone
from utils import ewma
from config.config import *
import warnings
import argparse

warnings.filterwarnings("ignore")


def show_opposite_team(team: str, matches: list[Match]) -> str:
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
            f"{'B2B ' if is_away_b2b or is_home_b2b else ''}vs {off_team} on {match['date']} {'at HOME' if at_home else 'at AWAY'}"
        )
    info = " and ".join(match_info)
    return info


def player_is_main(player: str, team: str | None) -> tuple[bool, list[str]]:
    if team is None:
        return False, []
    with open("./data/player_positions.json", "r") as f:
        team_to_position: dict = json.load(f)
        players: dict[str, str | list[str]] = team_to_position[team]
        starters: list[str] = list(map(lambda l: l[0], list(players.values())))
        seconds: list[str] = list(map(lambda l: l[1], list(players.values())))
        thirds: list[str] = list(map(lambda l: l[2], list(players.values())))
        next_choose: list[str] = []
        if player in starters:
            index = starters.index(player)
            next_choose.append(seconds[index])
            for third in thirds[index]:
                next_choose.append(third)
            return True, next_choose
        elif player in seconds:
            index = seconds.index(player)
            for third in thirds[index]:
                next_choose.append(third)
            return True, next_choose
        else:
            return False, next_choose


def get_score_with_ratio(
    stats: list[DetailedStats],
    stats_ratio: dict[str, float],
) -> float:
    if stats == []:
        return 0
    default_ratio: dict[str, float] = {
        "points": 1,
        "rebounds": 1,
        "assists": 1,
        "blocks": 1,
        "steals": 1,
        "turnovers": 1,
        "made3PointFGs": 1,
        "doubleDoubles": 1,
        "tripleDoubles": 1,
    }
    default_ratio.update(stats_ratio)
    stat_per_game = []
    for stat in stats:
        detail: DetailedStat = stat["detailedStats"]
        total_point: float = sum(
            [
                detail["points"] * default_ratio["points"] * 1,
                detail["rebounds"] * default_ratio["rebounds"] * 1.2,
                detail["assists"] * default_ratio["assists"] * 1.5,
                detail["blocks"] * default_ratio["blocks"] * 3,
                detail["steals"] * default_ratio["steals"] * 3,
                detail["turnovers"] * default_ratio["turnovers"] * (-2),
                detail["made3PointFGs"] * default_ratio["made3PointFGs"] * 1,
                detail["doubleDoubles"] * default_ratio["doubleDoubles"] * 1,
                detail["tripleDoubles"] * default_ratio["tripleDoubles"] * 1,
            ]
        )
        stat_per_game.append(total_point)
    return max(stat_per_game)


def predict(
    player: NBAPlayer,
    game_decision_players: list[str],
    out_players: list[str],
    matches: list[Match],
    team_rank: TeamRank,
    stats_ratio: dict[str, float],
) -> NormalDist:
    has_ratio = stats_ratio != {}
    is_main, next_chooses = player_is_main(
        player["displayName"],
        player["team"]["abbreviation"] if player["team"] is not None else None,
    )
    # next_chooses exclude players who are not main
    next_chooses = list(
        filter(
            lambda n: n not in out_players and n not in game_decision_players,
            next_chooses,
        )
    )

    all_card_scores: list[NBAPlayerInFixture] = player["latestFinalFixtureStats"]
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

    player_name: str = player["displayName"]
    if (
        player_name in out_players
        and (
            last_game != PlayerInFixtureStatusIconType.no_game.value
            and last_game != PlayerInFixtureStatusIconType.did_not_play.value
        )
        and not has_ratio
        and show_injure_detail
    ):  # 新受伤的球员
        print(
            f"『{player_name}』is out for the next game"
            + f", reserve players are 2️⃣『{'』,『'.join(next_chooses)}』"
            if is_main
            else ""
        )

    card_average: int = player["tenGameAverage"]
    team: str | None = None if player["team"] is None else player["team"]["fullName"]
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
    stats_arr: list[float] = list(
        map(
            lambda s: s["score"]
            if len(stats_ratio) == 0
            else get_score_with_ratio(
                s["status"]["gameStats"], stats_ratio=stats_ratio
            ),
            all_card_scores[
                last_game_index : last_game_index + compute_by_recent_n_weeks_games
            ],  # 取最近n周比赛
        )
    )  # 计算每场比赛的表现变化率，应该0上下浮动

    if is_main:  # 主力球员不打可能是伤病管理，不影响评分，所以过滤掉0
        stats_arr = list(filter(lambda s: s != 0, stats_arr))

    if (
        len(stats_arr) == 0 or (array(stats_arr) == 0).all()
    ):  # 对于万年不打的饮水机球员，没有比赛数据，直接返回0
        return NormalDist(0, 0)

    ewma_: list[float] = ewma(stats_arr, 0.2)  # 用ewma平滑结果，系数可以调整，该数值越小，历史数据的影响越小
    _, mu, sigma = t.fit(
        ewma_, fdf=len(ewma_)
    )  # 用t分布拟合数据，得到均值和标准差。对于不怎么打的球员，用norm有可能sigma为0

    game_decision_bonus: float = 0

    if player_name in game_decision_players:
        second_str = (
            f", reserve players are 2️⃣『{'』,『'.join(next_chooses)}』"
            if is_main and len(next_chooses) != 0
            else ""
        )
        if not has_ratio and show_injure_detail:
            print(
                f"『{player_name}』may not play in the next game, he has {next_matches} matches in next week"
                + second_str
            )
        game_decision_bonus = mu_of_game_decision

    match_join: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )

    # 1. 获取对手攻防实力，按标准化加成
    positions = player["positions"]
    k_list: list[float] = []
    bonus: float = 0
    for match in match_join:
        opponent: str = match["away"] if match["home"] == team else match["home"]
        offense_rank: int = team_rank["team_offense_rank"].index(opponent)
        defense_rank: int = team_rank["team_defense_rank"].index(opponent)
        k_o: float = 0.0
        k_d: float = 0.0
        # offense bonus
        if "NBA_FORWARD" in positions or "NBA_CENTER" in positions:
            k_o = (offense_rank - 15) / 30 * mu_of_max_rank_team_bonus_ratio
        # defense bonus
        if "NBA_FORWARD" in positions or "NBA_GUARD" in positions:
            k_d = (defense_rank - 15) / 30 * mu_of_max_rank_team_bonus_ratio
        k: float = k_o + k_d
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

    bonus = (
        game_decision_bonus
        + opponent_bonus
        + home_bonus
        + b2b_bonus
        + match_count_bonus
    )
    mu += bonus * card_average

    future_performance: NormalDist = NormalDist(mu, sigma)
    return future_performance


def get_all_card_dist(stats_ratio: dict[str, float] = {}) -> list[SelectCard]:
    all_stats_dist_list = []
    # ------------predict--------------
    if is_recommend:
        for player in avaliable_players:
            player_name: str = player["displayName"]

            future_performance: NormalDist = predict(
                player,
                game_decision_players,
                out_players,
                matches,
                team_rank,
                stats_ratio,
            )

            card_dist: SelectCard = {
                "name": player_name,
                "average": player["tenGameAverage"],
                "age": player["age"],
                "rarity": None,
                "expect": future_performance,
                "team": player["team"]["fullName"],
                "id": None,
            }
            all_stats_dist_list.append(card_dist)
    else:
        for card in avaliable_cards:
            player_name: str = card["player"]["displayName"]
            # ------------check single player for holding cards--------------
            # if player_name != "Josh Richardson":
            #     continue

            future_performance: NormalDist = predict(
                card["player"],
                game_decision_players,
                out_players,
                matches,
                team_rank,
                stats_ratio,
            ) * (1 + card["totalBonus"])

            card_dist: SelectCard = {
                "name": player_name,
                "average": card["player"]["tenGameAverage"],
                "age": card["player"]["age"],
                "rarity": card["rarity"],
                "expect": future_performance,
                "team": None
                if card["player"]["team"] is None
                else card["player"]["team"]["fullName"],
                "id": card["id"],
            }
            all_stats_dist_list.append(card_dist)
    return all_stats_dist_list


if __name__ == "__main__":
    p = argparse.ArgumentParser()

    p.add_argument("-r", "--recommend", required=False)
    args = p.parse_args()

    is_recommend = False

    if args.recommend:
        is_recommend = True

    today: datetime = datetime.now(timezone("US/Eastern"))
    today_str: str = today.strftime("%Y-%m-%d")
    # today_str = "2023-01-05"

    with open(f"data/cards-{today_str}.json", "r") as f:
        cards: list[NBACard] = json.load(f)

    with open(f"data/injure-{today_str}.json", "r") as g:
        injure: list[Injure] = json.load(g)

    with open(f"data/next-week-{today_str}.json", "r") as h:
        matches: list[Match] = json.load(h)

    with open(f"data/team-rank-{today_str}.json", "r") as i:
        team_rank: TeamRank = json.load(i)

    common_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "common", cards))
    limited_cards: list[NBACard] = list(
        filter(lambda c: c["rarity"] == "limited", cards)
    )
    rare_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "rare", cards))
    super_rare_cards: list[NBACard] = list(
        filter(lambda c: c["rarity"] == "super_rare", cards)
    )

    print(
        f"\nLoad {len(common_cards)} common, {len(limited_cards)} limited, {len(rare_cards)} rare, {len(super_rare_cards)} super rare cards."
    )
    print()

    out_players: list[str] = list(
        map(
            lambda j: j["player"], filter(lambda i: not i["game_time_decision"], injure)
        )
    )
    game_decision_players: list[str] = list(
        map(lambda j: j["player"], filter(lambda i: i["game_time_decision"], injure))
    )
    avaliable_cards: list[NBACard] = list(
        filter(
            lambda t: t["id"] not in blacklist_cards,
            cards,
        )
    )

    avaliable_players = []
    if is_recommend:
        with open(f"data/all-players-data-{today_str}.json", "r") as f:
            players: list[NBAPlayer] = json.load(f)

        avaliable_players: list[NBAPlayer] = list(
            filter(
                lambda t: t["displayName"] not in blacklist_players,
                players,
            )
        )

        if len(recommend_from_teams) != 0:
            for team in recommend_from_teams:
                assert team in source_team_names.keys(), f"{team} not valid team name"

            avaliable_players: list[NBAPlayer] = list(
                filter(
                    lambda t: t["team"]["abbreviation"] in recommend_from_teams,
                    avaliable_players,
                )
            )

    all_stats_dist_list: list[SelectCard] = []

    # TODO: check configs (for example: suggest_player) is valid
    if len(all_tournaments) == 0:
        print(
            'No tournaments found, please check "all_tournaments" in config/config.py'
        )
        exit(1)

    all_stats_dist_list = get_all_card_dist()

    # convert all_stats_dist_list to dataframe
    df: DataFrame = DataFrame(all_stats_dist_list)
    df["mean"] = df["expect"].apply(lambda x: x.mean)
    df_show: DataFrame = df.sort_values(by="mean", ascending=False)
    print("\nAll players stats:")
    df_show = df_show.drop(columns=["id", "mean"])
    print(df_show.to_string(index=True))

    # user input Y to continue
    input(
        "Press any key to continue (You can press Ctrl+C to stop program and set suggest or blacklist card in config): "
    )

    result_lines = []
    used_cards = []

    for tournaments in all_tournaments:
        group_to_select: list[list[SelectCard]] = []
        if tournaments["name"] in suggest_cards:
            suggest_players_id_to_name: dict[str, str] = suggest_cards[
                tournaments["name"]
            ]
            pre_select: int = len(suggest_players_id_to_name)
        else:
            pre_select = 0

        if "multiplier" not in tournaments:
            stats_dist_list: list[SelectCard] = all_stats_dist_list.copy()
        else:
            stats_dist_list: list[SelectCard] = get_all_card_dist(
                tournaments["multiplier"]
            )

        if is_recommend:
            pre_select_cards: list[SelectCard] = (
                list(
                    filter(
                        lambda c: c["name"] in suggest_players_id_to_name.values(),
                        stats_dist_list,
                    )
                )
                if pre_select != 0
                else []
            )
        else:
            pre_select_cards: list[SelectCard] = (
                list(
                    filter(
                        lambda c: c["id"] in suggest_players_id_to_name.keys(),
                        stats_dist_list,
                    )
                )
                if pre_select != 0
                else []
            )

        if is_recommend:
            assert (
                len(pre_select_cards) >= 2
            ), f"You need set at least 2 cards for {tournaments['name']} because compute limit"

        allowed_rarities: list[str] = [t.value for t in tournaments["allowedRarities"]]
        allow_mvp: bool = tournaments["allowMVP"]
        target: int = tournaments["target"]
        allowed_conference: NBAConference | None = tournaments["allowedConference"]
        is_common: bool = tournaments["minRarity"] is None
        min_rarity: CardRarity | None = (
            None if is_common else tournaments["minRarity"]["rarity"]  # type: ignore
        )
        divisor = 1
        match min_rarity:
            case CardRarity.limited:
                divisor = 1.05
            case CardRarity.rare:
                divisor = 1.15
            case CardRarity.super_rare:
                divisor = 1.25
            case _:
                divisor = 1

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

        if "veterans" in tournaments["name"]:
            stats_dist_list = list(
                filter(
                    lambda c: c["age"] >= 30,
                    stats_dist_list,
                )
            )

        if "under_23" in tournaments["name"]:
            stats_dist_list = list(
                filter(
                    lambda c: c["age"] <= 23,
                    stats_dist_list,
                )
            )

        if is_recommend:
            card_pool: list[SelectCard] = list(
                filter(
                    lambda c: c not in pre_select_cards,
                    stats_dist_list,
                )
            )
        else:
            card_pool: list[SelectCard] = list(
                filter(
                    lambda c: c["rarity"] in allowed_rarities
                    and (c["id"] not in map(lambda u: u["id"], used_cards))
                    and (c not in pre_select_cards),
                    stats_dist_list,
                )
            )

        # filter card_pool average less than expect's mean
        card_pool: list[SelectCard] = list(
            filter(lambda c: c["average"] < c["expect"].mean, card_pool)
        )

        to_select_card_count: int = 5 - pre_select
        possible_group: list[list[SelectCard]] = []

        if tournaments["tenGameAverageTotalLimit"] == 0:
            sorted_card_pool = sorted(
                card_pool, key=lambda c: c["expect"].mean, reverse=True
            )
            group_to_select.append(
                sorted_card_pool[:to_select_card_count] + pre_select_cards
            )
        else:
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

                if (
                    total_point <= tournaments["tenGameAverageTotalLimit"] - 5
                    or total_point > tournaments["tenGameAverageTotalLimit"]
                ):
                    continue

                if not is_recommend:
                    # check player duplicate
                    tmp_selected_players: list[str] = list(
                        map(lambda card: card["name"], all_5_cards)
                    )
                    unique_players: int = len(set(tmp_selected_players))
                    if unique_players != len(tmp_selected_players):
                        continue

                possible_group.append(all_5_cards)

            if len(possible_group) == 0:
                message = f"{tournaments['name']} no possible lineup\n"
                print(message)
                result_lines.append(message)
                continue

            group_index_to_cdf: dict[int, float] = {}

            for index, group in enumerate(possible_group):
                total_dist: NormalDist = NormalDist(0, 0)
                for card in group:
                    total_dist += card["expect"]
                try:
                    p_of_reach_target = total_dist.cdf(
                        target / (divisor if is_recommend else 1)
                    )
                    if p_of_reach_target < 1 - probability_reach_target:
                        group_index_to_cdf[index] = p_of_reach_target
                except:
                    continue

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
        if len(group_to_select) == 0:
            result = f"{tournaments['name']} no possible lineup"
            print(result)
            result_lines.append(result)
            continue
        for index, group in enumerate(group_to_select):
            print(
                f"Group: {index}, total: {sum([card['average'] for card in group])}, expect: {sum([card['expect']*divisor if is_recommend else card['expect'] for card in group])}"
            )
            for select_card in group:
                print(
                    f"{select_card['name']}({select_card['rarity'] if select_card['rarity'] != None else min_rarity.value},{select_card['average']}) {show_opposite_team(select_card['team'], matches=matches)}"  # type: ignore
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
            result_lines.append(f"{tournaments['name']} no possible lineup\n")

        result_lines.append("\n")

    # write result lines to file
    with open(f"data/result-{today_str}.txt", "w") as f:
        f.writelines(result_lines + "\n" for result_lines in result_lines)
        print("compute done, save in data/result.txt")
