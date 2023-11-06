import requests as rq
from lxml import etree
from pytz import timezone
from datetime import datetime, timedelta, date
import json
import time
from config.config import proxies, cookies

from types_ import NBAPlayerPosition
from utils import rename_player
from get_injure import query_last_injury_report
import pandas as pd
import os
from config.config import inPlayoff


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
    return (
        stash_name.split("/")[4]
        .replace("-", " ")
        .title()
        .replace("76Ers", "76ers")
        .replace("Los Angeles Clippers", "LA Clippers")
    )


def get_injure_data():
    injured_data = []
    res = rq.get(
        "https://www.cbssports.com/nba/injuries/daily/",
        headers={"cookies": cookies},
        proxies=proxies,
    )
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root.xpath('//tr[@class="TableBase-bodyTr"]'):
        team = stash_team_rename(
            element.xpath('./td[1]//span[@class="TeamName"]/a/@href')[0]
        )

        player = rename_player(
            element.xpath('./td[2]/span[@class="CellPlayerName--long"]//a/text()')[0]
        )

        position = element.xpath("./td[3]/text()")[0].strip()
        status_text = element.xpath("./td[5]/text()")[0].strip()
        status = (
            False
            if "Expected to be out" in status_text
            or status_text == "Out for the season"
            else True
        )
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

    with open(f"data/injure-0.json", "w") as f:
        json.dump(injured_data, f, indent=4)

    return injured_data


def get_correct_name(series):
    try:
        name = series[-1]
        first = series[-1:]
        return rename_player(name + " " + first)
    except ValueError:
        print("Rename error:", series)
        return series


def get_injure_data_new():
    # from_str = (today - timedelta(days=0)).strftime("%Y-%m-%d")
    # df = extarct_official_injury_report(from_str, today_str)
    df = query_last_injury_report()
    print(df.to_string())
    # remove duplicate by Player Name
    df = df.drop_duplicates(subset=["Player Name"], keep="last")
    df["team"] = df["Team"]
    df["player"] = df["Player Name"]
    df["injure_type"] = df["Current Status"]
    df = df[["team", "player", "injure_type"]]
    df.to_json(f"data/injure-1.json", orient="records")


def combine_two_type_injure_json():
    today = datetime.now(timezone("US/Eastern"))
    today_str = today.strftime("%Y-%m-%d")
    # read json as dataframe
    df0 = pd.read_json(f"data/injure-0.json")
    df1 = pd.read_json(f"data/injure-1.json")
    # join df0 and df1 with key='player'
    df = df0.merge(df1, on=["team", "player"], how="outer")
    # fill na cell in injure_type to Out if game_time_decision is False and to Questionable if game_time_decision is True
    df["injure_type"] = df["injure_type"].fillna(  # type: ignore
        df["game_time_decision"].apply(
            lambda x: "Out" if x == False else "Questionable"
        )
    )
    # select column team,player,injure_type
    df = df[["team", "player", "injure_type"]]
    # save to json
    df.to_json(f"data/injure-{today_str}.json", orient="records", indent=4)
    print(f"save injure info to data/injure-{today_str}.json")
    # delete old json
    os.remove(f"data/injure-0.json")
    os.remove(f"data/injure-1.json")


