# AI Game Referee – Rock–Paper–Scissors–Plus

## Overview
This project implements a minimal AI game referee that runs a short game of
Rock–Paper–Scissors–Plus between a user and a bot. The referee is responsible
for enforcing game rules, validating inputs, tracking state across turns, 
and providing clear round-by-round feedback in a conversational loop.

The focus of the implementation is correctness, clean state management, and
clear separation of responsibilities using tool-based abstractions.

## Game Rules
- The game is best of 3 rounds
- Valid moves: rock, paper, scissors, bomb
- Each player may use bomb only once per game
- Bomb beats all other moves
- Bomb vs bomb results in a draw
- Invalid input consumes the round
- The game ends automatically after 3 rounds

## State Model
The game maintains a single in-memory state object that persists across turns.
The state tracks:
- Current round number
- Maximum number of rounds
- User score and bot score
- Bomb usage flags for both players
- Game-over indicator

This ensures that game state is not stored in the prompt and remains consistent
across turns, making all game decisions deterministic and rule-compliant.

## Agent and Tool Design
The solution follows a tool-based architecture inspired by Google ADK concepts,
with clear separation of concerns:

- validate_move:
  Validates user and bot moves and enforces bomb usage constraints.

- resolve_round:
  Applies game rules to determine the winner of a round and provides an
  explanation.

- update_game_state:
  Mutates the game state by updating scores, round count, bomb usage, and
  end-of-game status.

State mutation occurs only through tools, keeping validation, game logic, and
state updates separate from response generation.

## Tradeoffs
- Bot move selection is random for simplicity.
- A single-agent design was chosen instead of multiple agents to keep the
  solution minimal and focused on correctness.
- Input validation is strict to avoid ambiguous behavior.

## Testing
The game was tested locally using a command-line conversational loop.

Google ADK is not publicly available for local installation. For local testing,
ADK decorators can be temporarily disabled without affecting the core logic.
All edge cases were tested, including invalid input handling, bomb usage limits,
draw scenarios, and automatic game termination.

## Future Improvements
- Smarter bot strategy based on game history
- Input normalization for common variations
- Ability to replay a new game without restarting the program
- Richer conversational responses
