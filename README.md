# tictactoe-api
Tic Tac Toe API with Django

To use the api, run the migrations at the root directory of the project
```
python manage.py migrate
```

# Routes
 ## /games/
 - Use a GET request on this endpoint to get how many games have been created on the system at that point.

 ## /games/
 - Post to this endpoint to create a new game, you can add a **number_of_sides** field in the body to specify the board size, from 3 to 5.

 ## /games/<game_id>/
 - GET request to fetch from this endpoint, stats of a game like winner, how many moves played etc.

 ## /play/<game_id>/
 - POST request with the **player**, **row**, and **column** to make a move on the board game