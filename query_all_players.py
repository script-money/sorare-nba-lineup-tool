import json
from asyncio import Task, run, create_task, gather

from gql import Client, gql, client
from gql.transport.aiohttp import AIOHTTPTransport
from types_ import NBAPlayer, team_slugs
from datetime import datetime
from pytz import timezone

with open("query/NBAPlayersByTeamQuery.graphql") as f:
    playersQuery = gql(f.read())

with open("query/NBAPlayersBySlugsQuery.graphql") as g:
    playerDataQuery = gql(g.read())


async def main():
    async with Client(
        transport=AIOHTTPTransport(
            url="https://api.sorare.com/sports/graphql",
            # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
        )
    ) as session:
        all_cards_info: list[NBAPlayer] = []
        tasks: list[Task[NBAPlayer]] = [create_task(query_task(s, session)) for s in team_slugs]  # type: ignore
        await gather(*tasks)

        all_cards_info.extend([task.result() for task in tasks])

        today: datetime = datetime.now(timezone("US/Eastern"))
        today_str: str = today.strftime("%Y-%m-%d")

        with open(f"data/all-players-data-{today_str}.json", "w") as f:
            json.dump(all_cards_info, f, indent=4)
            print("all player data saved in data folder")


async def query_players_in_a_team_task(team_slug: str, session) -> list[str]:
    playersResult = await session.execute(
        playersQuery, variable_values={"input": team_slug}
    )
    players_in_a_team: list[str] = list(
        map(lambda i: i["slug"], playersResult["nbaTeam"]["players"])
    )

    players_in_a_team: list[str] = list(
        set(players_in_a_team)
        - set(["ibou-badji-20021013"])  # ibou badji has no data, query will cause error
    )
    return players_in_a_team


async def query_player_data_task(players_in_a_team, session: client.AsyncClientSession):
    playerDataResult = await session.execute(
        playerDataQuery, variable_values={"input": players_in_a_team}
    )
    return [playerData for playerData in playerDataResult["nbaPlayers"]]


async def query_task(team_slug, session: client.AsyncClientSession):
    players_in_a_team = await query_players_in_a_team_task(team_slug, session)
    playerDatas = await query_player_data_task(players_in_a_team, session)
    return playerDatas


run(main())
