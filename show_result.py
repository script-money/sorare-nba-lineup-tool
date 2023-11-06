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
    diffs_str = "\n".join(diffs)
    pyperclip.copy(diffs_str)
    print("result in copyboard")


if __name__ == "__main__":
    results = "Joel Embiid(42), Cam Thomas(14), Moritz Wagner(11), Luka Dončić(54), Aaron Nesmith(21), Derrick White(26), Jalen Duren(28), Evan Mobley(29), Ben Simmons(18), Malik Beasley(6)"
    print_last_week_prict(results)
