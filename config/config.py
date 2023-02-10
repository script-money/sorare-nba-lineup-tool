from types_ import Tournaments, CardRarity, NBAConference


common_champion: Tournaments = {
    "name": "common_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 265,  # target can be set according to the prize pool target, if the target is too high, it will tend to pick players with more inconsistent performance
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

common_all_offense: Tournaments = {
    "name": "common_all_offense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 220,
    "multiplier": {
        "points": 1,
        "blocks": 0,
        "rebounds": 1,
        "steals": 0,
        "assists": 1,
        "turnovers": 0,
        "made3PointFGs": 1,
        "doubleDoubles": 1,
        "tripleDoubles": 1,
    },
}


common_all_defense: Tournaments = {
    "name": "common_all_defense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 150,
    "multiplier": {
        "points": 0,
        "blocks": 1,
        "rebounds": 1,
        "steals": 1,
        "assists": 0,
        "turnovers": 0,
        "made3PointFGs": 0,
        "doubleDoubles": 0,
        "tripleDoubles": 0,
    },
}

common_veterans: Tournaments = {
    "name": "common_veterans",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 220,
}

common_under_23: Tournaments = {
    "name": "common_under_23",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 220,
}


season_of_giving: Tournaments = {
    "name": "season_of_giving",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 380,
    "multiplier": {
        "rebounds": 2,
        "assists": 2,
    },
}

deck_the_halls: Tournaments = {
    "name": "deck_the_halls",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited, CardRarity.rare, CardRarity.super_rare],
    "minRarity": None,
    "target": 250,
}

rare_champion: Tournaments = {
    "name": "rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 250,
}

rare_contender: Tournaments = {
    "name": "rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 175,
}

super_rare_contender: Tournaments = {
    "name": "super_rare_contender",
    "tenGameAverageTotalLimit": 110,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.super_rare,
    },
    "target": 180,
}

super_rare_champion: Tournaments = {
    "name": "super_rare_champion",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
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
    "target": 120,
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

limited_all_offense: Tournaments = {
    "name": "limited_all_offense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": None,
    "target": 220,
    "multiplier": {
        "points": 1,
        "blocks": 0,
        "rebounds": 1,
        "steals": 0,
        "assists": 1,
        "turnovers": 0,
        "made3PointFGs": 1,
        "doubleDoubles": 1,
        "tripleDoubles": 1,
    },
}

limited_all_defense: Tournaments = {
    "name": "limited_all_defense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": None,
    "target": 120,
    "multiplier": {
        "points": 0,
        "blocks": 1,
        "rebounds": 1,
        "steals": 1,
        "assists": 0,
        "turnovers": 0,
        "made3PointFGs": 0,
        "doubleDoubles": 0,
        "tripleDoubles": 0,
    },
}

limited_under_23: Tournaments = {
    "name": "limited_under_23",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": None,
    "target": 220,
}

limited_veterans: Tournaments = {
    "name": "limited_veterans",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": None,
    "target": 220,
}


rare_underdog: Tournaments = {
    "name": "rare_underdog",
    "tenGameAverageTotalLimit": 60,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 130,
}

rare_no_cap: Tournaments = {
    "name": "rare_no_cap",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 300,
}

rare_veterans: Tournaments = {
    "name": "rare_veterans",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": None,
    "target": 230,
}

super_rare_underdog: Tournaments = {
    "name": "super_rare_underdog",
    "tenGameAverageTotalLimit": 60,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.super_rare,
    },
    "target": 140,
}

super_rare_no_cap: Tournaments = {
    "name": "super_rare_no_cap",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.super_rare,
    },
    "target": 300,
}

# Player performance a normal distribution, mu is the average value of the distribution, for example, player rating 30, mu = 0.1, then the expected average value of performance is 33
# The mu additions (or reductions) set below are empirical values and are not guaranteed to be 100% accurate, so you can fine-tune them yourself
compute_by_recent_n_weeks_games: int = (
    3  # Calculate the rate of change in performance for the last n weeks of play
)
mu_of_home_bonus: float = (
    0.04  # Home additions to the mean rate of change in performance
)
mu_of_home_b2b: float = (
    -0.15
)  # Deductions for mean change in home playing back-to-back performance
mu_of_away_b2b: float = (
    -0.2
)  # Deductions for mean change in away playing back-to-back performance
mu_of_single_game_bonus: float = (
    -0.2
)  # Deductions for average single-game performance change only
mu_of_multiple_games_bonus: float = (
    0.1  # of performance change averages for games played 3 or more
)
outperform_treshold: float = (
    -2
)  # include players who average - outperform more than this value
show_top_10_outperform = True
suggestion_count: int = 3  # Number of recommended results
probability_reach_target: float = 0.01  # Sort from the results that have that probability of reaching the target score
show_injure_detail = True

