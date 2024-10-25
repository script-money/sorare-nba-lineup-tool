from asyncio import run
import json
import os

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

from types_ import NBACard

with open("query/RecentCurrentUserCardsQuery.graphql") as g:
    query_card_info = gql(g.read())

with open("query/NBACardsByIdsQuery.graphql") as f:
    query = gql(f.read())


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
        after = ""
        card_slugs = []
        while True:
            result = await session.execute(
                query_card_info,
                variable_values={"after": after},
            )
            for node in result["currentUser"]["cards"]["nodes"]:
                card_slugs.append(node["slug"])

            endCursor = result["currentUser"]["cards"]["pageInfo"]["endCursor"]
            if endCursor == None:
                break
            after = endCursor
        print(f"total {len(card_slugs)} cards")

        all_cards_info: list[NBACard] = []

        for i in range(0, len(card_slugs), 50):
            print("querying from", i, "to", min(len(card_slugs), i + 50))
            result = await session.execute(
                query,
                variable_values={"slugs": card_slugs[i : i + 50]},
            )
            for card in result["anyCards"]:
                if card["sport"] == "NBA":
                    all_cards_info.append(card)

        # save result as json to data, naming as date
        with open(f"data/cards.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print(f"{len(all_cards_info)} cards data saved in data folder")


run(main())
