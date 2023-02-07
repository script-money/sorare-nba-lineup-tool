import pandas as pd
import tabula
import datetime
import time
import re
import requests as rq
from lxml import etree
from pytz import timezone

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


# check if a cell belongs to the "Team" column by building a list of all NBA teams
def teams_pattern(val):
    return val in [
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
        "Minnesota " + "Timberwolves",
        "Minnesota\rTimberwolves",
    ]


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


def move_cell_right(df):
    """
    a function that locating each variable in it's right cell using the patterns above
    :param df: data frame - Data frame fo NBA injury report
    :return: data frame - a fixed data frameof the NBA official injury report
    """
    if df.shape[1] == 11 | df.shape[1] == 10:
        for row in range(df.shape[0]):
            for col in range(7):
                cell = df.iat[row, col]
                if pd.isna(cell) == True or shift_by_pattern(cell, df.columns[col]):
                    continue
                else:
                    df.iloc[[row], col:] = df.iloc[[row], col:].shift(1, axis=1)
    else:
        for row in range(df.shape[0]):
            for col in range(6):
                cell = df.iat[row, col]
                if pd.isna(cell) == True or shift_by_pattern(cell, df.columns[col]):
                    continue
                else:
                    df.iloc[[row], col:] = df.iloc[[row], col:].shift(1, axis=1)
    return df


def fill_na_with_above_value(df):
    """
    a function that fills Nan values with the appropriate value
    :param df: data frame - Data frame fo the NBA injury report
    :return: data frame - Data frame of the NBA official injury report with values instead of Nan
    """
    for row in range(1, df.shape[0]):
        for col in range(4):
            cell = df.iat[row, col]
            if pd.isna(cell):
                df.iat[row, col] = df.iat[row - 1, col]
    return df


def remove_if_not_submitted(df):
    """
    a function that remove rows with NOT YET SUBMITTED, which are not informative
    :param df: data frame - the data frame fo the NBA injury report
    :return: data frame - the data frame of the NBA official injury report without rows that contains NOT YET SUBMITTED values
    """
    if df.shape[1] == 11:
        col_names = [
            "Game Date",
            "Game Time",
            "Matchup",
            "Team",
            "Player Name",
            "Category",
            "Reason",
            "Current Status",
            "Previous Status",
            "Date injury Report",
            "Time injury Report",
        ]
        if list(df.columns) == col_names:
            df = df[df["Category"] != "NOT YET SUBMITTED"]
        else:
            df = df[df["Reason"] != "NOT YET SUBMITTED"]
    else:
        df = df[df["Reason"] != "NOT YET SUBMITTED"]
    return df


def arrange_df(df):
    """
    a function that making all the relevant changes in the df to make it in the right format
    :param df: data frame - the data frame of the NBA injury report
    :return: data frame - The final and useful data frame of the NBA official injury report
    """
    df1 = df.iloc[:, : df.shape[1] - 2]
    df2 = df.iloc[:, df.shape[1] - 2 :]
    df1 = move_cell_right(df1)
    df1 = fill_na_with_above_value(df1)
    df = pd.concat([df1, df2], axis=1)
    df = remove_if_not_submitted(df)

    return df


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
    df_7col = pd.DataFrame()
    last_link = ""
    res = rq.get("https://official.nba.com/nba-injury-report-2022-23-season/")
    if res.status_code != 200:
        raise ValueError(
            "Error in getting the link to the last injury report, please try again later"
        )
    root = etree.HTML(res.text, parser=etree.HTMLParser(encoding="utf-8"))
    for element in root.xpath('//div[@class="col-xs-12 post-injury"]//a/@href'):
        last_link = element

    today = datetime.datetime.now(timezone("US/Eastern"))
    today_str = today.strftime("%Y-%m-%d")
    result = None
    retry = 0

    while result is None and retry < 2:
        try:
            df_lst: list[pd.DataFrame] = tabula.read_pdf(last_link, pages="all")  # type: ignore
            for df in df_lst:
                df["Date injury Report"] = today_str
                df["Time injury Report"] = last_link[-8:-4]
                df_7col = pd.concat([df_7col, df], axis=0)
            result = True
        except Exception as e:
            retry += 1
            time.sleep(1)

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
    start_date = "2023-01-21"
    end_date = "2023-01-26"
    df = extarct_official_injury_report(start_date, end_date)
    df.to_csv(f"data/{start_date}_{end_date}.csv")
