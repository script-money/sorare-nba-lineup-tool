import json
import math
import numpy as np
from statistics import NormalDist
from datetime import datetime
from itertools import combinations
from pytz import timezone
from utils import ewma, divide, exclude_best_and_worst
from config.config import (
    mu_of_game_decision,
    compute_by_recent_n_weeks_games,
    mu_of_max_rank_team_bonus_ratio,
    mvp_threshold,
    mu_of_home_bonus,
    mu_of_away_b2b,
    mu_of_home_b2b,
    mu_of_single_game_bonus,
    mu_of_multiple_games_bonus,
    all_tournaments,
)

western_teams = [
    "Sacramento Kings",
    "New Orleans Pelicans",
    "Utah Jazz",
    "Oklahoma City Thunder",
    "Golden State Warriors",
    "Phoenix Suns",
    "Denver Nuggets",
    "Minnesota Timberwolves",
    "Memphis Grizzlies",
    "Los Angeles Lakers",
    "San Antonio Spurs",
    "Dallas Mavericks",
    "Portland Trail Blazers",
    "Houston Rockets",
    "Los Angeles Clippers",
]

today = datetime.now(timezone("US/Eastern"))
today_str = today.strftime("%Y-%m-%d")
with open(f"data/cards-{today_str}.json", "r") as f:
    cards = json.load(f)
with open(f"data/injure-{today_str}.json", "r") as g:
    injure = json.load(g)
with open(f"data/next-week-{today_str}.json", "r") as h:
    matches = json.load(h)
with open(f"data/team-rank-{today_str}.json", "r") as i:
    team_rank = json.load(i)

common_cards = list(filter(lambda c: c["rarity"] == "common", cards))
limited_cards = list(filter(lambda c: c["rarity"] == "limited", cards))
rare_cards = list(filter(lambda c: c["rarity"] == "rare", cards))
super_rare_cards = list(filter(lambda c: c["rarity"] == "super_rare", cards))

print(
    f"Load {len(common_cards)} common, {len(limited_cards)} limited, {len(rare_cards)} rare, {len(super_rare_cards)} super rare cards."
)

out_players = list(
    map(lambda j: j["player"], filter(lambda i: not i["game_time_decision"], injure))
)
game_decision_players = list(
    map(lambda j: j["player"], filter(lambda i: i["game_time_decision"], injure))
)
avaliable_cards = list(
    filter(lambda t: t["player"]["displayName"] not in out_players, cards)
)

# 获取球队下周比赛数量
def get_team_match_count(team):
    return len(list(filter(lambda m: m["away"] == team or m["home"] == team, matches)))


# 根据对阵进行加成
def get_match_bonus(team) -> float:
    match_join = list(filter(lambda m: m["away"] == team or m["home"] == team, matches))
    k_list = []
    bonus = 0
    # 1. 获取对手攻防实力，按标准化加成
    if len(match_join) == 0:
        return -9999
    for match in match_join:
        opponent = match["away"] if match["home"] == team else match["home"]
        offense_rank = team_rank["team_offense_rank"].index(opponent)
        defense_rank = team_rank["team_defense_rank"].index(opponent)
        k = (
            (offense_rank - 15) / 30 + (defense_rank - 15) / 30
        ) * mu_of_max_rank_team_bonus_ratio
        k_list.append(k)
    opponent_bonus = sum(k_list) / len(k_list) if len(k_list) != 0.0 else 0.0
    # 2. 主客场加成
    home_bonus = 0
    for match in match_join:
        if match["home"] == team:
            home_bonus += mu_of_home_bonus
    # 3. 背靠背
    b2b_bonus = 0
    for match in match_join:
        if (
            match["away"] == team and match["away_is_b2b"] and not match["home_is_b2b"]
        ):  # 客场背靠背且对手不是背靠背
            b2b_bonus -= mu_of_away_b2b
        if match["home"] == team and match["home_is_b2b"] and not match["away_is_b2b"]:
            b2b_bonus -= mu_of_home_b2b
    # 4. 比赛场数
    match_count_bonus = 0
    if len(match_join) == 1:
        match_count_bonus += mu_of_single_game_bonus
    if len(match_join) > 2:
        match_count_bonus += mu_of_multiple_games_bonus
    bonus = opponent_bonus + home_bonus + b2b_bonus + match_count_bonus
    return bonus


