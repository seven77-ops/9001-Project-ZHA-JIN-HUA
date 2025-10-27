# CLI Zha Jin Hua (Three-Card Brag) – standard library only + bluff/talk strategy
import random
from typing import List, Tuple, Optional

SUITS = ["♠", "♥", "♣", "♦"]  # suit order for tie-breaks (high to low)
RANKS = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
RANK_VALUE = {r:i for i,r in enumerate(RANKS, start=2)}  # 2->2 ... A->14
SUIT_VALUE = {"♠":4, "♥":3, "♣":2, "♦":1}                # used for final suit tie-break

# Hand types: bigger is stronger
HAND_TYPE = {
    "trips": 6,            # Three of a kind
    "straight_flush": 5,   # Straight flush
    "flush": 4,            # Flush
    "straight": 3,         # Straight
    "pair": 2,             # Pair
    "high": 1              # High card
}

class Card:
    def __init__(self, rank: str, suit: str):
        self.rank = rank
        self.suit = suit
    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(r,s) for s in SUITS for r in RANKS]
    def shuffle(self, seed: Optional[int]=None):
        if seed is not None:
            random.seed(seed)
        random.shuffle(self.cards)
    def deal(self, n:int) -> List[Card]:
        if len(self.cards) < n:
            raise RuntimeError("Not enough cards")
        hand = self.cards[:n]
        self.cards = self.cards[n:]
        return hand

def is_consecutive(vals: List[int]) -> bool:
    s = sorted(vals)
    if s[0]+1 == s[1] and s[1]+1 == s[2]:
        return True
    # Special case: A(14),2,3 treated as consecutive with A as 1
    if set(s) == {14,2,3}:
        return True
    return False

def normalize_straight(vals: List[int]) -> List[int]:
    # For comparing straights; A-2-3 is treated as the lowest straight
    s = sorted(vals, reverse=True)
    if set(vals) == {14,2,3}:   # A23
        return [3,2,1]
    return s

def hand_rank(cards: List[Card]) -> Tuple[int, List[int], List[int]]:
    """
    Returns a tuple used for comparison:
    (hand_type_strength, primary_keys(list), secondary_keys(list))
    Comparison:
      1) hand_type_strength
      2) primary_keys (lexicographic, desc)
      3) secondary_keys
      4) highest suit (as final tie-break)
    """
    ranks = [RANK_VALUE[c.rank] for c in cards]
    suits = [c.suit for c in cards]
    counts = {}
    for v in ranks:
        counts[v] = counts.get(v,0)+1
    unique = sorted(counts.items(), key=lambda x:(x[1], x[0]), reverse=True) # by freq then rank

    is_flush = len(set(suits)) == 1
    consec = is_consecutive(ranks)

    # Trips
    if 3 in counts.values():
        tval = unique[0][0]
        return (HAND_TYPE["trips"], [tval], sorted([v for v in ranks if v!=tval], reverse=True))
    # Straight flush
    if is_flush and consec:
        main = normalize_straight(ranks)
        return (HAND_TYPE["straight_flush"], main, [])
    # Flush
    if is_flush:
        return (HAND_TYPE["flush"], sorted(ranks, reverse=True), [])
    # Straight
    if consec:
        main = normalize_straight(ranks)
        return (HAND_TYPE["straight"], main, [])
    # Pair
    if 2 in counts.values():
        pair_val = [v for v,cnt in counts.items() if cnt==2][0]
        kicker = [v for v in ranks if v!=pair_val][0]
        return (HAND_TYPE["pair"], [pair_val, kicker], [])
    # High card
    return (HAND_TYPE["high"], sorted(ranks, reverse=True), [])

def highest_suit(cards: List[Card]) -> int:
    return max(SUIT_VALUE[c.suit] for c in cards)

def compare_hands(a: List[Card], b: List[Card]) -> int:
    """
    Compare two 3-card hands.
    Returns: 1 if a wins, -1 if b wins, 0 if perfectly tied.
    """
    ra = hand_rank(a)
    rb = hand_rank(b)
    if ra[0] != rb[0]:
        return 1 if ra[0] > rb[0] else -1
    # primary keys
    for x, y in zip(ra[1], rb[1]):
        if x != y:
            return 1 if x > y else -1
    # secondary keys
    for x, y in zip(ra[2], rb[2]):
        if x != y:
            return 1 if x > y else -1
    # final suit tie-break
    ha = highest_suit(a)
    hb = highest_suit(b)
    if ha != hb:
        return 1 if ha > hb else -1
    return 0

