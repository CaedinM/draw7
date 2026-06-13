from helpers import get_players
from gamestate import Gamestate
from textwrap import dedent

# welcome user
print(dedent("""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
         WELCOME TO DRAW7!
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""))

# Ask how many players and get names
players = get_players()

# Initialize a new game
current_game = Gamestate(players)

while current_game.is_game_over == False:
    result = current_game.run_round()
    if result == "GG":
        current_game.is_game_over = True
    else:
        current_game.update(result)
        current_game.print_scores()
        print()
        input("Press Enter to continue to the next round...")
