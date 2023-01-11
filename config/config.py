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

# Player performance a normal distribution, mu is the average value of the distribution, for example, player rating 30, mu = 0.1, then the expected average value of performance is 33
# The mu additions (or reductions) set below are empirical values and are not guaranteed to be 100% accurate, so you can fine-tune them yourself
compute_by_recent_n_weeks_games: int = (
    10  # Calculate the rate of change in performance for the last n weeks of play
)
mu_of_game_decision: float = (
    -0.1
)  # Injury report inside game_decision may or may not play, the performance rate of change of the average value plus the negative value
mu_of_max_rank_team_bonus_ratio: float = 0.2  # If the opponent is the weakest team in offense and defense, the maximum addition to the average value of performance change rate, and vice versa playing strong teams cut
mu_of_home_bonus: float = (
    0.04  # Home additions to the mean rate of change in performance
)
mu_of_home_b2b: float = (
    -0.01
)  # Deductions for mean change in home playing back-to-back performance
mu_of_away_b2b: float = (
    -0.02
)  # Deductions for mean change in away playing back-to-back performance
mu_of_single_game_bonus: float = (
    -0.2
)  # Deductions for average single-game performance change only
mu_of_multiple_games_bonus: float = (
    0.15  # of performance change averages for games played 3 or more
)
suggestion_count: int = 3  # Number of recommended results
probability_reach_target: float = 0.01  # Sort from the results that have that probability of reaching the target score

all_tournaments: list[Tournaments] = [
    common_champion,
    # season_of_giving,
    common_contender,
    # common_underdog,
    # common_western_conference,
    # common_eastern_conference,
    # common_no_cap,
    # common_all_offense,
    # common_all_defense,
    # common_veterans,
    common_under_23,
    super_rare_contender,
    rare_champion,
    rare_contender,
    # limited_all_defense,
    limited_champion,
    limited_contender,
    # limited_under_23,
    limited_veterans,
    # limited_all_offense,
    # deck_the_halls,
    super_rare_champion,
    # limited_western_conference,
    # limited_eastern_conference,
    # limited_no_cap,
    # limited_underdog,
]  #  Change the priority of the tournament, the more advanced will be priority card selection

blacklist_cards: list[str] = [
    # "dbb7d8a8-4a7d-4097-b8b7-77f4faed2350",  # Sam Hauser
    # "839244ed-a59c-4b46-b13b-b124b49a8038",  # Kevin Huerter
    # "aa34b029-d04c-43de-8b3f-9f5ea58814dd",  # Kevin Huerter
    # "9754710e-0cea-4372-8d41-743781ca3ffb",  # Kevin Huerter
    # "aa3a4968-2d2d-419b-8e5b-85f3fbaae634",  # Brandon Ingram
    # "a6cca7ff-4832-4a1e-887d-35216e2c310e",  # Paul Reed
    # "ca553b45-5402-4541-a032-a6578da8c200",  # Eugene Omoruyi
]  # Set the id that will not be selected, duplicate cards are recommended to set

blacklist_players: list[str] = [
    "Kemba Walker",
]  # Putting players name who do not query here is only valid for recommand mode

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
        # "a3c70a48-c949-42e2-8c3c-8424679d6bcf": "Andre Drummond",
        # "3b9c8713-2e0d-4fcc-89e5-2c3c892e24e8": "Trendon Watford",
        # "48072d8e-ea46-4d4b-8bec-d613916aa991": "Trae Young",
        # "ca553b45-5402-4541-a032-a6578da8c200": "Eugene Omoruyi",
    },
    "rare_contender": {},
    "limited_contender": {},
    "super_rare_champion": {},
    "rare_champion": {
        # "3a4425d7-06f6-4382-86fc-ac29baadf125": "Ja Morant",
        # "ccacb679-5d6a-4539-b6d6-5392e4b39edf": "Giannis Antetokounmpo",
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
}  #  Set the id of cards that will be selected, can find id and name in data/cards-xxxx-xx-xx.json
