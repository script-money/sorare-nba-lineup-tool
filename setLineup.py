from asyncio import run
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError
import os
from pandas import DataFrame, read_pickle
import json
import time

from types_ import NBACard

token = os.getenv("JWT")
caceh_file_path = "data/cached.pickle"


async def setLineup():
    if os.path.exists(caceh_file_path):
        print(f"Read weekly prediction from {caceh_file_path}")
        prediction_df = DataFrame(read_pickle(caceh_file_path).to_dict("records"))

    with open("config/priority_training_players.txt") as f:
        priority_players = f.readlines()

    priority_slugs = list(
        map(
            lambda x: x.strip(),
            filter(lambda x: x != "" and x != "\n", priority_players),
        )
    )

    with open(f"data/cards.json", "r") as f:
        cards: list[NBACard] = json.load(f)

    if token is None:
        print("Please run login.py first")
        exit(0)

    with open("query/NBAOpenFixtureQuery.graphql") as g:
        openFixtureQuery = gql(g.read())

    with open("query/NBAMyCardsSuggestionsQuery.graphql") as g:
        myCardsSuggestionsQuery = gql(g.read())

    with open("query/NBACreateOrUpdateLineupMutation.graphql") as g:
        setLineupMutation = gql(g.read())

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

    groups_to_set = []

    async with Client(transport=transport) as session:
        # 读取所有联赛，获取联赛训练的 slug
        try:
            open_fixture_res = await session.execute(openFixtureQuery)
            leader_boards = open_fixture_res["nbaOpenFixture"]["leaderboards"]
            # find first isTraining==True leaderboard use next()
            leader_board = next(
                filter(lambda x: x["isTraining"] == True, leader_boards)
            )
            train_slug = leader_board["slug"]
            print(f"setting up {train_slug}")
        except TransportQueryError as e:
            print("fetch open fixture failed")
            exit(0)

        if train_slug == None or train_slug == "":
            print("No training leaderboard slug found")
            exit(0)

        # 获取所有可以用在训练的卡
        is_end = False
        after = 0
        all_train_cards = []
        while not is_end:
            suggestion_res = await session.execute(
                myCardsSuggestionsQuery,
                variable_values={
                    "leaderboardSlug": train_slug,
                    "after": str(after),
                },
            )
            lineup_cards = suggestion_res["nbaLeaderboard"]["myComposeLineupCards"]
            if not lineup_cards["pageInfo"]["hasNextPage"]:
                is_end = True
            all_train_cards.extend(
                list(map(lambda x: x["card"]["slug"], lineup_cards["nodes"]))
            )
            after = lineup_cards["pageInfo"]["endCursor"]
        print(f"available card have {len(all_train_cards)}")

        all_train_cards_info = list(
            filter(lambda x: x["slug"] in all_train_cards, cards),
        )

        # resort all_train_cards_info by prediciton_df
        def get_normaldist_mean(card_id):
            matching_rows = prediction_df.loc[prediction_df["id"] == card_id, "expect"]
            if not matching_rows.empty:
                return matching_rows.iloc[0].mean
            return float("-inf")  # 如果没有找到匹配的行，返回负无穷大，使得这张卡片排在最后

        # 所有可以训练的卡片进行排序
        all_train_cards = sorted(
            all_train_cards_info,
            key=lambda x: get_normaldist_mean(x["id"]),
            reverse=True,
        )

        all_train_cards_slug = list(map(lambda x: x["slug"], all_train_cards))

        index = 0
        for priority_slug in priority_slugs:
            if priority_slug in all_train_cards_slug:
                all_train_cards_slug.remove(priority_slug)
                other_players = all_train_cards_slug[index : index + 4]
                groups_to_set.append([priority_slug] + other_players)
                index += 4
            else:  # 说明这张优先卡不能用于训练
                groups_to_set.append(all_train_cards_slug[index : index + 5])
                index += 5
        # 优先卡片已经全部处理完毕，剩下的卡片5个一组，放入groups_to_set
        while index < len(all_train_cards_slug):
            groups_to_set.append(all_train_cards_slug[index : index + 5])
            index += 5

        # print(set_lineup_res["createOrUpdateNBALineup"]["createdLineup"]["id"])
        # TODO save lineup to file

    async with Client(transport=transport) as session2:
        lineups = []
        for group in groups_to_set:
            try:
                set_lineup_res = await session2.execute(
                    setLineupMutation,
                    variable_values={
                        "input": {
                            "leaderboardSlug": train_slug,
                            "cardSlugs": group,
                        }
                    },
                )
                lineup_id = set_lineup_res["createOrUpdateNBALineup"]["createdLineup"][
                    "id"
                ]
                lineups.append(lineup_id)
                print(f"set lineup {lineup_id} success")
                time.sleep(1)
            except:
                continue

        # save lineup to file
        with open("data/lineups.txt", "w") as f:
            f.writelines(lineups)


run(setLineup())
