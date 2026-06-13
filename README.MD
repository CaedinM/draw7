# Draw7

A terminal-based, press-your-luck card game for 2–8 players, written in pure Python with zero dependencies. Each round you decide whether to **hit** for more points or **stay** and lock in what you've got — but draw a duplicate and you bust, losing everything you earned that round. First player to **200 points** wins.

To help you make the call, Draw7 ships with a built-in **expected-value advisor** that crunches the live deck composition every turn and tells you whether hitting is statistically worth it.

---

> ### Built by hand, in one day
>
> This project was written **from scratch in one day**, and **no AI code-generation tools were used at any point** ...(except for writing this README)

---

## How to play

```bash
cd src
python main.py
```

You'll be asked how many players are playing (2–8) and prompted for each player's name. Then the rounds begin.

### Rules

- Every player starts each round with one card drawn automatically.
- On your turn you choose to **Hit (H)** to draw another card or **Stay (S)** to bank your current round score.
- Card values range from **0 to 12**. Higher cards are rarer in the deck than lower ones.
- **Draw a card you already hold and you BUST** — your score for the round drops to 0.
- Collect **7 cards in a single round** and you earn a **+15 point bonus**, ending the round.
- A round ends once every player has either stayed or busted.
- Round scores are added to your running total. The first player to reach **200 points** wins immediately.
- When the deck runs dry, busted players' cards are reshuffled back in from the discard pile.

### The deck

Lower cards are common, higher cards are scarce — which is exactly what makes the press-your-luck decision interesting:

| Card  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|-------|---|---|---|---|---|---|---|---|---|---|----|----|----|
| Count | 1 | 1 | 2 | 2 | 4 | 4 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |

## The EV advisor

Before each decision, Draw7 evaluates the current deck against your hand and reports:

- **Chance of drawing a duplicate** (the probability you bust on the next hit).
- **Expected value of hitting**, computed as:

  ```
  EV = (1 - p) * v  +  p * (-s)
  ```

  where `p` is the bust probability, `v` is the average value of the non-duplicate cards remaining in the deck, and `s` is the points you'd forfeit by busting.

If the EV is positive, it recommends **Hit**; otherwise it recommends **Stay**. The decision is still yours.

## Project layout

```
src/
├── main.py        # entry point and top-level game loop
├── gamestate.py   # Gamestate class: deck, discard pile, scores, round logic
├── helpers.py        # input prompts and ASCII/console rendering
└── ev_calculator.py   # expected-value calculator and insights
```

## Requirements

- Python 3.9+ (uses standard-library modules only: `random`, `itertools`, `statistics`, `textwrap`).
- No third-party packages. No installation step.
