import requests as rq
from lxml import etree
import json
from utils import rename_player

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

all_players: dict[str, dict[str, str | list[str]]] = {}

for abridge, full_name in source_team_names.items():
    web_name = full_name.replace(" ", "-").lower()
    res = rq.get(
        f"https://www.cbssports.com/nba/teams/{abridge}/{web_name}/depth-chart/"
    )
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    positions_source: list[str] = root.xpath(
        "//tbody/tr[@class='TableBase-bodyTr']/td[1]/text()"
    )
    positions: list[str] = [position.strip() for position in positions_source]
    starters: list[str] = root.xpath(
        "//tbody/tr[@class='TableBase-bodyTr']/td[2]/span[@class='CellPlayerName--long']/span/a/text()"
    )
    starters = [rename_player(starter) for starter in starters]
    seconds: list[str] = root.xpath(
        "//tbody/tr[@class='TableBase-bodyTr']/td[3]/span[@class='CellPlayerName--long']/span/a/text()"
    )
    seconds = [rename_player(second) for second in seconds]
    thirds = []

    thirds_by_position: list[list[str]] = root.xpath(
        "//tbody/tr[@class='TableBase-bodyTr']/td[4]/div[@class='CellPlayerNames']"
    )
    for third_element in thirds_by_position:
        thirds_list: list[str] = third_element.xpath(  # type: ignore
            "div[@class='CellPlayerNames-name']/span[@class='CellPlayerName--long']/span/a/text()"
        )
        thirds_list = [rename_player(third) for third in thirds_list]
        thirds.append(thirds_list)
    players_in_team: dict[str, str | list[str]] = {}
    for i in range(len(positions)):
        players_in_team[positions[i]] = [starters[i], seconds[i], thirds[i]]

    match abridge:
        case "PHO":
            abridge = "PHX"
        case "SA":
            abridge = "SAS"
        case "GS":
            abridge = "GSW"
        case "NY":
            abridge = "NYK"
        case "NO":
            abridge = "NOP"
        case _:
            pass

    all_players[abridge] = players_in_team
    print(f"Query {full_name} players position done.")

# save all_players to json file
with open(f"data/player_positions.json", "w") as f:
    json.dump(all_players, f)
    print("players position saved in data folder")
