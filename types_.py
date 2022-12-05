from typing import TypedDict
from enum import Enum
from statistics import NormalDist


class NBATeam(TypedDict):
    fullName: str


class NBAPlayerPosition(Enum):
    g = "NBA_GUARD"
    f = "NBA_FORWARD"
    c = "NBA_CENTER"


class PlayerInFixtureStatusIconType(Enum):
    final_score = "FINAL_SCORE"
    in_progress_score = "IN_PROGRESS_SCORE"
    pending = "PENDING"
    no_game = "NO_GAME"
    did_not_play = "DID_NOT_PLAY"
    inactive = "INACTIVE"


class NBAConference(Enum):
    east = "EASTERN"
    west = "WESTERN"


class CardRarity(Enum):
    unique = "unique"
    super_rare = "super_rare"
    rare = "rare"
    limited = "limited"
    common = "common"


class NBAGame(TypedDict):
    startDate: str
    homeTeam: NBATeam
    awayTeam: NBATeam
    homeScore: int
    awayScore: int


class NBAPlayerInFixtureStatus(TypedDict):
    statusIconType: str


class NBAPlayerInFixture(TypedDict):
    score: float
    tenGameAverage: int
    status: NBAPlayerInFixtureStatus


class NBAPlayer(TypedDict):
    displayName: str
    tenGameAverage: int
    positions: list[str]
    latestFinalFixtureStats: list[NBAPlayerInFixture]


class NBACard(TypedDict):
    id: str
    slug: str
    totalBonus: float
    team: NBATeam
    player: NBAPlayer
    rarity: CardRarity


class LeaderboardRulesMinimumRarityRequirement(TypedDict):
    minCount: int
    rarity: CardRarity


class Tournaments(TypedDict):
    name: str
    tenGameAverageTotalLimit: int
    allowMVP: bool
    allowedConference: NBAConference | None
    allowedRarities: list[CardRarity]
    minRarity: LeaderboardRulesMinimumRarityRequirement | None
    target: int


class Match(TypedDict):
    date: str
    away: str
    away_is_b2b: bool
    home: str
    home_is_b2b: bool


class TeamRank(TypedDict):
    team_offense_rank: list[str]
    team_defense_rank: list[str]


class Injure(TypedDict):
    team: str
    player: str
    position: NBAPlayerPosition
    game_time_decision: bool


class SelectCard(TypedDict):
    name: str
    average: int
    rarity: CardRarity
    expect: NormalDist
    team: str
    id: str


western_teams: list[str] = [
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
    "LA Clippers",
]
