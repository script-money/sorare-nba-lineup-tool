import json
from asyncio import run
import os

from gql import Client, gql, client
from gql.transport.aiohttp import AIOHTTPTransport
from types_ import NBAPlayerWithStats, team_slugs

with open("query/NBAPlayersByTeamQuery.graphql") as f:
    playersQuery = gql(f.read())

with open("query/NBAPlayersBySlugsQuery.graphql") as g:
    playerDataQuery = gql(g.read())


async def main():
    token = os.getenv("JWT")
    async with Client(
        transport=AIOHTTPTransport(
            url="https://api.sorare.com/federation/graphql",
            headers={
                "content-type": "application/json",
                "Authorization": f"Bearer {token}",
                "JWT-AUD": "sorare-nba-lineup-tool",
            },
        )
    ) as session:
        all_players_info: list[NBAPlayerWithStats] = []

        for team_slug in team_slugs:
            all_players_info.extend(await query_task(team_slug, session))

        with open(f"data/all-players-data.json", "w") as f:
            json.dump(all_players_info, f, indent=4)
            print("all player data saved in data folder")


async def query_task(team_slug, session: client.AsyncClientSession):
    print(f"querying {team_slug}")
    players_in_a_team = await query_players_in_a_team_task(team_slug, session)
    playerDatas = await query_player_data_task(players_in_a_team, session)
    return playerDatas


async def query_players_in_a_team_task(team_slug: str, session) -> list[str]:
    playersResult = await session.execute(
        playersQuery, variable_values={"input": team_slug}
    )
    players_in_a_team: list[str] = list(
        map(lambda i: i["slug"], playersResult["team"]["activePlayers"]["nodes"])
    )

    return players_in_a_team


async def query_player_data_task(players_in_a_team, session: client.AsyncClientSession):
    playerDataResult = await session.execute(
        playerDataQuery, variable_values={"input": players_in_a_team}
    )
    return [playerData for playerData in playerDataResult["anyPlayers"]["nodes"]]


run(main())
