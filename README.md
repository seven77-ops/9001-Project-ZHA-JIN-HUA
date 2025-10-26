# 9001-Project-ZHA-JIN-HUA
Sure 👍 Here’s a **clean, all-English version** of your `README.md` — well-structured and ready for GitHub or project submission.

---

# 🃏 Zha Jin Hua (Three-Card Brag) – Python CLI Game

---

## 📖 Introduction

**Zha Jin Hua** (also known as *Three-Card Brag*) is a fast-paced Chinese poker-style game.
Each player is dealt three cards and competes through betting, bluffing, and card comparison to win the pot.

This project is a **Python command-line implementation** of Zha Jin Hua built entirely with the standard library.
It features human-vs-AI gameplay, five bluffing speech options, and basic AI decision logic.

---

## 🎯 Objective

Win chips by either:

* Having the strongest hand, or
* Bluffing your opponents into folding.

The last player standing—or the one with the best hand at showdown—wins the pot.

---

## 🧩 Card Rankings

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

## 💬 Bluff System

After viewing your cards, you can choose one of five bluffing speech options to influence other players:

| Option | Behavior                                                 |
| ------ | -------------------------------------------------------- |
| 1      | **Boast** – act confident or intimidating                |
| 2      | **Act Disappointed** – pretend to have weak cards        |
| 3      | **Be Honest (Weak)** – sigh and admit a bad hand         |
| 4      | **Be Honest (Strong)** – sound confident with good cards |
| 5      | **Stay Silent** – say nothing                            |

AI opponents also make random comments based on their estimated hand strength, sometimes bluffing and sometimes being honest.

---

## 🕹️ Controls

| Key          | Action                             |
| ------------ | ---------------------------------- |
| **K**        | View your cards                    |
| **F**        | Fold                               |
| **C**        | Call (match the current bet)       |
| **R**        | Raise                              |
| **V**        | Compare (challenge another player) |
| **Ctrl + C** | Exit the game                      |

---

## ⚖️ Hand Comparison Rules

When two players compare hands:

1. Compare **hand type**
   (Three of a Kind > Straight Flush > Flush > Straight > Pair > High Card)
2. If the same type, compare the **main ranks** (e.g., higher straight or pair).
3. If still tied, compare **secondary ranks** (kickers).
4. If still tied, compare the **highest suit** (♠ > ♥ > ♣ > ♦).

---

## 🤖 Bot AI Logic

AI players estimate their hand strength and decide whether to:

* View cards or stay blind
* Fold, call, raise, or challenge another player
* Speak or stay silent, sometimes bluffing to mislead opponents

The AI uses a simplified decision model with random variation for realism.

---

## 💻 How to Run

### Method 1 – Direct Run

```bash
python zhajinhua_en.py
```

Then follow the on-screen prompts to:

* Choose the number of players
* Set initial chips, ante, and minimum bet
* Play interactively using keyboard input

---

## 📁 Project Structure

```
zhajinhua_en.py     # main program
README.md           # documentation
```

---

## 🧩 Tech Stack

* **Language:** Python 3.x
* **Libraries:** Standard Library only (no external dependencies)
* **Core Concepts:**

  * Classes and Objects
  * Loops and Conditionals
  * CLI Input/Output
  * Random Module
  * Simple AI Decision Logic
  * Bluff Simulation

---

## 🏆 Possible Improvements

* Add **game history** or save logs for replay
* Support **multiplayer online** mode (socket implementation)
* Create a **GUI version** (Tkinter or Pygame)
* Include **sound effects and animations**
* Improve **AI bluff logic** using probability modeling

---

## ⚠️ Disclaimer

This game is created **for educational and entertainment purposes only**.
Do **not** use it for gambling or monetary play.
Please play responsibly.

---

Would you like me to add a short **example gameplay transcript** (one round showing bluff dialogue and comparison) at the end of the README? It makes the project demo much more engaging.

