from textwrap import dedent

def calculate_ev(deck: dict[int, int], drawn: list[int], bonuses: list[str]) -> float:
    """
    Calculate the expected value of drawing an extra card given the
    cards that have already been drawn.
    """
    print(dedent("""
    Insights:"""))
    dupes_in_deck = sum([(deck[k]) for k in drawn]) + sum([deck[i] for i in bonuses])
    cards_in_deck = sum(deck.values())
    
    # probability of drawing a duplicate card
    p = dupes_in_deck / cards_in_deck
    print("* Chance of drawing a duplicate: ", str(round(p * 100, 2)) + "%")

    # points accumulated so far in this turn
    s = sum(drawn) + sum([int(b[1:]) for b in bonuses if b[0] == "+"])
    if "2x" in bonuses:
        s = s * 2

    # calculate the expected value of drawing a non-duplicate card
    value_of_non_dupes_in_deck = 0
    for k in deck:
        if k in drawn or k in bonuses:
            continue
        if isinstance(k, int):
            value_of_non_dupes_in_deck += k * deck[k]
        elif isinstance(k, str):
            if k[0] == "+":
                value_of_non_dupes_in_deck += int(k[1:]) * deck[k]
            elif k[-1] == "x":
                value_of_non_dupes_in_deck += s
    # if the player has the 2x bonus, th value of every non-duplicate card in the deck doubles.
    if "2x" in bonuses:
        value_of_non_dupes_in_deck = value_of_non_dupes_in_deck * 2

    non_dupes_in_deck_count = sum([deck[k] for k in deck if k not in drawn and k not in bonuses])

    # if there have already been 6 cards drawn, drawing a non-dupe now carries an extra 15 point bonus (7 card bonus)
    if len(drawn) == 6:
        value_of_non_dupes_in_deck += 15 * non_dupes_in_deck_count


    # expected value of drawing a non-duplicate
    v = value_of_non_dupes_in_deck / non_dupes_in_deck_count

    # calculate the expected value of drawing the next card
    ev = ((1 - p) * v) + (p * (-s))
    print("* Expected value of hitting here: ", round(ev, 2))
    
    # return the expected value of drawing another card
    return ev
