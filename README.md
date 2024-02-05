----------------------- TACTEGO, A STRATEGY BOARD GAME -------------------------


Welcome to tactego, a 2 player strategy board game. 
The object of the game is to capture all of the enemy flags.

-------- setup -------------

When running the program, you will first be asked for a seed. You may type in anything you'd like, as it will use this to randomly place each token on the board. For best results, use seed "asdf"

After that, you will be asked for the pieces file name. You will enter the name of the file with the list of the tokens you want to place. These files are
   1. small_game.pieces
   2. basic_game.pieces
These files are located in the project folder.

After that, you will be asked for the length and width of the board. 
For best results, when using the small_game.pieces file, set length to 6 and width to 4
When using the basic_game.pieces file, set length to 12 and width to 8

The game will start on reds turn. 

----- gameplay ----------

type in the coordinates of the token you would like to interact with in this format (row col). 

you have 2 types of tokens: numbered units and your flag. Protect enemy numbered units from moving onto your flag. 
two numbered units can engage in combat with each other by one moving onto each other. The one with the higher number wins. (ie. R6 will beat B5)
In the event of a tie, the attacker will always win

The winner will be decided when someone loses all of their flags. The person who lost their flags, well, lost. 