class Player:
    def __init__(self, name: str, chips: int, is_bot: bool):
        self.name = name
        self.chips = chips
        self.is_bot = is_bot
        self.alive = True        # not folded
        self.seen = False        # has viewed cards
        self.hand: List[Card] = []
        self.last_bluff_round = -1  # to avoid multiple speeches per round
    def __repr__(self):
        st = "BOT" if self.is_bot else "YOU"
        return f"{self.name}({st}) chips:{self.chips}"

class Table:
    def __init__(self, players: List[Player], ante: int=10, min_bet: int=10, max_rounds: int=3):
        self.players = players
        self.ante = ante
        self.min_bet = min_bet
        self.max_rounds = max_rounds
        self.deck = Deck()
        self.pot = 0
        self.cur_bet = min_bet
        self.last_raiser = None

    def collect_ante(self):
        for p in self.players:
            pay = min(self.ante, p.chips)
            p.chips -= pay
            self.pot += pay

    def active_players(self) -> List[Player]:
        return [p for p in self.players if p.alive and p.chips >= 0]

    def deal(self):
        self.deck = Deck()
        self.deck.shuffle()
        for p in self.players:
            p.hand = self.deck.deal(3)
            p.alive = True
            p.seen = False
            p.last_bluff_round = -1

    def show_state(self):
        print("\n==== Table ====")
        print(f"Pot: {self.pot} | Current call: {self.cur_bet}")
        for p in self.players:
            status = "In" if p.alive else "Folded"
            seen = "Seen" if p.seen else "Blind"
            me = " (You)" if not p.is_bot else ""
            print(f"- {p.name}{me}: chips {p.chips} | {status} | {seen}")
        print("================")

    # ------------------- Bluff system (Human) -------------------
    def choose_bluff_phrase(self, player: Player, round_idx: int):
        if not player.seen:
            return
        if player.last_bluff_round == round_idx:
            return  # already spoke this round
        print("\nChoose your speech (bluff) strategy:")
        options = [
            "Boast (intimidate others)",
            "Act disappointed (pretend weak)",
            "Be honest: sigh (weak hand)",
            "Be honest: confident (strong hand)",
            "Stay silent"
        ]
        for i, opt in enumerate(options, 1):
            print(f"{i}) {opt}")
        try:
            choice = int(input("Your choice (1-5): ").strip())
        except:
            choice = 5
        phrases = {
            1: "Haha, this hand is almost too good to play. 😏",
            2: "Sigh… luck’s not on my side today…",
            3: "Oh no… I can already tell this is bad.",
            4: "Is that it? Feels rock-solid to me. 😎",
            5: "(You chose to stay silent.)"
        }
        print(f"You say: {phrases.get(choice, '(Silence)')}")
        player.last_bluff_round = round_idx

    # ------------------- Bluff system (Bot) -------------------
    def bot_speak(self, bot: Player, strength: float, round_idx: int):
        if not bot.seen:
            return
        if bot.last_bluff_round == round_idx:
            return
        phrases_strong = [
            "Not bad at all, haha~ 😏",
            "Heh, this could be dangerous for you.",
            "Solid. Very solid.",
            "Don’t worry, my hand is just okay. 😌"
        ]
        phrases_weak = [
            "Hmm… a bit awkward.",
            "Uh-oh, that’s rough.",
            "Luck isn’t great today.",
            "(Silent smile.)"
        ]
        # Strong hand might pretend weak; weak might pretend strong
        if strength > 0.7:
            msg = random.choice(phrases_strong if random.random()>0.35 else phrases_weak)
        else:
            msg = random.choice(phrases_weak if random.random()>0.35 else phrases_strong)
        print(f"{bot.name} says: {msg}")
        bot.last_bluff_round = round_idx

    # ------------------- Turn flow -------------------
    def player_action(self, p: Player, round_idx: int):
        if not p.alive or p.chips <= 0:
            return

        if p.is_bot:
            self.bot_action(p, round_idx)
            return

        # Human player
        print(f"\nYour hand: {' '.join(map(str,p.hand)) if p.seen else '(Hidden – press K to view)'}")

        # If already seen, allow speech once per round
        if p.seen:
            self.choose_bluff_phrase(p, round_idx)

        while True:
            print(f"[F]old  [C]all({self.cur_bet})  [R]aise  [V] Compare  [K] View")
            cmd = input("Your move: ").strip().lower()
            if cmd == "k":
                if p.seen:
                    print("You have already viewed your cards.")
                else:
                    p.seen = True
                    print(f"You viewed: {' '.join(map(str,p.hand))}")
                    # allow speech right after viewing
                    self.choose_bluff_phrase(p, round_idx)
                continue
            elif cmd == "f":
                p.alive = False
                print("You folded.")
                return
            elif cmd == "c":
                self.call_bet(p)
                return
            elif cmd == "r":
                self.raise_bet(p)
                return
            elif cmd == "v":
                self.challenge_compare(p)
                return
            else:
                print("Invalid command. Try again.")

    def call_bet(self, p: Player):
        pay = min(self.cur_bet, p.chips)
        p.chips -= pay
        self.pot += pay
        print(f"{p.name} calls {pay}")

    def raise_bet(self, p: Player):
        max_raise = p.chips
        if max_raise < self.cur_bet:
            print("Not enough chips to raise. Calling instead.")
            self.call_bet(p)
            return
        try:
            amt = int(input(f"Raise to (>= {self.cur_bet}, <= {max_raise}): ").strip())
        except:
            print("Invalid input. Calling instead.")
            self.call_bet(p)
            return
        if amt < self.cur_bet:
            print("Too small to raise. Calling instead.")
            self.call_bet(p)
            return
        p.chips -= amt
        self.pot += amt
        self.cur_bet = amt
        self.last_raiser = p
        print(f"{p.name} raises to {amt}")

    def challenge_compare(self, attacker: Player):
        targets = [q for q in self.players if q.alive and q is not attacker]
        if not targets:
            print("No one to compare with. Action changed to Call.")
            self.call_bet(attacker)
            return
        for i, q in enumerate(targets, start=1):
            print(f"{i}) {q.name} {'(Blind)' if not q.seen else ''}")
        try:
            idx = int(input("Choose a player to compare with: ").strip())
            target = targets[idx-1]
        except:
            print("Invalid choice. Defaulting to the first one.")
            target = targets[0]

        cost = min(self.cur_bet, attacker.chips)
        attacker.chips -= cost
        self.pot += cost
        print(f"{attacker.name} challenges {target.name}! (Compare fee {cost})")
        self.reveal_and_eliminate(attacker, target)

    def reveal_and_eliminate(self, a: Player, b: Player):
        print(f"  {a.name} shows: {' '.join(map(str,a.hand))}")
        print(f"  {b.name} shows: {' '.join(map(str,b.hand))}")
        res = compare_hands(a.hand, b.hand)
        if res >= 0:
            print(f"  {a.name} wins. {b.name} is out.")
            b.alive = False
        else:
            print(f"  {b.name} wins. {a.name} is out.")
            a.alive = False

    # —— Bot logic (with bluff speech) ——
    def bot_action(self, p: Player, round_idx: int):
        strength = self.estimate_strength(p.hand)

        # Decide whether to view cards
        if not p.seen and (strength >= 0.75 or random.random() < 0.35):
            p.seen = True

        # If seen, speak once per round
        if p.seen:
            self.bot_speak(p, strength, round_idx)

        # Very simple strategy
        action = "call"
        if strength >= 0.9 and p.chips >= self.cur_bet*2 and random.random() < 0.7:
            action = "raise"
        elif strength <= 0.25 and random.random() < 0.5:
            action = "fold"
        elif strength >= 0.6 and random.random() < 0.2 and len(self.active_players())>=2:
            action = "compare"

        if action == "fold":
            p.alive = False
            print(f"{p.name} folds.")
        elif action == "raise":
            amt = min(max(self.cur_bet*2, self.cur_bet), p.chips)
            if amt <= 0:
                self.call_bet(p)
                return
            p.chips -= amt
            self.pot += amt
            self.cur_bet = amt
            self.last_raiser = p
            print(f"{p.name} raises to {amt}")
        elif action == "compare":
            targets = [q for q in self.players if q.alive and q is not p]
            human = [q for q in targets if not q.is_bot]
            target = human[0] if human else random.choice(targets)
            cost = min(self.cur_bet, p.chips)
            p.chips -= cost
            self.pot += cost
            print(f"{p.name} challenges {target.name}! (Compare fee {cost})")
            self.reveal_and_eliminate(p, target)
        else:
            self.call_bet(p)

    def estimate_strength(self, hand: List[Card]) -> float:
        t, main, _ = hand_rank(hand)
        base = {HAND_TYPE["high"]:0.35, HAND_TYPE["pair"]:0.6,
                HAND_TYPE["straight"]:0.75, HAND_TYPE["flush"]:0.78,
                HAND_TYPE["straight_flush"]:0.92, HAND_TYPE["trips"]:0.98}[t]
        hi = max(RANK_VALUE[c.rank] for c in hand)
        bonus = (hi-6)/10.0  # 6..14 => ~0..0.8 -> scaled lightly
        return max(0.0, min(1.0, base + bonus*0.1))

    def settle(self):
        alive = [p for p in self.players if p.alive]
        if len(alive) == 1:
            winner = alive[0]
            winner.chips += self.pot
            print(f"\n*** {winner.name} wins the pot {self.pot} ***")
        else:
            print("\n--- Showdown ---")
            best = None
            winners = []
            for p in alive:
                print(f"{p.name}: {' '.join(map(str,p.hand))}")
                r = hand_rank(p.hand)
                tup = (r, highest_suit(p.hand))
                if (best is None) or (tup > best):
                    best = tup
                    winners = [p]
                elif tup == best:
                    winners.append(p)
            share = self.pot // len(winners)
            for w in winners:
                w.chips += share
            names = ", ".join(p.name for p in winners)
            print(f"*** Winner(s): {names}, each receives {share} ***")

    def play_hand(self):
        self.pot = 0
        self.cur_bet = self.min_bet
        self.last_raiser = None
        self.deal()
        self.collect_ante()
        print("\n================= New Hand =================")
        self.show_state()

        for r in range(1, self.max_rounds + 1):
            print(f"\n— Round {r} —")
            for p in self.players:
                if len(self.active_players()) <= 1:
                    break
                if not p.alive or p.chips <= 0:
                    continue
                self.player_action(p, r)
                if len(self.active_players()) <= 1:
                    break

            self.show_state()

            # >>> 新增：每轮结束后的“按 Enter 进入下一轮” <<<
            if len(self.active_players()) > 1 and r < self.max_rounds:
                input("\n[Press Enter] to start the next round...")

            if len(self.active_players()) <= 1:
                break

        self.settle()


