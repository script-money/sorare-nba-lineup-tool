from typing import TypedDict, NotRequired
from enum import Enum
from statistics import NormalDist


class NBATeam(TypedDict):
    fullName: str
    abbreviation: str


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


class DetailedStat(TypedDict):
    points: int
    rebounds: int
    assists: int
    blocks: int
    steals: int
    turnovers: int
    made3PointFGs: int
    doubleDoubles: int
    tripleDoubles: int
    minutes: str


class DetailedStats(TypedDict):
    detailedStats: DetailedStat


class NBAPlayerInFixtureStatus(TypedDict):
    statusIconType: str
    gameStats: list[DetailedStats]


class NBAPlayerInFixture(TypedDict):
    score: float
    tenGameAverage: int
    status: NBAPlayerInFixtureStatus


class NBAPlayer(TypedDict):
    displayName: str
    tenGameAverage: int
    age: int
    positions: list[str]
    latestFinalFixtureStats: list[NBAPlayerInFixture]
    team: NBATeam


class NBACard(TypedDict):
    id: str
    slug: str
    totalBonus: float
    player: NBAPlayer
    rarity: CardRarity


class NBACardsRes(TypedDict):
    nbaCards: list[NBACard]


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
    multiplier: NotRequired[dict[str, float]]


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
    age: int
    rarity: CardRarity | None
    expect: NormalDist
    team: str
    id: str | None


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

source_team_names: dict[str, str] = {
    "BOS": "Boston Celtics",
    "BKN": "Brooklyn Nets",
    "NY": "New York Knicks",
    "PHI": "Philadelphia 76ers",
    "TOR": "Toronto Raptors",
    "CHI": "Chicago Bulls",
    "CLE": "Cleveland Cavaliers",
    "DET": "Detroit Pistons",
    "IND": "Indiana Pacers",
    "MIL": "Milwaukee Bucks",
    "ATL": "Atlanta Hawks",
    "CHA": "Charlotte Hornets",
    "MIA": "Miami Heat",
    "ORL": "Orlando Magic",
    "WAS": "Washington Wizards",
    "DEN": "Denver Nuggets",
    "MIN": "Minnesota Timberwolves",
    "OKC": "Oklahoma City Thunder",
    "POR": "Portland Trail Blazers",
    "UTA": "Utah Jazz",
    "GS": "Golden State Warriors",
    "LAC": "Los Angeles Clippers",
    "LAL": "Los Angeles Lakers",
    "PHO": "Phoenix Suns",
    "SAC": "Sacramento Kings",
    "DAL": "Dallas Mavericks",
    "HOU": "Houston Rockets",
    "MEM": "Memphis Grizzlies",
    "NO": "New Orleans Pelicans",
    "SA": "San Antonio Spurs",
}

team_slugs = [
    "brooklyn-nets",
    "indiana-pacers",
    "cleveland-cavaliers",
    "toronto-raptors",
    "phoenix-suns",
    "portland-trail-blazers",
    "detroit-pistons",
    "orlando-magic",
    "la-clippers",
    "boston-celtics",
    "memphis-grizzlies",
    "oklahoma-city-thunder",
    "dallas-mavericks",
    "minnesota-timberwolves",
    "houston-rockets",
    "utah-jazz",
    "los-angeles-lakers",
    "denver-nuggets",
    "chicago-bulls",
    "san-antonio-spurs",
    "sacramento-kings",
    "miami-heat",
    "golden-state-warriors",
    "new-york-knicks",
    "new-orleans-pelicans",
    "washington-wizards",
    "atlanta-hawks",
    "milwaukee-bucks",
    "philadelphia-76ers",
    "charlotte-hornets",
]
