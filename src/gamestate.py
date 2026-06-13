import random
from itertools import cycle
from textwrap import dedent
from helpers import *
from ev_calculator import calculate_ev


class Gamestate:
    
    DEFAULT_DECK = {0: 1, 1: 1, 2: 2, 3: 2, 4: 4, 5: 4, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10, 11: 11, 12: 12}
    EMPTY_DISCARD_PILE = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0}

    def __init__(self, players):
        # deck
        self.deck = dict(self.DEFAULT_DECK)
        self.discard_pile = dict(self.EMPTY_DISCARD_PILE)
        
        # game status
        self.is_game_over = False
        self.round = 0

        # players/scores
        self.players = players
        self.scores = {name: 0 for name in players}
    

    # draw a card from the deck
    def draw_card(self, player):
        """A helper that draws a card from the deck"""
        # pick a card at random from the deck
        keys = [k for k in self.deck if self.deck[k] > 0]
        weights = [self.deck[k] for k in keys]
        card = random.choices(keys, weights=weights, k=1)[0]

        # remove the card from the deck
        self.deck[card] -= 1

        # print the card
        print_card(card, player)
        return card

    # update gamestate
    def update(self, stats):
        for name, player in stats.items():
            # add round scores to players total score
            self.scores[name] += player["score"]

            if player["status"] == "busted":
                for card in player["hand"]:
                    self.discard_pile[card] += 1
    
    def reshuffle_deck(self):
        print("deck is empty, reshuffling from discard pile...")
        for card in self.discard_pile:
            self.deck[card] += self.discard_pile[card]
        self.discard_pile = dict(self.EMPTY_DISCARD_PILE)

    def print_scores(self):
        print(dedent("""

        -------------------
             SCOREBOARD
        ------------------- 
        """))
        for player in self.players:
            print(f"{player}: {self.scores[player]}")

    def win_check(self, player, score):
        if self.scores[player] + score >= 200:
            return True
        else: return False

    # full turn logic
    def run_round(self):
        round_status = "active"
        self.round += 1

        print(dedent(f"""
        ###################
              ROUND {self.round}
        ###################
        """))

        stats = {
            name: {
                # player can be: "active", "busted" or "secured"
                "status": "active",
                "score": 0,
                "hand": []
                    } for name in self.players
                }  
        
        player_turn = cycle(self.players)

        print(dedent("Initial Draws:"))
        # draw an initial card for each player
        for p in self.players:
            card = self.draw_card(p)

            # check if deck is empty after every draw
            if sum(self.deck.values()) == 0:
                self.reshuffle_deck()

            # update player's stats
            stats[p]["hand"].append(card)
            stats[p]["score"] += card
            
        while round_status == "active":
            # check for the case that every player has chosen to stay
            if all(not player["status"] == "active" for player in stats.values()):
                break
            
            # move to next player
            current_player = next(player_turn)
            # check if they are active
            if stats[current_player]["status"] == "active":
                print(dedent(f"""
                    -------------------------------------------------
                              Its {current_player}'s turn!
                    -------------------------------------------------
                    Current Hands:"""))
                for name, player in stats.items():
                    print(f"{name}: {player['hand']}")

                # calculate EV before asking for decision
                ev = calculate_ev(self.deck, stats[current_player]["hand"])
                
                # display recomendation
                if ev > 0:
                    recommendation = "Hit"
                else:
                    recommendation = "Stay"
                print(f"Recommendation: " + recommendation)

                # ask for a decision from active player
                decision = ask_decision(current_player)
                # if player chooses to stay
                if decision == "s":
                    stats[current_player]["status"] = "secured"
                elif decision == "h":
                    # draw a card
                    card = self.draw_card(current_player)
                    
                    # check if deck is empty after every draw
                    if sum(self.deck.values()) == 0:
                        self.reshuffle_deck()
                    

                    if card in stats[current_player]["hand"]:
                        stats[current_player]["status"] = "busted"
                        stats[current_player]["score"] = 0
                        print(dedent("BUSTED!"))
                    
                    else:
                        stats[current_player]["score"] += card
                        # if player has more than 200 points...
                        if self.win_check(current_player, stats[current_player]["score"]):
                            win_score = self.scores[current_player] + stats[current_player]["score"]
                            print_win_message(current_player, win_score)
                            return "GG"
                    
                    # add the card to the player's hand
                    stats[current_player]["hand"].append(card)
                    # If hand is now at 7 cards, apply 15 pt bonus and end round
                    if len(stats[current_player]["hand"]) >= 7:
                        stats[current_player]["score"] += 15
                        break
        
        round_status = "inactive"
        # print a summary of the round
        summary = print_round_summary(self.round, stats)

        # end the round and return stats
        return stats