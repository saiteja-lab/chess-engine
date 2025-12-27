import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from engine.board import Board, WHITE, BLACK
from engine.move import Move

def test_initial_moves():
    b = Board()
    moves = b.generate_moves()
    # 20 moves for white (16 pawn moves + 4 knight moves)
    assert len(moves) == 20

def test_simple_capture():
    b = Board("rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
    # White to move. e4 pawn can capture d5.
    moves = b.generate_moves()
    captures = [m for m in moves if b.squares[m.end] != 0] # This check is tricky because squares is updated on make_move
    # But generate_moves doesn't change board.
    # We can check target square content.
    
    # Actually, generate_moves returns moves. We need to check if any move lands on d5 (index 27)
    # d5 is rank 3 (0-7 from top? No, rank 5).
    # My board: rank 0 is top.
    # d5: file d (3), rank 5 (from 1). So rank index 3 (8-5=3).
    # index = 3*8 + 3 = 27.
    
    capture_found = False
    for m in moves:
        if m.end == 27:
            capture_found = True
            break
    assert capture_found

def test_fools_mate():
    # White is mated
    b = Board("rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 2")
    moves = b.generate_moves()
    assert len(moves) == 0
