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
- Number cards range from **0 to 12**. Higher cards are rarer in the deck than lower ones.
- **Draw a card you already hold and you BUST** — your score for the round drops to 0. This applies to bonus cards too: a second copy of a bonus you already hold busts you.
- Collect **7 number cards in a single round** and you earn a **+15 point bonus**, ending the round. (Bonus cards don't count toward this total.)
- A round ends once every player has either stayed or busted.
- Round scores are added to your running total. The first player to reach **200 points** wins immediately.
- When the deck runs dry, busted players' cards are reshuffled back in from the discard pile.

### Bonus cards

Mixed into the deck alongside the number cards are six special cards that change how points accumulate:

- **`+2`, `+4`, `+6`, `+8`, `+10`** — add their face value straight to your round score. They live in a separate "bonus" pile and do **not** count toward the 7-card hand.
- **`2x`** — doubles your current round score the moment you draw it, and **doubles the value of every card you draw afterward** for the rest of the round.

Because each special card is unique, drawing one twice busts you just like a duplicate number.

### The deck

Lower numbers are common, higher numbers are scarce — which is exactly what makes the press-your-luck decision interesting. The card's count equals its face value (with `0` and `1` both appearing once):

| Card  | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|-------|---|---|---|---|---|---|---|---|---|---|----|----|----|
| Count | 1 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |

The six bonus cards (`+2`, `+4`, `+6`, `+8`, `+10`, `2x`) each appear exactly once.

## The EV advisor

Before each decision, Draw7 evaluates the current deck against your hand and reports the chance of busting and the expected value of hitting.

Let $\mathrm{deck}[k]$ be the number of copies of card $k$ left in the deck, let $H$ be the set of cards (number **and** bonus) you already hold, and let $N = \sum_k \mathrm{deck}[k]$ be the total cards remaining.

**Bust probability** — the chance your next draw duplicates something you hold:

$$p = \frac{\sum_{k \in H} \mathrm{deck}[k]}{N}$$

**The `2x` multiplier** applied throughout, depending on whether you hold the `2x` bonus:

$$m = \begin{cases} 2 & \text{if you hold } \texttt{2x} \\ 1 & \text{otherwise} \end{cases}$$

**Points at risk** ($s$) — everything you forfeit if you bust:

$$s = m\left(\sum_{c \,\in\, \text{hand}} c \;+\; \sum_{+j \,\in\, \text{bonuses}} j\right)$$

**Value of a candidate card** ($\mathrm{val}$) — how much drawing card $k$ would add. Drawing `2x` doubles your banked score, so its value is the current $s$:

$$\mathrm{val}(k) = \begin{cases} k & k \text{ is a number card} \\ j & k \text{ is a +j bonus card} \\ s & k \text{ is the 2x multiplier bonus card} \end{cases}$$

**Expected value of a non-duplicate draw** ($v$), summed over the cards $k \notin H$ you don't already hold, where $n = \sum_{k \,\notin\, H} \mathrm{deck}[k]$ is the number of such cards:

$$v = \frac{\, m\left(\sum_{k \,\notin\, H} \mathrm{val}(k)\,\mathrm{deck}[k]\right) \;+\; 15\,n\cdot\mathbf{1}\!\left[\,|\text{hand}| = 6\,\right]\,}{n}$$

The $\mathbf{1}[\,|\text{hand}| = 6\,]$ term is the seven-card bonus: only when you already hold six number cards does every non-duplicate outcome carry the extra **+15** for completing a seven-card hand.

**Overall expected value of hitting:**

$$\mathrm{EV} = (1-p)\,v \;-\; p\,s$$

If $\mathrm{EV} > 0$ it recommends **Hit**; otherwise it recommends **Stay**. The decision is still yours.

### How the bonus cards change the math

The advisor doesn't just count number cards — it prices in every special card currently live in the deck and every bonus already in your hand:

- **Bust probability (`p`)** includes duplicate bonus cards. If you already hold `+6`, the second `+6` in the deck counts toward your chance of busting.
- **Points at risk (`s`)** sums your number cards *plus* the value of any `+N` bonuses you hold, and is doubled if you're holding `2x`. Drawing `2x` makes your whole round score the stake.
- **Expected value of a non-duplicate (`v`)** values a `+N` card at `N`, and values the `2x` card at your current score `s` (since drawing it doubles what you've banked). If you already hold `2x`, every prospective draw is worth double, so `v` is doubled to match.

### Why it's greedy

The advisor only looks **one card ahead** — it maximizes the expected value of the *next* draw, not the round. The clearest symptom is the **+15 seven-card bonus**: that reward only enters the calculation once you're already holding **six** number cards (i.e. on the decision for your potential seventh card). Every earlier hit is priced as if the +15 didn't exist.

So the recommendation never *plans toward* the seven-card bonus. A human who can see they're four cards away from +15 might reasonably keep hitting to chase it; the advisor won't suggest that until the bonus is one card away. It's a deliberately simple, myopic heuristic — accurate for the immediate decision, blind to multi-card strategy.

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