all_tournaments: list[Tournaments] = [
    common_champion,
    # common_veterans,
    common_contender,
    # common_underdog,
    # season_of_giving,
    # common_western_conference,
    # common_eastern_conference,
    # common_no_cap,
    # common_all_offense,
    # common_all_defense,
    # common_under_23,
    # super_rare_underdog,
    # super_rare_contender,
    # super_rare_champion,
    # rare_veterans,
    # rare_champion,
    # rare_contender,
    # rare_underdog,
    # rare_no_cap,
    # limited_champion,
    # limited_all_defense,
    # limited_contender,
    # limited_eastern_conference,
    # limited_under_23,
    # limited_veterans,
    # limited_all_offense,
    # deck_the_halls,
    # limited_western_conference,
    # limited_no_cap,
    # limited_underdog,
]  #  Change the priority of the tournament, the more advanced will be priority card selection

blacklist_cards: list[str] = [
    # "aa3a4968-2d2d-419b-8e5b-85f3fbaae634",  # Brandon Ingram
]  # Set the id that will not be selected, duplicate cards are recommended to set

blacklist_players: list[str] = [
    "Kemba Walker",
]  # Putting players name who do not query here is only valid for recommand mode

recommend_from_teams: list[str] = [
    # "ATL",
    # "DAL",
    # "MEM",
]  # if list is not empty, card recommend from those teams

suggest_cards: dict[str, dict[str, str]] = {
    "common_champion": {},
    "common_contender": {},
    "common_underdog": {},
    "common_western_conference": {},
    "common_eastern_conference": {},
    "common_no_cap": {},
    "super_rare_contender": {
        # "7687d882-b499-4a00-83f1-b16dab40a6fd": "Christian Braun",
        # "abbe6b0a-88c7-4539-ba80-9c41a25b4ce3": "Josh Okogie",
    },
    "rare_contender": {
        # "7687d882-b499-4a00-83f1-b16dab40a6fd": "Christian Braun",
        # "e9bacf6f-f367-46fb-85bd-b6c642c69f51": "Bones Hyland",
        # "26550275-d00e-4a81-8f61-ffbc036ef354": "Zeke Nnaji",
        # "45730281-cbb7-4b83-b824-219bf220c07f": "Terance Mann",
        # "5df4f5e8-7e52-4ee4-96a0-3cffafca2a02": "Buddy Hield",
        # "0087b6e6-c8d5-410e-9bc9-e051d793b6b8": "Jonas Valanciunas",
        # "a694ea01-a530-47c7-af92-ab5a7b97f6a3": "Bennedict Mathurin",
        # "e7237e22-e75f-4a11-8035-42292046aa50": "Cedi Osman",
    },
    "limited_contender": {},
    "super_rare_champion": {},
    "rare_champion": {
        # "5df4f5e8-7e52-4ee4-96a0-3cffafca2a02": "Buddy Hield",
        # "b85c6b5b-8d5f-4eed-84f2-135b273b99e7": "Nikola Joki\u0107",
    },
    "rare_underdog": {
        # "9fc2c2bd-9d3d-4831-a0df-013eff544469": "Bruce Brown",
        # "4cc2790f-6e43-48b1-ac45-d2e75ae1c49b": "Yuta Watanabe",
        # "e7237e22-e75f-4a11-8035-42292046aa50": "Cedi Osman",
        # "62ab6bad-b284-40e4-85da-8af52f870200": "Alondes Williams",
    },
    "super_rare_underdog": {
        # "7ec97d41-27fa-4422-8054-a6ac9780205c": "Vlatko \u010can\u010dar"
    },
    "limited_champion": {
        # "10c74499-37d5-4170-a952-3401588a3f8a": "Nikola Joki\u0107",
        # "6f93a513-5031-4e36-8e06-f922dc00ea3b": "Jayson Tatum",
        # "7ff1a297-9236-4ca5-8295-a7a2b45dd7a1": "Russell Westbrook",
    },
    "limited_western_conference": {},
    "limited_eastern_conference": {},
    "limited_no_cap": {},
    "limited_underdog": {},
    "limited_veterans": {},
}  #  Set the id of cards that will be selected, can find id and name in data/cards-xxxx-xx-xx.json
