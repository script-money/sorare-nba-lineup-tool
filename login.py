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

    two_factor_code = os.getenv("TWO_FACTOR_CODE")

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
        if two_factor_code is not None:
            otp_session_challenge = res["signIn"]["otpSessionChallenge"]
            if otp_session_challenge != "" or otp_session_challenge != None:
                res = await session.execute(
                    sign_in_mutation,
                    variable_values={
                        "input": {
                            "email": email,
                            "password": hashed_password.decode("utf-8"),
                            "otpSessionChallenge": otp_session_challenge,
                            "otpAttempt": two_factor_code,
                        }
                    },
                )
                if (
                    len(res["signIn"]["errors"]) > 0
                    and res["signIn"]["errors"][0]["message"] == "invalid"
                ):
                    print("Login in failed, Please check your two factor code")
                    exit(0)

        token = res["signIn"]["currentUser"]["jwtToken"]["token"]

        # Read the existing .env file
        env_lines = []
        if os.path.exists("./.env"):
            with open("./.env", "r") as f:
                env_lines = f.readlines()

        # Check if JWT exists and update it, or add a new JWT
        jwt_found = False
        for i, line in enumerate(env_lines):
            if line.startswith("JWT="):
                env_lines[i] = f"JWT={token}\n"
                jwt_found = True
                break

        if not jwt_found:
            env_lines.append(f"JWT={token}\n")

        # Save the updated .env file
        with open("./.env", "w") as f:
            f.writelines(env_lines)
            print("Save token to env success")


run(main())
