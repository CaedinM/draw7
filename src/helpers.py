from textwrap import dedent

def print_card(card, player):
    print(dedent(f"""
        {player}:
        ┏---┓
        | {card} |
        ┗---┛
    """))

def print_win_message(player, score):
    print(dedent(f"""
    ####################################
    {player} HAS WON WITH A SCORE OF {score}
    ####################################
    """))

# ask if user wants to draw or end turn
def ask_decision(player) -> str:
    while True:
        decision = input(dedent(f"""
            What would you like to do {player}?:

            H: Hit
            S: Stay
        """)).strip().lower()
        if decision in ["h", "s"]:
            break
        else:
            print("Invalid input, try again")

    return decision

# ask for player names at app start
def get_players() -> list[str]:
    print()
    while True:
        try:
            num_players = int(input("How many players are playing? "))
            if num_players >= 2 and num_players <= 8:
                break
            print("Number of players must be between 2 and 8.")
        except ValueError:
            print("Please enter a valid whole number")

    players = []
    for i in range(num_players):
        name = input(f"Enter name for Player {i + 1}: ")
        if not name:
            name = f"Player {i + 1}"
        players.append(name)
    
    return players

# print a summary given the final stats from a round
def print_round_summary(round, stats):
    print(dedent(f"""
        -----------------------------------------------
          Round {round} is over, here's how everyone did:
        -----------------------------------------------
    """))
    for name, player in stats.items():
        print(f"{name}: {player['score']} points")