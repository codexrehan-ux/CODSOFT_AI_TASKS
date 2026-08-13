"""CodSoft AI Internship Portfolio Web App.

Browser-based demos for the three completed CodSoft AI internship tasks.
The web UI is an optional portfolio enhancement; the original CLI projects remain intact.
"""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

from flask import Flask, jsonify, render_template, request

ROOT = Path(__file__).resolve().parent


def load_module(name, relative_path):
    path = ROOT / relative_path
    spec = spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Unable to load {relative_path}")
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


chatbot = load_module("chatbot", "Task-1-Rule-Based-Chatbot/chatbot.py")
tictactoe = load_module("tictactoe", "Task-2-Tic-Tac-Toe-AI/tic_tac_toe.py")
recommender = load_module("recommender", "Task-4-Recommendation-System/recommendation_system.py")

app = Flask(__name__)


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/api/chat")
def api_chat():
    data = request.get_json(silent=True) or {}
    message = str(data.get("message", "")).strip()
    if not message:
        return jsonify(error="Please enter a message."), 400
    return jsonify(response=chatbot.get_response(message))


@app.post("/api/tictactoe")
def api_tictactoe():
    data = request.get_json(silent=True) or {}
    incoming = data.get("board", [])
    if not isinstance(incoming, list) or len(incoming) != 9:
        return jsonify(error="Invalid board."), 400
    if any(cell not in {"X", "O", " "} for cell in incoming):
        return jsonify(error="Invalid board values."), 400

    x_count, o_count = incoming.count("X"), incoming.count("O")
    if x_count != o_count + 1:
        return jsonify(error="Invalid turn state."), 400

    board = [incoming[i:i + 3] for i in range(0, 9, 3)]
    winner = tictactoe.check_winner(board)
    if winner or not tictactoe.available_moves(board):
        return jsonify(board=incoming, message="Game over. Start a new game.", game_over=True)

    move = tictactoe.best_ai_move(board)
    if move:
        board[move[0]][move[1]] = tictactoe.AI

    winner = tictactoe.check_winner(board)
    if winner == tictactoe.AI:
        message = "AI wins. Better luck next time!"
        game_over = True
    elif winner == tictactoe.HUMAN:
        message = "Congratulations! You won!"
        game_over = True
    elif not tictactoe.available_moves(board):
        message = "It's a draw!"
        game_over = True
    else:
        message = "Your turn — choose a square."
        game_over = False
    return jsonify(board=sum(board, []), message=message, game_over=game_over)


@app.get("/api/movies")
def api_movies():
    return jsonify(movies=[movie["title"] for movie in recommender.MOVIES])


@app.post("/api/recommend")
def api_recommend():
    data = request.get_json(silent=True) or {}
    title = str(data.get("title", "")).strip()
    if not title:
        return jsonify(recommendations=[], error="Please select a movie."), 400
    selected, results = recommender.recommend(title)
    if selected is None:
        return jsonify(recommendations=[], error="Movie not found."), 404
    return jsonify(
        selected=selected["title"],
        recommendations=[
            {"title": movie_title, "score": f"{score:.2f}"}
            for score, movie_title in results
        ],
    )


if __name__ == "__main__":
    app.run(debug=True)
