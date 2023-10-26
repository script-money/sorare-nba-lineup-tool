# sorare nba up tool

Working for 23-24 season

## install

1. install poetry, then use `poetry install` to install dependencies
2. install JAVA environment
3. get all NBACard id at `https://api.sorare.com/federation/graphql/playground#`, The _(first: 120)_ change to your card amount and copy query ids to **config/NBACards.json**

   ```graphql
   query RecentCurrentUserCardsQuery {
     currentUser {
       nbaCards(first: 200) {
         nodes {
           id
         }
       }
     }
   }
   ```

## search in your cards

0. set proxies in config/config.py if your need proxy to request
1. `poetry run python query_all_cards.py` will request all your cards and save in data folder
2. `poetry run python query_position_players.py` will request all player current position (once a week)
3. `poetry run python query_injure_and_match.py` will request all injure and matches in data folder (once a week)
4. change `config/config.py` if need, then `poetry run python compute.py` will compute results.txt to data folder

PS: It is recommended to get the latest injury report within 20 minutes of the end of the game week

## search in all nba players

1. `poetry run python query_all_players.py` will query all nba players and save in data folder (once a week)
2. `poetry run python query_position_players.py` will request all player current position (once a week)
3. `poetry run python query_injure_and_match.py` will request all injure and matches in data folder (once a week)
4. change `config/config.py` if need, then `poetry run python compute.py -r True` will compute results.txt to data folder

## invite link

<<<<<<< HEAD
[https://sorare.pxf.io/scriptmoney](https://sorare.pxf.io/scriptmoney)
=======
[https://sorare.pxf.io/4eQk5r](https://sorare.pxf.io/4eQk5r)

> > > > > > > 9262514475539314e3bdbaaec574deac20dfb9fe
