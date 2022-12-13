# sorare nba up tool

invite link: [https://sorare.com/r/scriptmoney](https://sorare.com/r/scriptmoney)

1. install poetry, then use `poetry install` to install dependencies
2. get all NBACard id at `https://api.sorare.com/sports/graphql/playground#`, The *(first: 120)* change to your card amount and copy query ids to **config/NBACards.json**

    ```graphql
    query RecentCurrentUserCardsQuery {
    currentSportsUser {
        nbaCards(first: 120) {
        nodes {
            id
        }
        }
    }
    }
    ```

3. `poetry run python query_all_cards.py` will request all cards and save in data folder
4. `poetry run python query_injure_and_match.py`  will request all injure and matches in data folder
5. change `config/config.py` if need, then `poetry run python compute.py` will compute results.txt to data folder