def ask_int(prompt: str, low: int, high: int, default: Optional[int]=None) -> int:
    while True:
        s = input(f"{prompt} ").strip()
        if not s and default is not None:
            return default
        try:
            v = int(s)
            if low <= v <= high:
                return v
        except:
            pass
        print(f"Please enter an integer between {low} and {high}.")

def main():
    print("=== Zha Jin Hua ===")
    n = ask_int("Total players (2–6, incl. you):", 2, 6, 3)
    bots = max(0, n-1)
    init_chips = ask_int("Initial chips per player (>=100 suggested):", 20, 100000, 200)
    ante = ask_int("Ante (suggest 5–20):", 1, 1000, 10)
    min_bet = ask_int("Minimum call (suggest 10–50):", 1, 10000, 20)
    max_rounds = ask_int("Max betting rounds (1–5):", 1, 5, 3)

    players: List[Player] = []
    players.append(Player("You", init_chips, is_bot=False))
    for i in range(bots):
        players.append(Player(f"Bot{i+1}", init_chips, is_bot=True))

    table = Table(players, ante=ante, min_bet=min_bet, max_rounds=max_rounds)

    while True:
        rich = [p for p in table.players if p.chips > 0]
        if len(rich) < 2:
            alive = rich[0] if rich else None
            if alive:
                print(f"\nGame over! {alive.name} takes all the chips.")
            else:
                print("\nGame over! Everyone is broke (?!).")
            break
        table.play_hand()
        print("\n--- End of hand. Balances ---")
        for p in table.players:
            print(f"{p.name}: {p.chips}")
        go = input("\nPlay another hand? (Y/n): ").strip().lower()
        if go == "n":
            print("Thanks for playing. Play responsibly!")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited.")
