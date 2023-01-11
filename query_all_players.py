import asyncio
import json

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from types_ import team_slugs
from datetime import datetime
from pytz import timezone


async def main():

    transport = AIOHTTPTransport(
        url="https://api.sorare.com/sports/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    async with Client(transport=transport) as session:
        with open("query/NBAPlayersByTeamQuery.graphql") as f:
            playersQuery = gql(f.read())

        with open("query/NBAPlayersBySlugsQuery.graphql") as g:
            playerDataQuery = gql(g.read())

        all_cards_info = []
        for team_slug in team_slugs:
            playersResult = await session.execute(
                playersQuery, variable_values={"input": team_slug}
            )
            players_in_a_team: list[str] = list(
                map(lambda i: i["slug"], playersResult["nbaTeam"]["players"])
            )

            players_in_a_team: list[str] = list(
                set(players_in_a_team)
                - set(
                    ["ibou-badji-20021013"]
                )  # ibou badji has no data, query will cause error
            )

            playerDataResult = await session.execute(
                playerDataQuery, variable_values={"input": players_in_a_team}
            )

            for playerData in playerDataResult["nbaPlayers"]:
                all_cards_info.append(playerData)

            print(f"Query {team_slug} done.")

        today: datetime = datetime.now(timezone("US/Eastern"))
        today_str: str = today.strftime("%Y-%m-%d")

        with open(f"data/all-players-data-{today_str}.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print("all player slug saved in data folder")


asyncio.run(main())