if __name__ == "__main__":
    all_stats_dist_list = []

    for card in avaliable_cards:
        id = card["id"]
        total_bonus = card["totalBonus"]
        team = card["team"]["fullName"]
        all_card_scores = card["player"]["latestFinalFixtureStats"]
        card_scores = list(
            filter(
                lambda g: g["status"]["statusIconType"] != "NO_GAME",
                all_card_scores[2 : 2 + compute_by_recent_n_weeks_games],  # 取最近7周比赛
            )
        )
        player_name = card["player"]["displayName"]
        # ------------check single player--------------
        # if player_name != "Ja Morant":
        #     continue
        card_average = card["player"]["tenGameAverage"]
        card_rarity = card["rarity"]
        next_matches = get_team_match_count(team)
        if next_matches == 0 or player_name in out_players:  # 去掉下周没有比赛的球员和确定受伤不打的球员
            continue
        stats_arr = list(
            map(
                lambda s: divide(s["score"] - s["tenGameAverage"], s["tenGameAverage"]),
                card_scores,
            )
        )  # 计算每场比赛的表现变化率，应该0上下浮动
        clean_stats_arr = exclude_best_and_worst(stats_arr)
        if len(clean_stats_arr) == 0:
            continue
        ewma_ = ewma(clean_stats_arr, 0.5)  # 用ewma平滑结果，系数可以调整，该数值越小，历史数据的影响越小
        mu: float = np.mean(ewma_).__float__()
        sigma = np.std(ewma_, ddof=1).__float__()
        if math.isnan(sigma):
            continue
        if player_name in game_decision_players:
            mu += mu_of_game_decision
        team_bonus = get_match_bonus(team)
        mu += team_bonus
        future_performance = (NormalDist(mu, sigma) * card_average + card_average) * (
            1 + total_bonus
        )
        card_dist = [
            player_name,
            card_average,
            card_rarity,
            future_performance,
            team,
            id,
        ]
        all_stats_dist_list.append(card_dist)

    result_lines = []
    used_cards = []

    for tournaments in all_tournaments:
        select_cards = []
        stats_dist_list = all_stats_dist_list.copy()
        high_rarity_count = 0

        allowed_rarities = tournaments["allowedRarities"]
        allow_mvp = tournaments["allowMVP"]
        allowed_conference = tournaments["allowedConference"]
        is_common = tournaments["minRarity"] is None
        min_rarity = None if is_common else tournaments["minRarity"]["rarity"]
        min_count = 5 if is_common else tournaments["minRarity"]["minCount"]

        if allowed_conference != None:
            if allowed_conference == "WESTERN":
                stats_dist_list = list(
                    filter(
                        lambda c: c[4] in western_teams,
                        all_stats_dist_list,
                    )
                )
            else:
                stats_dist_list = list(
                    filter(
                        lambda c: c[4] not in western_teams,
                        all_stats_dist_list,
                    )
                )

        avaliable_cards_with_condition = list(
            filter(
                lambda c: c[2] in allowed_rarities and c not in used_cards,
                stats_dist_list,
            )
        )

        if allow_mvp:  # 选择mvp
            best_card = max(
                avaliable_cards_with_condition,
                key=lambda c: c[3].mean and c[1] >= mvp_threshold,
            )
            if best_card[2] == min_rarity and min_rarity != None:
                high_rarity_count += 1
            select_cards.append(best_card)
            used_cards.append(best_card)

        # exclude used cards
        card_pool = list(
            filter(lambda c: c not in used_cards, avaliable_cards_with_condition)
        )
        to_select_card_count = 4 if tournaments["allowMVP"] else 5
        all_possible = combinations(card_pool, to_select_card_count)
        other_cards = []
        for possible in all_possible:
            total_point = sum([card[1] for card in possible])
            rarities_count = (
                5
                if is_common
                else len(list(filter(lambda card: card[2] == min_rarity, possible)))
            )
            players = list(map(lambda card: card[0], possible))
            unique_players = len(set(players))  # type: ignore

            if (
                total_point <= tournaments["tenGameAverageTotalLimit"]
                and unique_players == len(players)
                and rarities_count + high_rarity_count >= min_count
            ):
                other_cards.append(possible)

        cdf = []
        for group in other_cards:
            all_dist = NormalDist(0, 0)
            for card in group:
                dist = card[3]
                all_dist += dist
            cdf.append(all_dist.cdf(tournaments["target"]))

        if len(cdf) != 0:
            min_cdf = min(cdf)
            min_cdf_index = cdf.index(min_cdf)
            best_group = other_cards[min_cdf_index]
            for card in best_group:
                select_cards.append(card)
                used_cards.append(card)
            result_lines.append(f"{tournaments['name']}")
            expect_sum = 0
            for card in select_cards:
                expect = card[3].mean
                result_lines.append(f"{card[0]} {card[2]} {expect:.2f}")
                expect_sum += expect
            result_lines.append(f"expect: {expect_sum:.2f}")
        else:
            result_lines.append(f"{tournaments['name']} no possible lineup")

        result_lines.append("\n")

    # write result lines to file
    with open(f"data/result-{today_str}.txt", "w") as f:
        f.writelines(result_lines + "\n" for result_lines in result_lines)
        print("compute done, save in data/result.txt")
