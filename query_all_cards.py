from asyncio import run
import json

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
from pytz import timezone

from types_ import NBACard, NBACardsInput

with open("query/NBACardsByIdsQuery.graphql") as f:
    query = gql(f.read())

with open("config/NBACards.json") as f:
    data = json.load(f)
    card_ids: list[str] = list(
        map(
            lambda x: x["id"],
            data["data"]["currentSportsUser"]["nbaCards"]["nodes"],
        )
    )


async def main():
    # token = os.getenv("JWT")
    transport: AIOHTTPTransport = AIOHTTPTransport(
        url="https://api.sorare.com/sports/graphql",
        # headers={
        #     "Authorization": f"Bearer {token}",
        #     "JWT-AUD": "sorare-nba-lineup-tool",
        # },
    )

    async with Client(transport=transport, execute_timeout=30) as session:

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
        today = datetime.now(timezone("US/Eastern"))
        today_str = today.strftime("%Y-%m-%d")
        with open(f"data/cards-{today_str}.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print(f"{len(all_cards_info)} cards data saved in data folder")


run(main())
