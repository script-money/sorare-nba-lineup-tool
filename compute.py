import json
from pandas import DataFrame
from numpy import array
from statistics import NormalDist
from datetime import datetime
from itertools import combinations
from types_ import *
from scipy.stats import t
from pytz import timezone
from utils import ewma, rename_player
from config.config import *
import warnings
import argparse
import numpy as np
import pandas as pd
import os

warnings.filterwarnings("ignore")


def show_opposite_team(team: str, matches: list[Match]) -> str:
    """
    Get the match info that the given team will play in the next days

    Parameters
    ----------
    team: str
        The team for which to get the opponent
    matches: list[Match]
        A list of matches

    Returns
    -------
    str
        The match info that the given team will play in the next days
    """
    # filter matches to include only those that the team has played in
    matches_played: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )
    # if there are no matches played, return a message saying so
    if len(matches_played) == 0:
        return "No match"
    match_info: list[str] = []
    for match in matches_played:
        # check if the team played at home
        is_at_home: bool = match["home"] == team
        # get the team that they played against
        opposing_team: str = match["away"] if is_at_home else match["home"]
        # check if the team played against the opposing team on the previous day
        is_away_b2b: bool = match["away"] == team and match["away_is_b2b"]
        is_home_b2b: bool = match["home"] == team and match["home_is_b2b"]
        match_info.append(
            f"{'B2B ' if is_away_b2b or is_home_b2b else ''}vs {opposing_team} {'at HOME' if is_at_home else 'at AWAY'}"
        )
    return " and ".join(match_info)


def position_anlaysis(player: str, team: str | None) -> tuple[bool, bool, list[str]]:
    """Return if player is main player and next choose players.

    Args:
        player (str): Player name
        team (str | None): Team name

    Returns:
        tuple[bool, bool, list[str]]: (has reserve player, is main player, next choose players)
    """
    if team is None:
        return False, False, []
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
            return True, True, next_choose
        elif player in seconds:
            index = seconds.index(player)
            for third in thirds[index]:
                next_choose.append(third)
            return True, False, next_choose
        else:
            return False, False, next_choose


def get_score_with_ratio(
    stats: list[DetailedStats],
    stats_ratio: dict[str, float],
) -> list[float]:
    """Get score with ratio (some tournaments have special condition calculation)

    Args:
        stats (list[DetailedStats]): List of detailed stats.
        stats_ratio (dict[str, float]): Ratio of stats.

    Returns:
        list[float]: Score list with ratio.
    """
    if len(stats) == 0:
        return [0]
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
    stat_per_game: list[float] = []
    for stat in stats:
        detail: DetailedStat = stat["detailedStats"]
        total_point: float = sum(
            [
                detail["points"] * default_ratio["points"],
                detail["rebounds"] * default_ratio["rebounds"] * 1.2,
                detail["assists"] * default_ratio["assists"] * 1.5,
                detail["blocks"] * default_ratio["blocks"] * 3,
                detail["steals"] * default_ratio["steals"] * 3,
                detail["turnovers"] * default_ratio["turnovers"] * (-2),
                detail["made3PointFGs"] * default_ratio["made3PointFGs"],
                detail["doubleDoubles"] * default_ratio["doubleDoubles"],
                detail["tripleDoubles"] * default_ratio["tripleDoubles"],
            ]
        )
        stat_per_game.append(total_point)
    return stat_per_game


