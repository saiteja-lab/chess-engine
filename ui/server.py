from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

# Add engine to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from engine.board import Board, WHITE, BLACK, PIECE_STR
from engine.search import search
from engine.move import Move

app = Flask(__name__)
CORS(app)

# Global board instance
board = Board()

def get_fen(board):
    """Convert board to FEN string"""
    rows = []
    for r in range(8):
        empty = 0
        row_str = ""
        for f in range(8):
            idx = r * 8 + f
            p = board.squares[idx]
            if p == 0:
                empty += 1
            else:
                if empty > 0:
                    row_str += str(empty)
                    empty = 0
                row_str += PIECE_STR[p]
        if empty > 0:
            row_str += str(empty)
        rows.append(row_str)
        
    fen = "/".join(rows)
    turn = 'w' if board.turn == WHITE else 'b'
    return f"{fen} {turn} - - 0 1"

@app.route('/api/new_game', methods=['POST'])
def new_game():
    """Start a new game"""
    global board
    board = Board()
    return jsonify({
        'fen': get_fen(board), 
        'turn': 'white'
    })

@app.route('/api/move', methods=['POST'])
def make_move():
    """Make a move and get engine response"""
    global board
    data = request.json
    move_uci = data.get('move')
    
    if not move_uci:
        return jsonify({'error': 'No move provided'}), 400
    
    # User move
    legal_moves = board.generate_moves()
    found = False
    for m in legal_moves:
        if m.to_uci() == move_uci:
            board.make_move(m)
            found = True
            break
            
    if not found:
        return jsonify({
            'error': 'Illegal move', 
            'fen': get_fen(board)
        }), 400
        
    # Check if game over after user move
    if not board.generate_moves():
        return jsonify({
            'fen': get_fen(board), 
            'game_over': True, 
            'winner': 'user',
            'engine_move': None
        })

    # Engine move
    try:
        best_move = search(board, 3, 2.0)
        if best_move:
            board.make_move(best_move)
            engine_move = best_move.to_uci()
        else:
            engine_move = None
    except Exception as e:
        print(f"Error during search: {e}")
        engine_move = None
        
    return jsonify({
        'fen': get_fen(board),
        'engine_move': engine_move,
        'game_over': engine_move is None
    })

if __name__ == '__main__':
    print("🚀 Starting Chess Engine Server...")
    print("📡 Server running on http://localhost:5000")
    print("✅ CORS enabled for frontend")
    app.run(port=5000, debug=True)
