from ev_calculator import calculate_ev

def ev_calc_test():
    deck = {0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:9, 11:11, 12:12, "+2":1, "+4":0, "+6":1, "+8":1, "+10":1, "2x": 0}
    hand = [10]
    bonuses = ["2x", "+4"]
    return calculate_ev(deck, hand, bonuses)

def bonus_applied_test():
    deck = {0:1, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:9, 11:11, 12:12, "+2":1, "+4":0, "+6":1, "+8":1, "+10":1, "2x": 0}
    hand = [10]
    bonuses = ["2x", "+4"]
    return calculate_ev(deck, hand, bonuses)

def six_card_test():
    deck = {0:0, 1:1, 2:1, 3:2, 4:4, 5:4, 6:6, 7:6, 8:7, 9:9, 10:9, 11:11, 12:12, "+2":1, "+4":0, "+6":1, "+8":1, "+10":1, "2x": 0}
    hand = [10, 2, 5, 7, 3, 0]
    bonuses = ["+4", "2x"]
    return calculate_ev(deck, hand, bonuses)

def five_card_test():
    deck = {0:1, 1:1, 2:1, 3:2, 4:4, 5:4, 6:6, 7:6, 8:8, 9:9, 10:9, 11:11, 12:12, "+2":1, "+4":0, "+6":1, "+8":1, "+10":1, "2x": 0}
    hand = [10, 2, 5, 7, 3]
    bonuses = ["+4", "2x"]
    return calculate_ev(deck, hand, bonuses)