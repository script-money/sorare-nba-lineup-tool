import requests as rq
from lxml import etree
from pytz import timezone
from datetime import datetime, timedelta, date
import json
import time
from types_ import NBAPlayerPosition


class MatchData:
    def __init__(self, date: date, away: str, home: str):
        self.date = date
        self.away = away
        self.away_is_b2b = False
        self.home = home
        self.home_is_b2b = False

    def mark_away_b2b(self):
        self.away_is_b2b = True

    def mark_home_b2b(self):
        self.home_is_b2b = True

    def last_day(self):
        return self.date - timedelta(days=1)

    def __str__(self):
        return f"{self.date} {self.away}{'(BTB)' if self.away_is_b2b else ''} vs {self.home}{'(BTB)' if self.home_is_b2b else ''}"

    def __dict__(self):
        return {
            "date": self.date.strftime("%Y%m%d"),
            "away": self.away,
            "away_is_b2b": self.away_is_b2b,
            "home": self.home,
            "home_is_b2b": self.home_is_b2b,
        }


def stash_team_rename(
    stash_name,
):  # /nba/teams/MIN/minnesota-timberwolves/ to Minnesota Timberwolves
    return stash_name.split("/")[4].replace("-", " ").title().replace("76Ers", "76ers")


def get_injure_data():
    injured_data = []
    res = rq.get("https://www.cbssports.com/nba/injuries/daily/")
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root.xpath('//tr[@class="TableBase-bodyTr"]'):
        team = stash_team_rename(
            element.xpath('./td[1]//span[@class="TeamName"]/a/@href')[0]
        )

        player = element.xpath('./td[2]/span[@class="CellPlayerName--long"]//a/text()')[
            0
        ].replace("Nah'Shon Hyland", "Bones Hyland")

        position = element.xpath("./td[3]/text()")[0].strip()
        status_text = element.xpath("./td[5]/text()")[0].strip()
        status = False if "Expected to be out" in status_text else True
        format_position: NBAPlayerPosition = NBAPlayerPosition.g
        if position == "SF" or position == "PF":
            format_position: NBAPlayerPosition = NBAPlayerPosition.f
        if position == "C":
            format_position: NBAPlayerPosition = NBAPlayerPosition.c
        injured_data.append(
            {
                "team": team,
                "player": player,
                "position": format_position.value,
                "game_time_decision": status,
            }
        )

    today = datetime.now(timezone("US/Eastern"))
    today_str = today.strftime("%Y-%m-%d")
    with open(f"data/injure-{today_str}.json", "w") as f:
        json.dump(injured_data, f)
        print("injure saved in data folder")

    return injured_data


def get_next_epoch_schedule(specific_date=None) -> list[MatchData]:
    match_data: list[MatchData] = []
    today = (
        datetime.now(timezone("US/Eastern")) if specific_date == None else specific_date
    )
    today_str = today.strftime("%Y-%m-%d")
    next_days: list[str] = []
    weekday = today.weekday()
    if weekday <= 4 and weekday >= 1:  # upper week 1-4
        offset = -1 if weekday == 4 else 3 - weekday
        next_days.append((today + timedelta(days=offset)).strftime("%Y%m%d"))
        for i in range(3):
            next_days.append(
                (today + timedelta(days=i + offset + 1)).strftime("%Y%m%d")
            )
    else:  # lower week
        offset = -1 if weekday == 0 else 7 - weekday
        next_days.append((today + timedelta(days=offset)).strftime("%Y%m%d"))
        for i in range(4):
            next_days.append(
                (today + timedelta(days=i + offset + 1)).strftime("%Y%m%d")
            )

    for day in next_days:
        _date = datetime.strptime(day, "%Y%m%d").date()
        res = rq.get(f"https://www.cbssports.com/nba/schedule/{day}/")
        root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
        table = root.xpath('//tr[@class="TableBase-bodyTr"]')
        if len(table) == 0:
            match_data.append(MatchData(_date, "", ""))
            continue
        for match in table:
            away = stash_team_rename(
                match.xpath(
                    './td[1]//div[@class="TeamLogoNameLockup-nameContainer"]//a/@href'
                )[0]
            )
            home = stash_team_rename(
                match.xpath(
                    './td[2]//div[@class="TeamLogoNameLockup-nameContainer"]//a/@href'
                )[0]
            )
            match_data.append(MatchData(_date, away, home))

    match_exclude_first_day = list(
        filter(lambda m: m.date != match_data[0].date, match_data)
    )  # filter out the first day

    matches_mark_b2b: list[MatchData] = []
    for match in match_exclude_first_day:
        away, home = match.away, match.home

        yesterday = match.date - timedelta(days=1)
        away_has_b2b_last_matches: list[MatchData] = list(
            filter(
                lambda i: i.date == yesterday and (away == i.away or away == i.home),
                match_exclude_first_day,
            )
        )
        home_has_b2b_last_matches: list[MatchData] = list(
            filter(
                lambda i: i.date == yesterday and (home == i.home or home == i.away),
                match_exclude_first_day,
            )
        )

        if len(away_has_b2b_last_matches) == 0 and len(home_has_b2b_last_matches) == 0:
            matches_mark_b2b.append(match)
            continue

        if len(away_has_b2b_last_matches) != 0:
            match.mark_away_b2b()
            matches_mark_b2b.append(match)

        if len(home_has_b2b_last_matches) != 0:
            match.mark_home_b2b()
            if match in matches_mark_b2b:
                continue
            matches_mark_b2b.append(match)

    match_output_json = []
    for match in matches_mark_b2b:
        match_output_json.append(match.__dict__())
    with open(f"data/next-week-{today_str}.json", "w") as f:
        json.dump(match_output_json, f)
        print("next week matches saved in data folder")
    return matches_mark_b2b


def get_team_rank():
    teams = {}
    offense = []
    res = rq.get("https://www.cbssports.com/nba/stats/team/team/scoring/nba/regular/")
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root.xpath('//tr[@class="TableBase-bodyTr"]'):
        team = stash_team_rename(
            element.xpath('./td[1]//span[@class="TeamName"]/a/@href')[0]
        )
        offense.append(team)
    teams["team_offense_rank"] = offense
    time.sleep(1)

    defense = []
    res2 = rq.get(
        "https://www.cbssports.com/nba/stats/team/opponent/scoring/nba/regular/"
    )
    root2 = etree.HTML(res2.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root2.xpath('//tr[@class="TableBase-bodyTr"]'):
        team = stash_team_rename(
            element.xpath('./td[1]//span[@class="TeamName"]/a/@href')[0]
        )
        defense.append(team)
    teams["team_defense_rank"] = defense
    today = datetime.now(timezone("US/Eastern"))
    today_str = today.strftime("%Y-%m-%d")
    with open(f"data/team-rank-{today_str}.json", "w") as f:
        json.dump(teams, f)
        print("team rank saved in data folder")
    return teams


if __name__ == "__main__":
    get_next_epoch_schedule()
    get_injure_data()
    get_team_rank()
