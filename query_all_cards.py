from asyncio import run
import json
import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from types_ import NBACard, NBACardsInput

with open("query/NBACardsByIdsQuery.graphql") as f:
    query = gql(f.read())

with open("query/RecentCurrentUserCardsQuery.graphql") as g:
    query_card_info = gql(g.read())

# with open("config/NBACards.json") as f:
#     data = json.load(f)
#     card_ids: list[str] = list(
#         map(
#             lambda x: x["id"],
#             data["data"]["currentUser"]["nbaCards"]["nodes"],
#         )
#     )


async def main():
    token = os.getenv("JWT")
    transport: AIOHTTPTransport = AIOHTTPTransport(
        url="https://api.sorare.com/federation/graphql",
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {token}",
            "JWT-AUD": "sorare-nba-lineup-tool",
        },
    )

    async with Client(transport=transport, execute_timeout=30) as session:
        after = 0
        card_ids = []
        while True:
            result = await session.execute(
                query_card_info,
                variable_values={"after": str(after)},
            )
            for node in result["currentUser"]["nbaCards"]["nodes"]:
                card_ids.append(node["id"])

            endCursor = result["currentUser"]["nbaCards"]["pageInfo"]["endCursor"]
            if int(endCursor) % 200 != 0:
                break
            after += 200
        print(f"total {len(card_ids)} cards")

        all_cards_info: list[NBACard] = []

        for i in range(0, len(card_ids), 50):
            print("querying from", i, "to", min(len(card_ids), i + 50))
            input: NBACardsInput = {"assetIds": [], "ids": card_ids[i : i + 50]}
            result = await session.execute(
                query,
                variable_values={"input": input},
            )
            all_cards_info.extend(result["nbaCards"])

        # save result as json to data, naming as date

        with open(f"data/cards.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print(f"{len(all_cards_info)} cards data saved in data folder")


run(main())
