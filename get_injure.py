import numpy as np
import pandas as pd
import tabula
import requests as rq
from lxml import etree
from types_ import team_in_nba_office_website

team = team_in_nba_office_website


def query_last_injury_report():
    last_link = ""
    res = rq.get("https://official.nba.com/nba-injury-report-2024-25-season/")
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
        return input_string
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
            df[["Game Date", "Game Time", "Matchup"]] = df[
                ["Game Date", "Game Time", "Matchup"]
            ].fillna(method="ffill")
            # 删除Player Name为NaN的行
            df.dropna(subset=["Player Name"], inplace=True)
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
                df["Matchup"] = df["Matchup"].fillna(method="ffill")
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
        if df.shape[1] == 3:
            df.columns = ["Matchup", "Team Player Name Current Status", "Reason"]
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
            df["Matchup"] = df["Matchup"].fillna(method="ffill")
            df.dropna(subset=["Current Status"], inplace=True)
        if df.shape[1] == 2:
            df.columns = ["Team Player Name Current Status", "Reason"]
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
            df["Game Date"] = np.nan
            df["Game Time"] = np.nan
            df["Matchup"] = np.nan

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
    print(df_7col.to_string())
    return df_7col


if __name__ == "__main__":
    # combine_injury_report_page("data/Injury-Report_2023-10-27_02AM.pdf")
    pass
