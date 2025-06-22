from flask import Flask, request, jsonify
from flask_cors import CORS

from ai.minimax import minimax
# from ai.utils import apply_move  # Assumes you have a helper to apply a move
from ai.heuristic import heuristic

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains


@app.route("/move", methods=["POST"])
def get_ai_move():
    data = request.get_json()
    board = data["board"]
    player = data.get("player", 1)  # Default to black (1)

    # Call your existing search algorithm
    _, best_move = minimax(
        board,
        depth=3,  # Adjust depth as needed
        alpha=float("-inf"),
        beta=float("inf"),
        maximizing=True,
        player=player,
        evaluate=heuristic,
    )

    return jsonify({"move": best_move})


if __name__ == "__main__":
    app.run(host='127.0.0.1', debug=True, port=5050)  # Change port if needed
