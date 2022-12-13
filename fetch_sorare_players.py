import asyncio
import json
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport


team_slugs = [
    "brooklyn-nets",
    "indiana-pacers",
    "cleveland-cavaliers",
    "toronto-raptors",
    "phoenix-suns",
    "portland-trail-blazers",
    "detroit-pistons",
    "orlando-magic",
    "la-clippers",
    "boston-celtics",
    "memphis-grizzlies",
    "oklahoma-city-thunder",
    "dallas-mavericks",
    "minnesota-timberwolves",
    "houston-rockets",
    "utah-jazz",
    "los-angeles-lakers",
    "denver-nuggets",
    "chicago-bulls",
    "san-antonio-spurs",
    "sacramento-kings",
    "miami-heat",
    "golden-state-warriors",
    "new-york-knicks",
    "new-orleans-pelicans",
    "washington-wizards",
    "atlanta-hawks",
    "milwaukee-bucks",
    "philadelphia-76ers",
    "charlotte-hornets",
]


async def main():
    transport = AIOHTTPTransport(
        url="https://api.sorare.com/sports/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    players_in_team: dict[str, list[str]] = {}

    async with Client(transport=transport) as session:
        query = gql(
            """
          query NBATeamQuery($slug: String!) {
            nbaTeam(slug: $slug) {
              fullName
              abbreviation
              players{
                displayName
              }
            }
          }
        """
        )

        for team_slug in team_slugs:
            result = await session.execute(query, variable_values={"slug": team_slug})
            team = result["nbaTeam"]["abbreviation"]
            players = list(
                map(lambda x: x["displayName"], result["nbaTeam"]["players"])
            )
            players_in_team[team] = players
            print(f"query {team} done")

    with open("data/all_players_in_sorare.json", "w") as f:
        json.dump(players_in_team, f)
        print("all players in sorare data saved in data folder")


asyncio.run(main())