def predict(
    player: NBAPlayer,
    possible_match_players: dict[str, float],
    out_players: list[str],
    matches: list[Match],
    team_rank: TeamRank,
    stats_ratio: dict[str, float],
) -> NormalDist:
    """Predict a player's performance in the next week.

    Args:
        player (NBAPlayer): The player to predict
        possible_match_players (dict[str, float]): The names of players who have game-decision status
        out_players (list[str]): The names of players who are out
        matches (list[Match]): The list of next matches
        team_rank (TeamRank): The team rank information
        stats_ratio (dict[str, float]): The statistics ratio

    Returns:
        NormalDist: The prediction of the player's performance, in the form of a normal distribution
    """
    has_ratio: bool = stats_ratio != {}
    has_reserve, is_main, next_chooses = position_anlaysis(
        player["displayName"],
        player["team"]["abbreviation"] if player["team"] is not None else None,
    )
    next_chooses: list[str] = list(
        filter(
            lambda n: n not in out_players and n not in possible_match_players,
            next_chooses,
        )
    )

    all_card_week_scores: list[NBAPlayerInFixture] = player["latestFixtureStats"]

    all_card_week_scores = list(
        filter(
            lambda i: i["fixture"]["gameWeek"] not in exclude_game_weeks,
            all_card_week_scores,
        )
    )

    # get first not pending index
    last_game_week_index: int = next(
        (
            i
            for i, v in enumerate(all_card_week_scores)
            if v["status"]["statusIconType"]
            != PlayerInFixtureStatusIconType.pending.value
        )
    )
    last_week_type: str = all_card_week_scores[last_game_week_index]["status"][
        "statusIconType"
    ]

    player_name: str = player["displayName"]
    if (
        player_name in out_players
        and (
            last_week_type != PlayerInFixtureStatusIconType.no_game.value
            and last_week_type != PlayerInFixtureStatusIconType.did_not_play.value
        )
        and not has_ratio
        and show_injure_detail
    ):
        print(
            f"『{player_name}』is out for the next game"
            + f", reserve players are ❷『{'』,『'.join(next_chooses)}』"
            if has_reserve
            else ""
        )

    card_average: int = player["tenGameAverage"]
    team: str | None = None if player["team"] is None else player["team"]["fullName"]
    if player_name in possible_match_players and (
        last_week_type == PlayerInFixtureStatusIconType.no_game.value
        or last_week_type == PlayerInFixtureStatusIconType.did_not_play.value
    ):  # If in game_decision, but not on the last game, don't go on
        return NormalDist(0, 0)
    next_matches: int = len(
        list(filter(lambda m: m["away"] == team or m["home"] == team, matches))
    )  # the number of matches next week
    if (
        next_matches == 0 or player_name in out_players
    ):  # remove players who have no match next week and players who are confirmed injured
        return NormalDist(0, 0)

    stats_arr: list[float] = []
    for week in all_card_week_scores[
        last_game_week_index : last_game_week_index + compute_by_recent_n_weeks_games
    ]:
        if len(stats_ratio) == 0:
            for game_stat in week["status"]["gameStats"]:
                stats_arr.append(game_stat["score"])
        else:
            week_stat_array = get_score_with_ratio(
                week["status"]["gameStats"], stats_ratio
            )
            stats_arr.extend(
                week_stat_array
            )  # calculate the performance change rate of each game, which should float around 0

    if (
        has_reserve
    ):  # players who don't play may be injured, which doesn't affect the score, so filter out 0
        stats_arr = list(filter(lambda s: s != 0, stats_arr))

    if (
        len(stats_arr) == 0 or (array(stats_arr) == 0).all()
    ):  # for players who never play, there is no game data, so return 0 directly
        return NormalDist(0, 0)

    ewma_: list[float] = ewma(
        stats_arr, 0.2
    )  # use ewma to smooth the result, the coefficient can be adjusted, the smaller the value, the smaller the influence of the historical data
    _, mu, sigma = t.fit(ewma_, fdf=len(ewma_))  # type: ignore
    # use t distribution to fit the data to get the mean and standard deviation. For players who don't play much, sigma may be 0 with norm

    game_decision_bonus: float = 0

    if (
        player_name in possible_match_players
        and player_name not in suggest_players
        and is_game_decision_bonus_activate
    ):
        second_str = (
            f", reserve players are ❷『{'』,『'.join(next_chooses)}』"
            if has_reserve and len(next_chooses) != 0
            else ""
        )
        possible = possible_match_players[player_name]
        if not has_ratio and show_injure_detail:
            print(
                f"『{player_name}』have {possible:.0%} probability play in the next game, he has {next_matches} matches in next week"
                + second_str
            )
        game_decision_bonus = (
            possible - 1
        )  # If it is a probabilistic outing, subtract the score

    match_join: list[Match] = list(
        filter(lambda m: m["away"] == team or m["home"] == team, matches)
    )

    bonus: float = 0
    match_bonus: float = 0

    team_offense_rank = team_rank["team_offense_rank"].index(team)
    team_defense_rank = team_rank["team_defense_rank"].index(team)
    for match in match_join:
        team_bonus, opponent_bonus = 0, 0
        opponent: str = match["away"] if match["home"] == team else match["home"]
        opponent_offense_rank: int = team_rank["team_offense_rank"].index(opponent)
        opponent_defense_rank: int = team_rank["team_defense_rank"].index(opponent)
        is_opponent_home = match["home"] == opponent
        is_team_home = not is_opponent_home
        is_opponent_b2b = (match["away"] == opponent and match["away_is_b2b"]) or (
            match["home"] == opponent and match["home_is_b2b"]
        )
        is_team_b2b = (match["away"] == team and match["away_is_b2b"]) or (
            match["home"] == team and match["home_is_b2b"]
        )
        team_rank_bonus = -(
            (team_offense_rank + team_defense_rank - 30)
            / 30
            * mu_of_max_rank_team_bonus_ratio
        )
        team_home_bonus = is_team_home * mu_of_home_bonus
        team_b2b_bonus = is_team_b2b * mu_of_b2b
        opponent_rank_bonus = -(
            (opponent_offense_rank + opponent_defense_rank - 30)
            / 30
            * mu_of_max_rank_team_bonus_ratio
        )
        opponent_home_bonus = is_opponent_home * mu_of_home_bonus
        opponent_b2b_bonus = is_opponent_b2b * mu_of_b2b

        team_bonus = team_rank_bonus + team_home_bonus + team_b2b_bonus
        opponent_bonus = opponent_rank_bonus + opponent_home_bonus + opponent_b2b_bonus
        diff = abs(team_bonus - opponent_bonus)
        if diff <= 0.05:
            new_match_bonus = mu_of_main_player_in_high_value_game if is_main else 0
            match_bonus = (
                max(match_bonus, new_match_bonus)
                if match_bonus != 0
                else new_match_bonus
            )
        if diff >= 0.15:
            new_match_bonus = (
                mu_of_reserve_player_in_low_value_game if not is_main else 0
            )
            match_bonus = (
                max(match_bonus, new_match_bonus)
                if match_bonus != 0
                else new_match_bonus
            )
    # match count bonus
    match_count_bonus: float = 0
    if len(match_join) == 1:
        match_count_bonus += mu_of_single_game_bonus
    if len(match_join) > 2:
        match_count_bonus += mu_of_multiple_games_bonus

    bonus = game_decision_bonus + match_bonus + match_count_bonus
    mu += bonus * card_average

    future_performance: NormalDist = NormalDist(mu, sigma)
    return future_performance


