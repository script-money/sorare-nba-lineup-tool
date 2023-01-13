import bcrypt
from dotenv import load_dotenv
import os
import requests as rq
from gql.transport.aiohttp import AIOHTTPTransport
from gql import Client, gql
from asyncio import run

load_dotenv()


async def main():
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    if password is None or email is None:
        assert False, "Please set EMAIL and PASSWORD in .env file"

    url = f"https://api.sorare.com/api/v1/users/{email}"
    res = rq.get(url)
    if res.status_code != 200:
        assert False, "Please check your email and network"

    salt = res.json()["salt"]
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt.encode("utf-8"))

    with open(
        "./query/SignInMutation.graphql",
    ) as f:
        sign_in_mutation = gql(f.read())

    transport: AIOHTTPTransport = AIOHTTPTransport(
        url="https://api.sorare.com/graphql",
        # headers = {"Authorization": "Bearer <TheUserAccessToken>"}
    )

    async with Client(transport=transport) as session:
        res = await session.execute(
            sign_in_mutation,
            variable_values={
                "input": {"email": email, "password": hashed_password.decode("utf-8")}
            },
        )
        token = res["signIn"]["currentUser"]["jwtToken"]["token"]
        # save token to config/token
        with open("./.env", "a") as f:
            f.write(f"\nJWT={token}")
            print("save token to env success")


run(main())
