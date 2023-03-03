import json
from types_ import NBAPlayer

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
    print("\n".join(diffs))


if __name__ == "__main__":
    results = "Nassir Little(12), Justin Holiday(6), Jakob Poeltl(28), Naz Reid(19), Daniel Theis(11), Gordon Hayward(25), Kris Dunn(20), Charles Bassey(10), Mark Williams(22), Matisse Thybulle(15)"
    print_last_week_prict(results)
