import numpy as np
import pandas as pd
import tabula
import datetime
import time
import re
import requests as rq
from lxml import etree


# check if a cell belongs to the "Category" column
def category_pattern(val):
    return val in [
        "Injury/Illness",
        "Not With Team",
        "G League Team",
        "G League - Two-Way",
        "G League - On Assignment",
        "Personal Reasons",
        "League Suspension",
        "NOT YET SUBMITTED",
        "Coach's Decision",
        "Trade Pending",
        "Rest",
    ]


# check if a cell belongs to the "Status" column
def reason_pattern(val):
    return val in ["Out", "Doubtful", "Questionable", "Available", "Probable"]


team = [
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


# check if a cell belongs to the "Team" column by building a list of all NBA teams
def teams_pattern(val):
    return val in team


# check if a cell belongs to the "Current Status" column
def current_stat_pattern(val):
    return val in ["Out", "Doubtful", "Questionable", "Available", "Probable"]


# a function that matches each column to it's pattern
def shift_by_pattern(cell, col):  # function that check patterns
    pattern = None

    if col == "Game Date":
        date_pattern = "[0-9]{1,2}/[0-9]{1,2}/[0-9]{4}"
        pattern = re.match(date_pattern, cell)

    if col == "Game Time":
        pattern = "(ET)" in cell

    if col == "Matchup":
        pattern = "@" in cell

    if col == "Team":
        pattern = teams_pattern(cell)

    if col == "Player Name":
        pattern = ", " in cell

    if col == "Category":
        pattern = category_pattern(cell)

    if col == "Reason":
        pattern = reason_pattern(cell)

    if col == "Current Status":
        pattern = current_stat_pattern(cell)

    return pattern


def days_between(d1, d2):
    """
    a function that calculate the difference between two dates
    :param d1: string - string, format: ("%Y-%m-%d")
    :param d2: string - string, format: ("%Y-%m-%d")
    :return: int - the difference between the two dates
    """
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d").date()
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d").date()
    return abs((d2 - d1).days)


def query_last_injury_report():
    last_link = ""
    res = rq.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    if res.status_code != 200:
        raise ValueError(
            "Error in getting the link to the last injury report, please try again later"
        )
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root.xpath('//div[@class="col-xs-12 post-injury"]//a/@href'):
        last_link = element

    print(f"query injure report from {last_link}")
    return combine_injury_report_page(last_link)


def is_team_in_string(input_string, team_list):
    if pd.isna(input_string):
        return False
    matched_team = next((team for team in team_list if team in input_string), np.nan)
    return matched_team


def extract_team(value):
    if is_team_in_string(value, team) != np.nan:
        return is_team_in_string(value, team)
    else:
        return np.nan


def extract_name(value):
    if pd.isna(value):
        return value
    team_or_nan = is_team_in_string(value, team)
    if team_or_nan is not np.nan:
        name_array = value.replace(team_or_nan, "").strip().split(" ")[:-1]
    else:
        name_array = value.split(" ")[:-1]
    if len(name_array) == 0:
        return np.nan
    family_name = name_array[-1]
    given_name = " ".join(name_array[:-1])
    return f"{family_name}, {given_name}".replace(",", "")


def combine_injury_report_page(
    last_link,
):
    df_7col = pd.DataFrame()
    df_lst = tabula.read_pdf(last_link, pages="all", guess=False)  # type: ignore
    for df in df_lst:
        if df.shape[1] == 5:
            # remove columns and use first row as header
            df.columns = [
                "Game Date",
                "Game Time",
                "Matchup",
                "Team Player Name Current Status",
                "Reason",
            ]
            if df.iloc[0, 0] == "Game Date":
                df = df.drop(df.index[0])
            df["Team"] = df["Team Player Name Current Status"].apply(extract_team)

            df["Player Name"] = df["Team Player Name Current Status"].apply(
                extract_name
            )
            df["Current Status"] = df["Team Player Name Current Status"].apply(
                lambda x: x.split(" ")[-1] if pd.isna(x) == False else x
            )

            df.drop(columns=["Team Player Name Current Status", "Reason"], inplace=True)
            df_copy = df.copy()
            df = df_copy.drop(df_copy.tail(1).index)
            # 删除Player Name为NaN的行
            df.dropna(subset=["Player Name"], inplace=True)
            # print(df.to_string())
            # print("\n")
        if df.shape[1] == 4:
            # 如果第0行的最后一个是"NOT YET SUBMITTED"
            if df.iloc[0, -1] == "NOT YET SUBMITTED":
                # for not submit yet
                df.columns = ["Game Time", "Matchup", "Team", "Current Status"]
                df["Game Date"] = np.nan
                df["Player Name"] = np.nan
                # resort columns
                df = df[
                    [
                        "Game Date",
                        "Game Time",
                        "Matchup",
                        "Team",
                        "Player Name",
                        "Current Status",
                    ]
                ]
                df_copy = df.copy()
                df = df_copy.drop(df_copy.tail(1).index)
            else:
                # for normal
                df.columns = [
                    "Game Time",
                    "Matchup",
                    "Team Player Name Current Status",
                    "Reason",
                ]
                df["Game Date"] = np.nan
                df["Team"] = df["Team Player Name Current Status"].apply(extract_team)

                df["Player Name"] = df["Team Player Name Current Status"].apply(
                    extract_name
                )
                df["Current Status"] = df["Team Player Name Current Status"].apply(
                    lambda x: x.split(" ")[-1] if pd.isna(x) == False else x
                )
                df.drop(
                    columns=["Team Player Name Current Status", "Reason"], inplace=True
                )
                df_copy = df.copy()
                df = df_copy.drop(df_copy.tail(1).index)
                # 删除Player Name为NaN的行
                df.dropna(subset=["Player Name"], inplace=True)
                df = df[
                    [
                        "Game Date",
                        "Game Time",
                        "Matchup",
                        "Team",
                        "Player Name",
                        "Current Status",
                    ]
                ]
        # 创建 DataFrame 的副本
        df_copy = df.copy()

        # 在副本上修改 "Date injury Report" 和 "Time injury Report" 列
        df_copy["Date injury Report"] = last_link[-19:-9]
        df_copy["Time injury Report"] = last_link[-8:-4]

        # 如果需要将修改后的 DataFrame 赋值回原始 DataFrame
        df = df_copy

        df_7col = pd.concat([df_7col, df], axis=0)
        # fill nan with above value
        df_7col.fillna(method="ffill", inplace=True)
        # remove status is NOT YET SUBMITTED
        df_7col = df_7col[df_7col["Current Status"] != "NOT YET SUBMITTED"]

    return df_7col


def extarct_official_injury_report(start_date, end_date):
    """
    a function that unifies all the different formats of the NBA official injuries reports between two dates
    and returns the full data frame.
    :param start_date: str - strat date, fromat: ("%Y-%m-%d")
    :param end_date: str -  end date, fromat: ("%Y-%m-%d")
    :return: data frame - the data frame with all the NBA official injuries reports
    """

    df_7col = pd.DataFrame()

    base_url = "https://ak-static.cms.nba.com/referee/injury/Injury-Report_"
    days_num = days_between(start_date, end_date) + 1

    for _ in range(days_num):
        print("")
        print("Date: ", start_date)

        for hour in ["_01PM.pdf", "_05PM.pdf"]:
            url = base_url + str(start_date) + hour

            result = None
            retry = 0
            while result is None and retry < 2:
                try:
                    df_lst: list[pd.DataFrame] = tabula.read_pdf(url, pages="all")  # type: ignore
                    for df in df_lst:
                        df["Date injury Report"] = start_date
                        df["Time injury Report"] = hour[1:5]
                        df_7col = pd.concat([df_7col, df], axis=0)
                    result = True
                except Exception as e:
                    retry += 1
                    time.sleep(1)

        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d").date()
        start_date = str(start_date + datetime.timedelta(days=1))

    if len(df_7col) != 0:
        df_7col = arrange_df(df_7col)
        df_7col = df_7col[
            [
                "Game Date",
                "Game Time",
                "Matchup",
                "Team",
                "Player Name",
                "Current Status",
                "Reason",
                "Date injury Report",
                "Time injury Report",
            ]
        ]

    return df_7col


if __name__ == "__main__":
    # start_date = "2023-01-21"
    # end_date = "2023-01-26"
    # df = extarct_official_injury_report(start_date, end_date)
    # df.to_csv(f"data/{start_date}_{end_date}.csv")
    # combine_injury_report_page("data/Injury-Report_2023-10-27_02AM.pdf")
    pass
