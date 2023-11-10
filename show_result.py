import json
from types_ import NBAPlayer
import pyperclip

with open(f"data/all-players-data.json", "r") as f:
    players_json: list[NBAPlayer] = json.load(f)


def print_last_week_prict(results: str):
    player_results = results.split(", ")
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
    results = "Bismack Biyombo(11), Malcolm Brogdon(20), Goga Bitadze(19), Cam Thomas(22), Dyson Daniels(14), Dillon Brooks(20), Grant Williams(20), Reggie Jackson(10), Tyler Herro(34), Moritz Wagner(13)"
    print_last_week_prict(results)
