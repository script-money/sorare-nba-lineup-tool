import json
from asyncio import run

from gql import Client, gql, client
from gql.transport.aiohttp import AIOHTTPTransport
from types_ import NBAPlayer, team_slugs

with open("query/NBAPlayersByTeamQuery.graphql") as f:
    playersQuery = gql(f.read())

with open("query/NBAPlayersBySlugsQuery.graphql") as g:
    playerDataQuery = gql(g.read())


async def main():
    async with Client(
        transport=AIOHTTPTransport(
            url="https://api.sorare.com/federation/graphql",
            # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
        )
    ) as session:
        all_cards_info: list[NBAPlayer] = []

        for team_slug in team_slugs:
            all_cards_info.extend(await query_task(team_slug, session))

        with open(f"data/all-players-data.json", "w") as f:
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
    print(f"querying {team_slug}")
    players_in_a_team = await query_players_in_a_team_task(team_slug, session)
    playerDatas = await query_player_data_task(players_in_a_team, session)
    return playerDatas


run(main())
