from asyncio import run, Task, create_task, wait, TaskGroup
import json

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from datetime import datetime
from pytz import timezone

from types_ import NBACard, NBACardsRes

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

    transport: AIOHTTPTransport = AIOHTTPTransport(
        url="https://api.sorare.com/sports/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    async with Client(transport=transport) as session:

        variable = {"input": {"assetIds": [], "ids": card_ids}}
        all_cards_info: list[NBACard] = []
        task_list: list[Task[NBACardsRes]] = []

        # split card_ids into multiple chunks every 50
        async with TaskGroup() as g:
            for i in range(0, len(card_ids), 50):
                variable["input"]["ids"] = card_ids[i : i + 50]
                task: Task[NBACardsRes] = g.create_task(
                    session.execute(query, variable_values=variable)
                )  # type: ignore
                task_list.append(task)

        all_cards_info = [task.result()["nbaCards"] for task in task_list]  # type: ignore

        # save result as json to data, naming as date
        today = datetime.now(timezone("US/Eastern"))
        today_str = today.strftime("%Y-%m-%d")
        with open(f"data/cards-{today_str}.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print("cards data saved in data folder")


run(main())
