import json
from asyncio import run

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

# 读取查询
with open("query/OverperformQuery.graphql", "r") as f:
    nbaPastFixturesQuery = gql(f.read())


async def main():
    transport = AIOHTTPTransport(url="https://api.sorare.com/federation/graphql")

    async with Client(transport=transport) as session:
        all_fixtures_data = []
        after = None

        while True:
            result = await session.execute(
                nbaPastFixturesQuery, variable_values={"first": 120, "after": after}
            )

            fixtures = result["nbaPastFixtures"]["nodes"]
            all_fixtures_data.extend(fixtures)

            page_info = result["nbaPastFixtures"]["pageInfo"]
            after = page_info["endCursor"]

            if not page_info.get("hasNextPage", False):
                break

        with open("data/overperform-data.json", "w") as f:
            json.dump(all_fixtures_data, f, indent=4)
            print("All NBA past fixtures data saved in data folder")


run(main())
