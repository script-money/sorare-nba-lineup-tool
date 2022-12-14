# tournaments
# target 可以根据奖池目标进行设置，如果目标太高，会倾向于选表现更不稳定的球员
from types_ import Tournaments, CardRarity, NBAConference


common_champion: Tournaments = {
    "name": "common_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 265,
}

common_contender: Tournaments = {
    "name": "common_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 180,
}

common_western_conference: Tournaments = {
    "name": "common_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.west,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 260,
}

common_eastern_conference: Tournaments = {
    "name": "common_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.east,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 260,
}

common_underdog: Tournaments = {
    "name": "common_underdog",
    "tenGameAverageTotalLimit": 60,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 110,
}

common_no_cap: Tournaments = {
    "name": "common_no_cap",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 285,
}

rare_champion: Tournaments = {
    "name": "rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited, CardRarity.rare],
    "minRarity": {
        "minCount": 3,
        "rarity": CardRarity.rare,
    },
    "target": 250,
}

rare_contender: Tournaments = {
    "name": "rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited, CardRarity.rare],
    "minRarity": {
        "minCount": 3,
        "rarity": CardRarity.rare,
    },
    "target": 175,
}

super_rare_contender: Tournaments = {
    "name": "super_rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare, CardRarity.super_rare],
    "minRarity": {
        "minCount": 3,
        "rarity": CardRarity.super_rare,
    },
    "target": 180,
}

super_rare_champion: Tournaments = {
    "name": "super_rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare, CardRarity.super_rare],
    "minRarity": {
        "minCount": 3,
        "rarity": CardRarity.super_rare,
    },
    "target": 255,
}

limited_champion: Tournaments = {
    "name": "limited_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 240,
}

limited_contender: Tournaments = {
    "name": "limited_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 170,
}

limited_no_cap: Tournaments = {
    "name": "limited_no_cap",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 285,
}

limited_underdog: Tournaments = {
    "name": "limited_underdog",
    "tenGameAverageTotalLimit": 60,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 110,
}

limited_western_conference: Tournaments = {
    "name": "limited_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.west,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 200,
}

limited_eastern_conference: Tournaments = {
    "name": "limited_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.east,
    "allowedRarities": [CardRarity.limited],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.limited,
    },
    "target": 200,
}


# 球员表现和评分差异服从正态分布，mu是该分布的均值，例如球员评分30，mu=0.1，则表现的期望均值是33
# 下面设置的mu加成（或削减）都是经验值，不保证100%准确，可以自己微调
compute_by_recent_n_weeks_games: int = 10  # 计算最近n周比赛的表现变化率
mu_of_game_decision: float = -0.1  # 伤病报告里面game_decision的可能会打也可能不打，表现变化率均值的加该负值
mu_of_max_rank_team_bonus_ratio: float = 0.2  # 如果对手是攻防最弱球队，表现变化率均值的最大加成，反之打强队削减
mu_of_home_bonus: float = 0.04  # 表现变化率均值的主场加成
mu_of_home_b2b: float = -0.01  # 主场打背靠背表现变化率均值的扣减
mu_of_away_b2b: float = -0.02  # 客场打背靠背表现变化率均值的扣减
mu_of_single_game_bonus: float = -0.2  # 只打单场表现变化率均值的扣减
mu_of_multiple_games_bonus: float = 0.15  # 打3场及以上的比赛的表现变化率均值的加成
suggestion_count: int = 10
probability_reach_target: float = 0.03  # 从有该概率达到目标分数的结果中排序

all_tournaments: list[Tournaments] = [
    # common_champion,
    # common_contender,
    # common_underdog,
    # common_western_conference,
    # common_eastern_conference,
    # common_no_cap,
    # super_rare_contender,
    # rare_contender,
    # rare_champion,
    # limited_champion,
    # limited_contender,
    # super_rare_champion,
    # limited_western_conference,
    # limited_eastern_conference,
    # limited_no_cap,
    # limited_underdog,
]  # 更改联赛优先级，越前的会优先选卡

blacklist_cards: list[str] = [
    # "dbb7d8a8-4a7d-4097-b8b7-77f4faed2350",  # Sam Hauser
    # "839244ed-a59c-4b46-b13b-b124b49a8038",  # Kevin Huerter
    # "aa34b029-d04c-43de-8b3f-9f5ea58814dd",  # Kevin Huerter
    # "9754710e-0cea-4372-8d41-743781ca3ffb",  # Kevin Huerter
    # "aa3a4968-2d2d-419b-8e5b-85f3fbaae634",  # Brandon Ingram
    # "a6cca7ff-4832-4a1e-887d-35216e2c310e",  # Paul Reed
    # "ca553b45-5402-4541-a032-a6578da8c200",  # Eugene Omoruyi
]  # 设置不会被选中的id，重复卡建议设置

blacklist_players: list[str] = ["Duncan Robinson"]  # 把不查询的球员放在这里，只对recommend模式有效

suggest_cards: dict[str, dict[str, str]] = {
    "common_champion": {},
    "common_contender": {},
    "common_underdog": {},
    "common_western_conference": {},
    "common_eastern_conference": {},
    "common_no_cap": {},
    "super_rare_contender": {
        # "da82a46b-3265-4861-958f-5d13da220269": "Bruce Brown",
        # "306c2ecf-5fd3-4fc8-8bce-521d48705c57": "Nic Claxton",
        # "c8f7be3b-884c-4ba6-83c5-3a4ec08cb279": "Kentavious Caldwell-Pope",
        # "3b9c8713-2e0d-4fcc-89e5-2c3c892e24e8": "Trendon Watford",
    },
    "rare_contender": {
        # "a936c841-4039-4a09-82af-3b4e80b691fb": "Marcus Smart",
        # "5df4f5e8-7e52-4ee4-96a0-3cffafca2a02": "Buddy Hield",
    },
    "limited_contender": {},
    "super_rare_champion": {},
    "rare_champion": {
        # "3a4425d7-06f6-4382-86fc-ac29baadf125": "Ja Morant",
        # "ccacb679-5d6a-4539-b6d6-5392e4b39edf": "Giannis Antetokounmpo",
    },
    "limited_champion": {
        # "10c74499-37d5-4170-a952-3401588a3f8a": "Nikola Joki\u0107",
        # "93b7eca8-f70e-4720-bbac-3a9ccff3f970": "Jayson Tatum",
        # "7ff1a297-9236-4ca5-8295-a7a2b45dd7a1": "Russell Westbrook",
    },
    "limited_western_conference": {},
    "limited_eastern_conference": {},
    "limited_no_cap": {},
    "limited_underdog": {},
}  # 设置会被优先选中的卡的id，在 data/cards-xxxx-xx-xx.json 中发现 card 的 id 和 name
