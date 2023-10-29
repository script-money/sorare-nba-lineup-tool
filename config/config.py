from types_ import Tournaments, CardRarity, NBAConference

use_proxy = False
proxies = (
    {"http": "http://127.0.0.1:7890", "https": "http://127.0.0.1:7890"}
    if use_proxy
    else None
)

pickup: Tournaments = {
    "name": "pickup",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.common],
    "minRarity": None,
    "target": 260,  # target can be set according to the prize pool target, if the target is too high, it will tend to pick players with more inconsistent performance
}

street_ball: Tournaments = {
    "name": "street_ball",
    "tenGameAverageTotalLimit": 0,
    "allowMVP": False,
    "allowedConference": None,
    "allowedRarities": [
        CardRarity.common,
        CardRarity.limited,
        CardRarity.rare,
        CardRarity.super_rare,
        CardRarity.unique,
    ],
    "minRarity": None,
    "target": 300,
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
    "target": 260,
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
    "target": 200,
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
    "target": 160,
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
    "target": 260,
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
    "target": 245,
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
    "target": 190,
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
    "target": 295,
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
    "target": 125,
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
    "target": 210,
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
    "target": 210,
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
    "target": 230,
}

limited_veterans: Tournaments = {
    "name": "limited_veterans",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.limited],
    "minRarity": None,
    "target": 230,
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
    "target": 150,
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
    "target": 225,
}

rare_under_23: Tournaments = {
    "name": "rare_under_23",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": None,
    "target": 225,
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

super_rare_under_23: Tournaments = {
    "name": "super_rare_under_23",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": None,
    "target": 245,
}

super_rare_eastern_conference: Tournaments = {
    "name": "super_rare_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.east,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.super_rare,
    },
    "target": 255,
}

super_rare_western_conference: Tournaments = {
    "name": "super_rare_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.west,
    "allowedRarities": [CardRarity.super_rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.super_rare,
    },
    "target": 255,
}

rare_eastern_conference: Tournaments = {
    "name": "rare_eastern_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.east,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 250,
}

rare_western_conference: Tournaments = {
    "name": "rare_western_conference",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": NBAConference.west,
    "allowedRarities": [CardRarity.rare],
    "minRarity": {
        "minCount": 5,
        "rarity": CardRarity.rare,
    },
    "target": 250,
}

