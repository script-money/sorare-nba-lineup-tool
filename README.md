# sorare nba up tool

## install

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

## search in your cards

1. `poetry run python query_all_cards.py` will request all your cards and save in data folder
2. `poetry run python query_position_players.py` will request all player current position (once a week)
3. `poetry run python query_injure_and_match.py` will request all injure and matches in data folder (once a week)
4. change `config/config.py` if need, then `poetry run python compute.py` will compute results.txt to data folder

## search in all nba players

1. `poetry run python query_all_players.py` will query all nba players and save in data folder (once a week)
2. `poetry run python query_position_players.py` will request all player current position (once a week)
3. `poetry run python query_injure_and_match.py` will request all injure and matches in data folder (once a week)
4. change `config/config.py` if need, then `poetry run python compute.py -r True` will compute results.txt to data folder

## invite link

[https://sorare.pxf.io/4eQk5r](https://sorare.pxf.io/4eQk5r)