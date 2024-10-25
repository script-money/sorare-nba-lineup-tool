from typing import TypedDict, NotRequired
from enum import Enum
from statistics import NormalDist


class NBATeam(TypedDict):
    name: str
    slug: str


class NBAPlayerPosition(Enum):
    g = "basketball_guard"
    f = "basketball_forward"
    c = "basketball_center"


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
    secondsPlayed: int


class DetailedStats(TypedDict):
    detailedStats: DetailedStat
    score: float


class NBAPlayerInFixtureStatus(TypedDict):
    statusIconType: str
    gameStats: list[DetailedStats]


class Fixture(TypedDict):
    gameWeek: int


class NBAPlayerInFixture(TypedDict):
    score: float
    tenGameAverage: int
    fixture: Fixture
    status: NBAPlayerInFixtureStatus


class NBAPlayer(TypedDict):
    displayName: str
    lastFiveSo5Appearances: int
    lastTenSo5Appearances: int
    lastFifteenSo5Appearances: int
    activeClub: NBATeam


class NBACard(TypedDict):
    slug: str
    power: float
    player: NBAPlayer
    rarityTyped: CardRarity
    inSeasonEligible: bool
    addCommonCardPoints: int
    anyPositions: list[NBAPlayerPosition]
    anyPlayer: NBAPlayer


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
    seasonLimit: int | None
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
    injure_type: str
    probility: NotRequired[float]


class SelectCard(TypedDict):
    name: str
    average: int
    age: int
    rarity: CardRarity | None
    expect: NormalDist
    season: str
    minutes: int
    team: str | None
    id: str | None


class MatchProbility(TypedDict):
    Available: float
    Probable: float
    Questionable: float
    Doubtful: float
    Out: float


default_match_probility = {
    "Available": 1.0,
    "Probable": 0.75,
    "Questionable": 0.5,
    "Doubtful": 0.25,
    "Out": 0.0,
}


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

team_in_nba_office_website = [
    "Atlanta Hawks",
    "Boston Celtics",
    "Brooklyn Nets",
    "Charlotte Hornets",
    "Chicago Bulls",
    "Cleveland Cavaliers",
    "Dallas Mavericks",
    "Denver Nuggets",
    "Detroit Pistons",
    "Golden State Warriors",
    "Houston Rockets",
    "Indiana Pacers",
    "LA Clippers",
    "Los Angeles Lakers",
    "Memphis Grizzlies",
    "Miami Heat",
    "Milwaukee Bucks",
    "New Orleans Pelicans",
    "New York Knicks",
    "Oklahoma City Thunder",
    "Orlando Magic",
    "Philadelphia 76ers",
    "Phoenix Suns",
    "Portland Trail Blazers",
    "Sacramento Kings",
    "San Antonio Spurs",
    "Toronto Raptors",
    "Utah Jazz",
    "Washington Wizards",
    "Minnesota Timberwolves",
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
