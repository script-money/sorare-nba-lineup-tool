from asyncio import run
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import os

token = os.getenv("JWT")


async def deleteLineup():
    with open("data/lineups.txt", "r") as f:
        try:
            lineup_ids = f.readlines()
        except:
            print("No lineup to delete")
            return

        if len(lineup_ids) == 0:
            print("No lineup to delete")
            return

    with open("query/DeleteLineupMutation.graphql") as g:
        deleteLineupMutation = gql(g.read())

    # leaderboardSlug: str, cardSlugs: list[str]
    transport = AIOHTTPTransport(
        url="https://api.sorare.com/federation/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
        headers={
            "content-type": "application/json",
            "Authorization": f"Bearer {token}",
            "JWT-AUD": "sorare-nba-lineup-tool",
        },
    )

    deleted_lineup_ids = []
    async with Client(transport=transport) as session:
        for lineup_id in lineup_ids:
            try:
                res = await session.execute(
                    deleteLineupMutation,
                    variable_values={
                        "id": lineup_id,
                    },
                )
                if res["deleteNBALineup"] is None:
                    print(f"deleted lineup {lineup_id}")
                    deleted_lineup_ids.append(lineup_id)
            except:
                print(f"delete lineup {lineup_id} failed, skip")
                continue

    # get remaining lineups
    remaining_lineup_ids = list(set(lineup_ids) - set(deleted_lineup_ids))
    with open("data/lineups.txt", "w") as f:
        f.writelines(remaining_lineup_ids)


run(deleteLineup())
