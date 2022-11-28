# tournaments
# target 可以根据奖池目标进行设置，如果目标太高，会倾向于选表现更不稳定的球员
common_champion = {
    "name": "common_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": ["common"],
    "minRarity": None,
    "target": 300,
}

common_contender = {
    "name": "common_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": ["common"],
    "minRarity": None,
    "target": 250,
}

common_western_conference = {
    "name": "common_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": "WESTERN",
    "allowedRarities": ["common"],
    "minRarity": None,
    "target": 280,
}

common_eastern_conference = {
    "name": "common_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": "EASTERN",
    "allowedRarities": ["common"],
    "minRarity": None,
    "target": 280,
}

rare_champion = {
    "name": "rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": ["limited", "rare"],
    "minRarity": {
        "minCount": 3,
        "rarity": "rare",
    },
    "target": 180,
}

rare_contender = {
    "name": "rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": ["limited", "rare"],
    "minRarity": {
        "minCount": 3,
        "rarity": "rare",
    },
    "target": 240,
}

super_rare_contender = {
    "name": "super_rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": ["rare", "super_rare"],
    "minRarity": {
        "minCount": 3,
        "rarity": "super_rare",
    },
    "target": 180,
}

super_rare_champion = {
    "name": "super_rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": ["rare", "super_rare"],
    "minRarity": {
        "minCount": 3,
        "rarity": "super_rare",
    },
    "target": 255,
}

limited_champion = {
    "name": "limited_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": ["limited"],
    "minRarity": {
        "minCount": 5,
        "rarity": "limited",
    },
    "target": 250,
}

limited_contender = {
    "name": "limited_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": ["limited"],
    "minRarity": {
        "minCount": 5,
        "rarity": "limited",
    },
    "target": 220,
}

limited_western_conference = {
    "name": "limited_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": "WESTERN",
    "allowedRarities": ["limited"],
    "minRarity": {
        "minCount": 5,
        "rarity": "limited",
    },
    "target": 280,
}

limited_eastern_conference = {
    "name": "limited_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": "EASTERN",
    "allowedRarities": ["limited"],
    "minRarity": {
        "minCount": 5,
        "rarity": "limited",
    },
    "target": 280,
}


# 球员表现和评分差异服从正态分布，mu是该分布的均值，例如球员评分30，mu=0.1，则表现的期望均值是33
# 下面设置的mu加成（或削减）都是经验值，不保证100%准确，可以自己微调
compute_by_recent_n_weeks_games = 8  # 计算最近n周比赛的表现变化率
mu_of_game_decision = -0.1  # 伤病报告里面game_decision的可能会打也可能不打，表现变化率均值的加该负值
mu_of_max_rank_team_bonus_ratio = 0.2  # 如果对手是攻防最弱球队，表现变化率均值的最大加成，反之打强队削减
mu_of_home_bonus = 0.04  # 表现变化率均值的主场加成
mu_of_home_b2b = -0.01  # 主场打背靠背表现变化率均值的扣减
mu_of_away_b2b = -0.02  # 客场打背靠背表现变化率均值的扣减
mu_of_single_game_bonus = -0.25  # 只打单场表现变化率均值的扣减
mu_of_multiple_games_bonus = 0.15  # 打3场及以上的比赛的表现变化率均值的加成
mvp_threshold = 35  # MVP选择的最低阈值

all_tournaments = [
    common_champion,
    common_contender,
    # common_western_conference,
    common_eastern_conference,
    super_rare_champion,
    super_rare_contender,
    rare_champion,
    rare_contender,
    limited_champion,
    limited_contender,
    # limited_western_conference,
    limited_eastern_conference,
]  # 更改联赛优先级，越前的会优先选卡