def get_average_minutes(
    player_or_card: NBAPlayer | NBACard, last_n_games: int = 3
) -> int:
    """Get the average minutes of the player

    Args:
        player (NBAPlayer | NBACard): The player
        last_n_games (int, optional): The last n games for calculate. Defaults to 5.

    Returns:
        int: The average minutes
    """

    player: NBAPlayer = player_or_card["player"] if "player" in player_or_card else player_or_card  # type: ignore

    valid_weeks: list[NBAPlayerInFixture] = list(
        filter(
            lambda s: s["status"]["statusIconType"]
            != PlayerInFixtureStatusIconType.pending.value
            and s["status"]["statusIconType"]
            != PlayerInFixtureStatusIconType.no_game.value
            and s["status"]["statusIconType"]
            != PlayerInFixtureStatusIconType.inactive.value,
            player["latestFixtureStats"],
        )
    )

    latest_n_game_seconds: list[float] = []

    for week in valid_weeks:
        week_stats: list[DetailedStats] = week["status"]["gameStats"]
        if len(week_stats) == 0:
            continue
        for stat in week_stats:
            secords = stat["detailedStats"]["secondsPlayed"]

            if len(latest_n_game_seconds) < last_n_games:
                latest_n_game_seconds.append(secords)
            else:
                break

    if len(latest_n_game_seconds) == 0:
        return 0
    total_seconds = round(np.mean(latest_n_game_seconds))
    return round(total_seconds / 60)


