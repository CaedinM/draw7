from textwrap import dedent

def calculate_ev(deck: dict[int, int], drawn: list[int]) -> float:
    """
    Calculate the expected value of drawing an extra card given the
    cards that have already been drawn.
    """
    print(dedent("""
    Insights:"""))
    dupes_in_deck = sum([(deck[k]) for k in drawn])
    cards_in_deck = sum(deck.values())
    
    # probability of drawing a duplicate card
    p = dupes_in_deck / cards_in_deck
    print("* Chance of drawing a duplicate: ", str(round(p * 100, 2)) + "%")

    # calculate the expected value of drawing a non-duplicate card
    value_of_non_dupes_in_deck = sum([k * deck[k] for k in deck if k not in drawn])
    non_dupes_in_deck_count = sum([deck[k] for k in deck if k not in drawn])
    v = value_of_non_dupes_in_deck / non_dupes_in_deck_count

    # points accumulated so far in this turn
    s = sum(drawn)

    # calculate the expecte value of drawing the next card
    ev = ((1 - p) * v) + (p * (-s))
    print("* Expected value of hitting here: ", round(ev, 2))
    
    # return the expected value of drawing another card
    return ev
