import json
from types_ import NBAPlayer
import pyperclip

with open(f"data/all-players-data.json", "r") as f:
    players_json: list[NBAPlayer] = json.load(f)


def print_last_week_prict(results: str):
    player_results = []
    player_results_money_list = results.split(", ")
    for player_results_money in player_results_money_list:
        player_results.append(player_results_money.split(" $")[0])
    diffs = []
    for player in player_results:
        name, number = player.split("(")
        number = int(number[:-1])
        for player_data in players_json:
            if player_data["displayName"] == name:
                last_week_score = int(player_data["latestFixtureStats"][1]["score"])
                diff = last_week_score - number
                diffs.append(
                    f"{name:<25} avg: {number:<3} actual: {last_week_score:<3} outperform: {diff:<2}"
                )
    print("\n")
    diffs_str = "\n".join(diffs)
    print(diffs_str.strip())
    pyperclip.copy(diffs_str)
    print("\n")


if __name__ == "__main__":
    results = "Kevin Huerter(25) $14.77, Jordan Clarkson(25) $14.03, Matisse Thybulle(15) $7.38, Domantas Sabonis(41) $44.63, Nikola Jokić(60) $310.06, Brandin Podziemski(8) $20.99, David Roddy(15) $6.80, Santi Aldama(16) $8.66, Damian Lillard(41) $52.11, Cason Wallace(15) $10.81"
    print_last_week_prict(results)
