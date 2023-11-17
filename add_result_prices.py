import asyncio
import json
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import pyperclip


async def main(player_results: str):
    transport = AIOHTTPTransport(
        url="https://api.sorare.com/federation/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    rarity_index = 1
    rarity = (
        "limited"
        if rarity_index == 1
        else "rare"
        if rarity_index == 2
        else "super_rare"
    )
    slice_index = 5 if rarity_index == 1 else 3 if rarity_index == 2 else 1

    with open("data/all-players-data.json", "r") as f:
        players = player_results
        players_name = list(map(lambda x: x.split("(")[0].strip(), players.split(",")))
        players_average = list(
            map(lambda x: int(x.split("(")[1][:-1]), players.split(","))
        )
        # require len(players_name) == len(players_average) = len(players)

        # read f as json
        data = json.load(f)
        players_slots = []
        for player in players_name:
            player_data = next(filter(lambda p: p["displayName"] == player, data))
            players_slots.append(player_data["slug"])

    player_average_prices = dict()

    async with Client(transport=transport) as session:
        with open("query/PriceHistoryQuery.graphql", "r") as f:
            query_str = f.read()
            query = gql(query_str)
        for player_slot, player_name, player_average in zip(
            players_slots, players_name, players_average
        ):
            result = await session.execute(
                query,
                variable_values={
                    "rarity": rarity,
                    "playerSlug": player_slot,
                },
            )
            usd = list(
                map(
                    lambda x: int(x["amounts"]["usd"]),
                    result["tokens"]["tokenPrices"][:slice_index],
                )
            )
            mean_usd_price = sum(usd) / len(usd) / 1e2
            player_average_prices[player_name] = {
                "mean_usd_price": mean_usd_price,
                "players_average": player_average,
            }

        formatted_output = [
            f"{name}({info['players_average']}) ${info['mean_usd_price']:.2f}"
            for name, info in player_average_prices.items()
        ]
        result_str = ", ".join(formatted_output)
        print(result_str)
        pyperclip.copy(result_str)
        print("Result copied to clipboard")


if __name__ == "__main__":
    result_str = ""
    asyncio.run(main(result_str))