def get_all_cards_with_prediction(
    avaliable_players: list[NBAPlayer], stats_ratio: dict[str, float] = {}
) -> list[SelectCard]:
    """Return all cards with prediction

    Args:
        avaliable_players (list[NBAPlayer]): All players can be selected
        stats_ratio (dict[str, float], optional): The ratio of each stat. Defaults to {}.

    Returns:
        list[SelectCard]: All cards with prediction
    """
    all_cards_with_prediction_list = []

    if is_recommend:
        for player in avaliable_players:
            player_name: str = player["displayName"]
            average_minutes = get_average_minutes(player)

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
                "minutes": average_minutes,
                "team": player["team"]["fullName"],
                "id": None,
            }
            all_cards_with_prediction_list.append(card_dist)
    else:
        for card in avaliable_cards:
            player_name: str = card["player"]["displayName"]
            average_minutes = get_average_minutes(card)

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
                "minutes": average_minutes,
                "team": None
                if card["player"]["team"] is None
                else card["player"]["team"]["fullName"],
                "id": card["id"],
            }
            all_cards_with_prediction_list.append(card_dist)
    return all_cards_with_prediction_list


def load_data(
    today: str,
) -> tuple[
    list[NBACard],
    list[NBACard],
    list[NBACard],
    list[NBACard],
    list[str],
    dict[str, float],
    list[Match],
    TeamRank,
    list[NBACard],
    dict[str, MatchProbility],
    list[str],
]:
    with open(f"data/cards.json", "r") as f:
        cards: list[NBACard] = json.load(f)

    with open(f"data/injure-{today}.json", "r") as g:
        injure: list[Injure] = json.load(g)

    with open(f"data/next-week-{today}.json", "r") as h:
        matches: list[Match] = json.load(h)

    with open(f"data/team-rank.json", "r") as i:
        team_rank: TeamRank = json.load(i)

    # load probility
    with open(f"data/all_probility.json", "r") as j:
        # use rename_player for all_probility.keys
        all_probility: dict[str, MatchProbility] = {
            rename_player(k): v for k, v in json.load(j).items()
        }

    common_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "common", cards))
    limited_cards: list[NBACard] = list(
        filter(lambda c: c["rarity"] == "limited", cards)
    )
    rare_cards: list[NBACard] = list(filter(lambda c: c["rarity"] == "rare", cards))
    super_rare_cards: list[NBACard] = list(
        filter(lambda c: c["rarity"] == "super_rare", cards)
    )

    out_players: list[str] = list(
        map(lambda j: j["player"], filter(lambda i: i["injure_type"] == "Out", injure))
    )
    filter_players = list(
        filter(
            lambda i: i["injure_type"] == "Questionable"
            or i["injure_type"] == "Probable"
            or i["injure_type"] == "Doubtful",
            injure,
        )
    )
    # add probility to filter_players
    for player in filter_players:
        injure_type = player["injure_type"]
        if player["player"] not in all_probility:
            player["probility"] = default_match_probility[injure_type]
        else:
            player["probility"] = all_probility[player["player"]][injure_type]

    game_decision_players = {
        info["player"]: info["probility"] for info in filter_players  # type: ignore
    }

    avaliable_cards: list[NBACard] = list(
        filter(
            lambda t: t["id"] not in blacklist_cards,
            cards,
        )
    )

    # get player names in suggest_cards
    suggest_players: list[str] = []
    for tournament in suggest_cards:
        for card_id in suggest_cards[tournament]:
            suggest_players.append(suggest_cards[tournament][card_id])

    return (
        common_cards,
        limited_cards,
        rare_cards,
        super_rare_cards,
        out_players,
        game_decision_players,
        matches,
        team_rank,
        avaliable_cards,
        all_probility,
        suggest_players,
    )