def get_next_epoch_schedule(specific_date=None) -> list[MatchData]:
    match_data: list[MatchData] = []
    next_days: list[str] = []
    today = (
        datetime.now(timezone("US/Eastern")) if specific_date == None else specific_date
    )
    today_str = today.strftime("%Y-%m-%d")

    if not inPlayoff:
        weekday = today.weekday()

        if weekday in [1, 2, 3, 4]:
            days_to_add = [3 - weekday, 4 - weekday, 5 - weekday, 6 - weekday]
            next_days = [
                (today + timedelta(days=i)).strftime("%Y%m%d") for i in days_to_add
            ]
        elif weekday in [5, 6, 0]:
            days_to_add = [
                -1 - weekday,
                -weekday,
                1 - weekday,
                2 - weekday,
                3 - weekday,
            ]
            next_days = [
                (today + timedelta(days=i)).strftime("%Y%m%d")
                if i >= 0
                else (today + timedelta(days=i + 7)).strftime("%Y%m%d")
                for i in days_to_add
            ]
    else:
        weeks = [
            ("20230411", "20230416"),
            ("20230417", "20230423"),
            ("20230424", "20230430"),
            ("20230501", "20230507"),
            ("20230508", "20230514"),
            ("20230515", "20230521"),
            ("20230522", "20230529"),
            ("20230601", "20230618"),
        ]
        today_date = today.date()
        for start_date_str, end_date_str in reversed(weeks):
            start_date = datetime.strptime(start_date_str, "%Y%m%d").date()
            end_date = datetime.strptime(end_date_str, "%Y%m%d").date()

            if start_date >= today_date:
                current_date = start_date
                dates_in_week = []
                while current_date <= end_date:
                    dates_in_week.append(current_date.strftime("%Y%m%d"))
                    current_date += timedelta(days=1)
                next_days = dates_in_week
        if len(next_days) == 0:
            assert False, "No next days found"

    if len(next_days) == 0:
        print("No next days found")
        exit(0)
    for day in next_days:
        _date = datetime.strptime(day, "%Y%m%d").date()
        res = rq.get(
            f"https://www.cbssports.com/nba/schedule/{day}/",
            headers={"cookies": cookies},
            proxies=proxies,
        )
        root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
        if root is None:
            print(f"Can't get data from cbssports, proxies is {proxies}")
            exit(0)
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

    matches_mark_b2b: list[MatchData] = []
    for match in match_data:
        if match.away == "" and match.home == "":
            continue

        away, home = match.away, match.home

        yesterday = match.date - timedelta(days=1)
        away_has_b2b_last_matches: list[MatchData] = list(
            filter(
                lambda i: i.date == yesterday and (away == i.away or away == i.home),
                match_data,
            )
        )
        home_has_b2b_last_matches: list[MatchData] = list(
            filter(
                lambda i: i.date == yesterday and (home == i.home or home == i.away),
                match_data,
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

    match_exclude_first_day = matches_mark_b2b
    if not inPlayoff:
        match_exclude_first_day = list(
            filter(lambda m: m.date != match_data[0].date, match_data)
        )  # filter out the first day for b2b computation

    match_output_json = []
    for match in match_exclude_first_day:
        match_output_json.append(match.__dict__())
    with open(f"data/next-week-{today_str}.json", "w") as f:
        json.dump(match_output_json, f, indent=4)
        print("next week matches saved in data folder")
    return matches_mark_b2b


def get_team_rank():
    teams = {}
    offense = []
    res = rq.get(
        "https://www.cbssports.com/nba/stats/team/team/scoring/nba/regular/",
        headers={"cookies": cookies},
        proxies=proxies,
    )
    if res.status_code == 200:
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
            "https://www.cbssports.com/nba/stats/team/opponent/scoring/nba/regular/",
            headers={"cookies": cookies},
            proxies=proxies,
        )

        root2 = etree.HTML(res2.text, parser=etree.HTMLParser(encoding="utf-8"))
        for element in root2.xpath('//tr[@class="TableBase-bodyTr"]'):
            team = stash_team_rename(
                element.xpath('./td[1]//span[@class="TeamName"]/a/@href')[0]
            )
            defense.append(team)
        teams["team_defense_rank"] = defense

        with open(f"data/team-rank.json", "w") as f:
            json.dump(teams, f, indent=4)
            print("team rank saved in data folder")
        return teams
    else:
        print(f"Can't get team rank from cbssports, status is {res.status_code}")
        exit(0)


if __name__ == "__main__":
    get_next_epoch_schedule()
    get_injure_data()
    get_injure_data_new()
    combine_two_type_injure_json()
    get_team_rank()
