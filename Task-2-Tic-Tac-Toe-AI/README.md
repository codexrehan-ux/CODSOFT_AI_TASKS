# Task 2 — Tic-Tac-Toe AI

## CodSoft Artificial Intelligence Internship

### Objective

Build an AI agent that plays Tic-Tac-Toe against a human player. The AI uses the Minimax algorithm to evaluate possible moves and choose an optimal move.

### Features

- Human vs AI gameplay
- Human plays as `X`
- AI plays as `O`
- Minimax decision-making algorithm
- Win, loss, and draw detection
- Invalid input and occupied-position handling
- Terminal-based interface

### Technology

- Python 3
- Standard Python library only

### How the AI Works

The Minimax algorithm recursively explores possible future game states.

- The AI tries to maximize its score.
- The human player is treated as the minimizing player.
- An AI win receives a positive score.
- A human win receives a negative score.
- A draw receives a score of zero.

The AI then chooses the available move with the best score.

### How to Run

Make sure Python 3 is installed, then run:

```bash
python tic_tac_toe.py
```

Enter moves using row and column numbers from 1 to 3. For example:

```text
Enter your move (row column): 2 3
```

### Project Requirement

This project is completed as Task 2 of the CodSoft Artificial Intelligence internship.