if __name__ == "__main__":
    p: argparse.ArgumentParser = argparse.ArgumentParser()

    p.add_argument("-r", "--recommend", required=False)
    args = p.parse_args()

    is_recommend = False

    if args.recommend:
        is_recommend = True

    today_str: str = datetime.now(timezone("US/Eastern")).strftime("%Y-%m-%d")
    # today_str = "2023-02-27"

    (
        common_cards,
        limited_cards,
        rare_cards,
        super_rare_cards,
        out_players,
        game_decision_players,
        matches,
        team_rank,
        avaliable_cards,
        match_probility,
        suggest_players,
    ) = load_data(today_str)

    print(
        f"\nLoad {len(common_cards)} common, {len(limited_cards)} limited, {len(rare_cards)} rare, {len(super_rare_cards)} super rare cards."
    )
    print()

    avaliable_players = []
    if is_recommend:
        with open(f"data/all-players-data.json", "r") as f:
            players: list[NBAPlayer] = json.load(f)

        # Get all players who aren't blacklisted
        avaliable_players: list[NBAPlayer] = list(
            filter(
                lambda t: t["displayName"] not in blacklist_players,
                players,
            )
        )

        if len(avaliable_players) == 0:
            print("No avaliable players found, please check data/all-players-data.json")
            exit(1)

        # If we're only recommending from a specific team, filter to only include those players
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

    df = DataFrame()
    if is_recommend:
        caceh_file_path = f"data/cached_recommend.pickle"
    else:
        caceh_file_path = f"data/cached.pickle"
    if os.path.exists(caceh_file_path):
        print(f"Found {caceh_file_path}, do you want to use it? (Y/n)")
        if input().upper() == "Y":
            df = pd.read_pickle(caceh_file_path)
            # convert df to list
            all_stats_dist_list = df.to_dict("records")
        else:
            all_stats_dist_list = get_all_cards_with_prediction(avaliable_players)

            # convert all_stats_dist_list to dataframe
            df = DataFrame(all_stats_dist_list)
    else:
        all_stats_dist_list: list[SelectCard] = get_all_cards_with_prediction(
            avaliable_players
        )

        # convert all_stats_dist_list to dataframe
        df = DataFrame(all_stats_dist_list)

    df["mean"] = df["expect"].apply(lambda x: x.mean)

    def compute_outperform(mean, average):
        return round(mean - average, 2)

    # create column name outperform equal round(expect.mean - average)
    df["outperform"] = df.apply(
        lambda x: compute_outperform(x["mean"], x["average"]), axis=1
    )
    df_show: DataFrame = df.sort_values(by="mean", ascending=False)
    print("\nAll players stats:")
    df_show = df_show.drop(columns=["mean"])
    print(
        df_show.to_string(
            index=False,
            columns=["name", "rarity", "minutes", "average", "expect", "outperform"],
        )
    )

    if show_top_10_outperform:
        # print top 10 outperform players
        print("\nTop 10 outperform players:")
        top10_df = (
            df[df["rarity"] != "common"]
            .sort_values(by="outperform", ascending=False)
            .head(10)[["name", "rarity", "average"]]
        )
        # print with format name1(average1), name2(average2), ...
        print(
            ", ".join(
                [
                    f"{name}({rarity+',' if rarity is not None else ''}{average})"
                    for name, rarity, average in top10_df.values
                ]
            )
        )

    df_show = df_show.drop(columns=["outperform"])

    # save df_show to data folder
    df_show.to_pickle(caceh_file_path)

    # user input Y to continue
    input(
        "Press any key to continue (You can press Ctrl+C to stop program and set suggest or blacklist card in config): "
    )

    print(f"{len(all_tournaments)} tournaments found")

    result_lines = []
    choose_no_result = False
    for select_groups_epoch in range(suggestion_count):
        if choose_no_result:
            break
        result_lines.append("-" * 50)
        print(f"\nSelecting cards for No.{select_groups_epoch + 1} group(s)...")
        used_cards = []
        try:
            for tournament_index, tournaments in enumerate(all_tournaments):
                group_to_select: list[list[SelectCard]] = []
                if (
                    tournaments["name"] in suggest_cards
                ):  # current tournament in suggest_cards(preconfig)
                    suggest_players_id_to_name: dict[str, str] = suggest_cards[
                        tournaments["name"]
                    ]
                    pre_select: int = len(suggest_players_id_to_name)
                else:
                    pre_select = 0

                stats_dist_list: list[SelectCard] = (
                    all_stats_dist_list.copy()
                    if "multiplier" not in tournaments
                    else get_all_cards_with_prediction(
                        avaliable_players, tournaments["multiplier"]
                    )
                )  # TODO make get with ratio cache

                # in recommend mode, select cards by name, but in normal mode, select cards by id
                pre_select_cards: list[SelectCard] = (
                    list(
                        filter(
                            lambda c: c["name"] in suggest_players_id_to_name.values()
                            if is_recommend
                            else c["id"] in suggest_players_id_to_name.keys(),
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

                allowed_rarities: list[str] = [
                    t.value for t in tournaments["allowedRarities"]
                ]
                allow_mvp: bool = tournaments["allowMVP"]
                target: int = tournaments["target"]
                allowed_conference: NBAConference | None = tournaments[
                    "allowedConference"
                ]
                is_common: bool = tournaments["minRarity"] is None
                min_rarity: CardRarity | None = (
                    None if is_common else tournaments["minRarity"]["rarity"]  # type: ignore
                )
                divisor: float = 1
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
                    if allowed_conference.value == "WESTERN":
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
                    filter(
                        lambda c: c["average"] < c["expect"].mean - outperform_treshold,
                        card_pool,
                    )
                )

                to_select_card_count: int = 5 - pre_select
                possible_group: list[list[SelectCard]] = []
                max_group_index, max_group_value = -1, -1

                if tournaments["tenGameAverageTotalLimit"] == 0:
                    sorted_card_pool = sorted(
                        card_pool, key=lambda c: c["expect"].mean, reverse=True
                    )
                    group_to_select.append(
                        sorted_card_pool[:to_select_card_count] + pre_select_cards
                    )
                else:
                    for possible in combinations(card_pool, to_select_card_count):  # type: ignore
                        all_5_cards: list[SelectCard] = (
                            list(possible) + pre_select_cards
                        )

                        # check total points
                        total_point: int = (
                            sum([card["average"] for card in all_5_cards])
                            if not allow_mvp
                            else sum(
                                [
                                    card["average"]
                                    for card in sorted(
                                        all_5_cards,
                                        key=lambda c: c["average"],
                                        reverse=True,
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
                        message = f"{tournaments['name']} no possible group\n"
                        print(message)
                        result_lines.append(message)
                        continue

                    group_index_to_cdf: dict[int, float] = {}

                    for index, group in enumerate(possible_group):
                        total_dist: NormalDist = NormalDist(0, 0)
                        for card in group:
                            total_dist += card["expect"]
                            if (
                                total_dist.mean > max_group_value
                            ):  # record best group if use for no possible lineup
                                max_group_value = total_dist.mean
                                max_group_index = index
                        try:
                            p_of_reach_target = total_dist.cdf(
                                (target + target_adjust)
                                / (divisor if is_recommend else 1)
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
                            map(
                                lambda item: possible_group[item[0]],
                                sorted_possible_group,
                            )
                        )

                print(f"❗️Selecting {tournaments['name']}")
                if len(group_to_select) == 0:
                    best_group: list[SelectCard] = possible_group[max_group_index]
                    print(
                        f"total: {sum([card['average'] for card in best_group])}, expect to {sum([card['expect']*divisor if is_recommend else card['expect'] for card in best_group])}, best lineup:"
                    )
                    result_lines.append(f"{tournaments['name']}")
                    for select_card in best_group:
                        print(
                            f"🏀 {select_card['name']} ({select_card['average']}, mins:{select_card['minutes']}, mean:{round(select_card['expect'].mean - select_card['average']):+}, stdev:{select_card['expect'].stdev:.2f})"  # type: ignore
                        )
                        result_lines.append(
                            f'"{select_card["id"]}": "{select_card["name"]}",'
                        )
                    result_lines.append("\n")
                    if tournament_index == 0:
                        choose_no_result = True
                    continue

                index: int = select_groups_epoch if tournament_index == 0 else 0
                group = group_to_select[index]
                print(
                    f"total: {sum([card['average'] for card in group])}, expect: {sum([card['expect']*divisor if is_recommend else card['expect'] for card in group])}"
                )
                for select_card in group:
                    print(
                        f"🏀 {select_card['name']}({select_card['average']},{select_card['minutes']}mins) {show_opposite_team(select_card['team'], matches=matches)}"  # type: ignore
                    )
                # print("\n")

                select_cards: list[SelectCard] = []

                for select_card in group_to_select[index]:
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
        except IndexError:
            print("no more selection, break")
            break

    # write result lines to file
    if len(result_lines) > 0:
        with open(f"data/result-{today_str}.txt", "w") as f:
            f.writelines(result_lines + "\n" for result_lines in result_lines)
            print("\ncompute done, save in data/result.txt")
