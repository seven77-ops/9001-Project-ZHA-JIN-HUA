# 9001-Project-ZHA-JIN-HUA


#  Zha Jin Hua (Three-Card Brag) – Python CLI Game

---

##  Introduction

**Zha Jin Hua** (also known as *Three-Card Brag*) is a fast-paced Chinese poker-style game.
Each player is dealt three cards and competes through betting, bluffing, and card comparison to win the pot.

This project is a **Python command-line version** of Zha Jin Hua built entirely with the standard library.
It features **human vs computer gameplay**, five bluffing speech options, and smart computer decision-making.

---

##  Objective

Win chips by either:

* Having the strongest hand, or
* Bluffing your opponents into folding.

The last player standing—or the one with the best hand at showdown—wins the pot.

---

##  Card Rankings

| Rank                        | Description                                                  |
| --------------------------- | ------------------------------------------------------------ |
| **Three of a Kind (Trips)** | Three cards of the same rank                                 |
| **Straight Flush**          | Three consecutive cards of the same suit                     |
| **Flush**                   | Three cards of the same suit (not consecutive)               |
| **Straight**                | Three consecutive cards of mixed suits (A-2-3 is the lowest) |
| **Pair**                    | Two cards of the same rank                                   |
| **High Card**               | None of the above                                            |

**Notes:**

* Rank order: 2 < 3 < … < 10 < J < Q < K < A
* **A-2-3** counts as the **lowest straight**.
* If both hands are identical in rank and numbers, the **highest suit** decides the winner (♠ > ♥ > ♣ > ♦).

---

##  Bluff System

After viewing your cards, you can choose one of five bluffing speech options to influence other players:

| Option | Behavior                                                 |
| ------ | -------------------------------------------------------- |
| 1      | **Boast** – act confident or intimidating                |
| 2      | **Act Disappointed** – pretend to have weak cards        |
| 3      | **Be Honest (Weak)** – sigh and admit a bad hand         |
| 4      | **Be Honest (Strong)** – sound confident with good cards |
| 5      | **Stay Silent** – say nothing                            |

Computer players also make random comments based on their hand strength, sometimes bluffing and sometimes being honest.

---

##  Controls

| Key          | Action                             |
| ------------ | ---------------------------------- |
| **K**        | View your cards                    |
| **F**        | Fold                               |
| **C**        | Call (match the current bet)       |
| **R**        | Raise                              |
| **V**        | Compare (challenge another player) |
| **Ctrl + C** | Exit the game                      |

---

##  Hand Comparison Rules

When two players compare hands:

1. Compare **hand type**
   (Three of a Kind > Straight Flush > Flush > Straight > Pair > High Card)
2. If the same type, compare the **main ranks** (e.g., higher straight or pair).
3. If still tied, compare **secondary ranks** (kickers).
4. If still tied, compare the **highest suit** (♠ > ♥ > ♣ > ♦).

---

##  Computer Logic

Computer opponents estimate their hand strength and decide whether to:

* View cards or stay blind
* Fold, call, raise, or challenge another player
* Speak or stay silent, sometimes bluffing to mislead the player

The computer uses a simplified decision model with random variation for realism.

---

##  How to Run

### Method 1 – Direct Run

```bash
python zhajinhua_en.py
```

Then follow the on-screen prompts to:

* Choose the number of players
* Set initial chips, ante, and minimum bet
* Play interactively using keyboard input

---

##  Project Structure

```
zhajinhua_en.py     # main program
README.md           # documentation
```

---

## ⚠️ Disclaimer

This game is created **for educational and entertainment purposes only**.
Do **not** use it for gambling or monetary play.
Please play responsibly.
