import asyncio
import json

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import date


def load_query(path):
    with open(path) as f:
        return gql(f.read())


async def main():

    transport = AIOHTTPTransport(
        url="https://api.sorare.com/sports/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    async with Client(transport=transport) as session:

        query = load_query("query/NBACardsByIdsQuery.graphql")
        with open("config/NBACards.json") as f:
            data = json.load(f)
            card_ids = list(
                map(
                    lambda x: x["id"],
                    data["data"]["currentSportsUser"]["nbaCards"]["nodes"],
                )
            )

        variable = {"input": {"assetIds": [], "ids": card_ids}}

        all_cards_info = []

        # split card_ids into multiple chunks every 50
        for i in range(0, len(card_ids), 50):
            variable["input"]["ids"] = card_ids[i : i + 50]
            result = await session.execute(query, variable_values=variable)
            all_cards_info += result["nbaCards"]

        # save result as json to data, naming as date
        with open(f"data/cards-{date.today()}.json", "w") as f:
            json.dump(all_cards_info, f)
            print("cards data saved in data folder")


asyncio.run(main())
