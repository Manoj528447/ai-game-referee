"""
Rock–Paper–Scissors–Plus Game

Rules:
- Best of 3 rounds
- Valid moves: rock, paper, scissors, bomb
- Bomb can be used only once per player
- Bomb beats all moves
- Bomb vs Bomb is a draw
- Invalid input consumes the round
- Game ends automatically after 3 rounds
"""

import random
from google.adk import tool   

# ---------------------------
# GAME STATE
# ---------------------------

game_state = {
    "round": 1,
    "max_rounds": 3,
    "user_score": 0,
    "bot_score": 0,
    "user_bomb_used": False,
    "bot_bomb_used": False,
    "game_over": False
}

# ---------------------------
# TOOL 1: VALIDATE MOVE
# ---------------------------

@tool
def validate_move(move: str, player: str, state: dict) -> dict:
    """
    Validates a move and enforces bomb usage rules.
    """
    valid_moves = ["rock", "paper", "scissors", "bomb"]

    if move not in valid_moves:
        return {"valid": False, "error": "Invalid move"}

    if move == "bomb":
        if player == "user" and state["user_bomb_used"]:
            return {"valid": False, "error": "User already used bomb"}
        if player == "bot" and state["bot_bomb_used"]:
            return {"valid": False, "error": "Bot already used bomb"}

    return {"valid": True, "error": None}

# ---------------------------
# TOOL 2: RESOLVE ROUND
# ---------------------------

@tool
def resolve_round(user_move: str, bot_move: str) -> dict:
    """
    Resolves a round and decides the winner.
    """
    if user_move == bot_move:
        return {"winner": "draw", "reason": "Same move played"}

    if user_move == "bomb" and bot_move != "bomb":
        return {"winner": "user", "reason": "Bomb beats everything"}

    if bot_move == "bomb" and user_move != "bomb":
        return {"winner": "bot", "reason": "Bomb beats everything"}

    wins = {
        "rock": "scissors",
        "scissors": "paper",
        "paper": "rock"
    }

    if wins[user_move] == bot_move:
        return {"winner": "user", "reason": f"{user_move} beats {bot_move}"}
    else:
        return {"winner": "bot", "reason": f"{bot_move} beats {user_move}"}

# ---------------------------
# TOOL 3: UPDATE GAME STATE
# ---------------------------

@tool
def update_game_state(state: dict, user_move: str, bot_move: str, result: dict) -> dict:
    """
    Mutates game state safely.
    """
    if user_move == "bomb":
        state["user_bomb_used"] = True

    if bot_move == "bomb":
        state["bot_bomb_used"] = True

    if result["winner"] == "user":
        state["user_score"] += 1
    elif result["winner"] == "bot":
        state["bot_score"] += 1

    state["round"] += 1

    if state["round"] > state["max_rounds"]:
        state["game_over"] = True

    return state

# ---------------------------
# RESPONSE / UI LAYER
# ---------------------------

def explain_rules():
    print("Welcome to Rock–Paper–Scissors–Plus!")
    print("Best of 3 rounds.")
    print("Moves: rock, paper, scissors, bomb (once per game).")
    print("Bomb beats everything. Invalid input wastes the round.")
    print("Game ends automatically after 3 rounds.\n")

# ---------------------------
# MAIN GAME LOOP
# ---------------------------

def play_game():
    global game_state
    explain_rules()

    while not game_state["game_over"]:
        print(f"Round {game_state['round']} / {game_state['max_rounds']}")

        user_move = input("Enter your move: ").strip().lower()

        user_check = validate_move(user_move, "user", game_state)

        # Invalid input → round wasted (NO forced bot win)
        if not user_check["valid"]:
            print(f"Invalid move: {user_check['error']}")
            result = {"winner": "draw", "reason": "Invalid input, round wasted"}
            bot_move = "none"
        else:
            # Bot move selection (bomb only if allowed)
            bot_choices = ["rock", "paper", "scissors"]
            if not game_state["bot_bomb_used"]:
                bot_choices.append("bomb")

            bot_move = random.choice(bot_choices)

            result = resolve_round(user_move, bot_move)

        # Update state ONLY via tool
        game_state = update_game_state(game_state, user_move, bot_move, result)

        # Explicit round feedback
        print(f"You played: {user_move}")
        print(f"Bot played: {bot_move}")
        print(f"Round winner: {result['winner']}")
        print(f"Reason: {result['reason']}")
        print(f"Score → You: {game_state['user_score']} | Bot: {game_state['bot_score']}\n")

    # Final result
    print("GAME OVER")
    if game_state["user_score"] > game_state["bot_score"]:
        print("🏆 Final Result: You win!")
    elif game_state["user_score"] < game_state["bot_score"]:
        print("🤖 Final Result: Bot wins!")
    else:
        print("🤝 Final Result: Draw!")

# ---------------------------
# ENTRY POINT
# ---------------------------

if __name__ == "__main__":
    play_game()