rare_all_offense: Tournaments = {
    "name": "rare_all_offense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": None,
    "target": 230,
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

rare_all_defense: Tournaments = {
    "name": "rare_all_defense",
    "tenGameAverageTotalLimit": 120,
    "allowMVP": True,
    "allowedConference": None,
    "allowedRarities": [CardRarity.rare],
    "minRarity": None,
    "target": 130,
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

# Player performance a normal distribution, mu is the average value of the distribution, for example, player rating 30, mu = 0.1, then the expected average value of performance is 33
# The mu additions (or reductions) set below are empirical values and are not guaranteed to be 100% accurate, so you can fine-tune them yourself
compute_by_recent_n_weeks_games: int = (
    1  # Calculate the rate of change in performance for the last n weeks of play
)
mu_of_max_rank_team_bonus_ratio: float = 0  # If the opponent is the weakest team in offense and defense, the maximum addition to the average value of performance change rate, and vice versa playing strong teams cut
mu_of_home_bonus: float = (
    0.1  # Home additions to the mean rate of change in performance
)
mu_of_b2b: float = (
    -0.15
)  # Deductions for mean change in home playing back-to-back performance
mu_of_main_player_in_high_value_game: float = 0.1
mu_of_reserve_player_in_low_value_game: float = 0.3

mu_of_single_game_bonus: float = (
    -0.1  # Deductions for average single-game performance change only
)
mu_of_multiple_games_bonus: float = (
    0.1  # of performance change averages for games played 3 or more
)
outperform_treshold: float = (
    -3  # include players who average - outperform more than this value
)
exclude_game_weeks = [35, 48]  # Exclude the game weeks (such as all_star_week)
show_top_10_outperform = True
suggestion_count: int = 3  # Number of recommended results
probability_reach_target: float = 0.01  # Sort from the results that have that probability of reaching the target score
show_injure_detail = False
target_adjust = 0  # if target_adjust is 10, all Tournaments targets will add 10, 0 for minimum number of matches. Suggestion: 0 for weekend, 5 for weekday, 20-30 for T3
is_game_decision_bonus_activate = (
    False  # Whether to activate the bonus for the game decision
)
inPlayoff = False

all_tournaments: list[Tournaments] = [
    pickup,
    # common_veterans,
    # common_underdog,
    # common_western_conference,
    # common_eastern_conference,
    # common_no_cap,
    # common_all_offense,
    # common_all_defense,
    # common_under_23,
    # limited_eastern_conference,
    # limited_western_conference,
    # limited_under_23,
    # limited_veterans,
    # limited_all_offense,
    # limited_all_defense,
    # limited_champion,
    # limited_contender,
    # limited_underdog,
    # limited_no_cap,
    # rare_eastern_conference,
    # rare_western_conference,
    # rare_no_cap,
    # rare_under_23,
    # rare_veterans,
    # rare_all_offense,
    # rare_all_defense,
    # rare_champion,
    # rare_contender,
    # rare_underdog,
    # super_rare_eastern_conference,
    # super_rare_western_conference,
    # super_rare_champion,
    # super_rare_contender,
    # super_rare_underdog,
    # super_rare_under_23,
    # deck_the_halls,
    # season_of_giving,
    # street_ball,
]  #  Change the priority of the tournament, the more advanced will be priority card selection

blacklist_cards: list[str] = [
    # "aa3a4968-2d2d-419b-8e5b-85f3fbaae634",  # Brandon Ingram
    # "3a228b27-9745-4f8e-b5f7-892394942f85",  # Trey Murphy III
    # "1c3587a2-4ef4-4f74-a109-980be7381be8",  # Joel Embiid
    # "438a6b0d-f352-4693-a757-b540d5d4ec69",  # Patrick Beverley
    # "612a02fd-25d8-4cf2-916c-24da947ef8b3",  # jjj
    # "25239483-2190-4594-a5c5-79f45dbcb30e",  # claxton
    # "eca889fc-72a5-4800-8341-4724ae39990c",  # jb
    # "3123a3b9-18c0-4f59-8a8f-15c32bde7d11",  # jjj
    # "6d5a968f-72d6-423d-a1b1-7211fcc6c5c0",  # claxton
    # "dec7ed75-bed1-4506-9ed9-86474b955d05",  # mcbride
    # "1d06fe80-c8ee-47cc-8ce1-add192fc951b",  # Lindy Waters III
    # "fc970e85-84cb-4a15-b7f7-08098d0dd9b6"  # Lamar Stevens
    # "48072d8e-ea46-4d4b-8bec-d613916aa991",  # Trae Young
    # "dd178ee5-e8e6-46d3-be07-39cf26314869",  # Kawhi Leonard
]  # Set the id that will not be selected, duplicate cards are recommended to set

blacklist_players: list[str] = [
    "Kemba Walker",
    "Skylar Mays",
    "Jay Huff",
    "Justin Minaya",
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
        # "da82a46b-3265-4861-958f-5d13da220269": "Bruce Brown",
        # "abbe6b0a-88c7-4539-ba80-9c41a25b4ce3": "Josh Okogie",
    },
    "limited_contender": {},
    "super_rare_champion": {
        # "48072d8e-ea46-4d4b-8bec-d613916aa991": "Trae Young",
        # "da82a46b-3265-4861-958f-5d13da220269": "Bruce Brown",
        # "abbe6b0a-88c7-4539-ba80-9c41a25b4ce3": "Josh Okogie"
        # "066a2859-0127-4481-860e-9f205203626d": "Brook Lopez"
        # "c016853c-1772-412f-b681-91f3ac74fd3f": "Jimmy Butler",
        # "aa3a4968-2d2d-419b-8e5b-85f3fbaae634": "Brandon Ingram",
    },
    "rare_champion": {
        # "f1464116-cdfc-42d1-aa03-16d360c5e3cd": "Nikola Joki\u0107",
        # "b29c6fed-4679-4476-8069-e79763b9f48a": "Cade Cunningham",
    },
    "rare_contender": {
        # "e1bb9b58-429d-40ef-98d9-5a571f8a6a2c": "Cade Cunningham",
        # "7687d882-b499-4a00-83f1-b16dab40a6fd": "Christian Braun",
    },
    "rare_underdog": {
        # "9fc2c2bd-9d3d-4831-a0df-013eff544469": "Bruce Brown",
        # "4cc2790f-6e43-48b1-ac45-d2e75ae1c49b": "Yuta Watanabe",
        # "e7237e22-e75f-4a11-8035-42292046aa50": "Cedi Osman",
        # "c830ad34-aa43-4b39-b0aa-b695d616bf5c": "Bryce McGowens",
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
    "limited_all_offense": {
        # "cdc65dd7-ee7b-4e81-978a-33f884d334ae": "Trae Young"
    },
    # "rare_all_defense": {"fad9b50e-4c35-4631-bcf6-3db5565553ca": "Andre Drummond"},
}  #  Set the id of cards that will be selected, can find id and name in data/cards-xxxx-xx-xx.json
