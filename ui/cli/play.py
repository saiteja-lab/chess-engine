import sys
import os

# Add engine to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from engine.board import Board, WHITE
from engine.search import search
from engine.move import Move

def main():
    board = Board()
    
    while True:
        print("\n" + "="*20)
        board.print_board()
        print("="*20)
        
        if board.turn == WHITE: # User plays White
            move_str = input("Your move (e.g. e2e4): ")
            if move_str == "quit": break
            
            # Validate
            legal_moves = board.generate_moves()
            found = False
            for m in legal_moves:
                if m.to_uci() == move_str:
                    board.make_move(m)
                    found = True
                    break
            if not found:
                print(f"Illegal move! Available: {[m.to_uci() for m in legal_moves[:5]]}...")
                continue
        else:
            print("Engine thinking...")
            best_move = search(board, 3)
            if best_move:
                print(f"Engine played: {best_move.to_uci()}")
                board.make_move(best_move)
            else:
                print("Game over?")
                break

if __name__ == "__main__":
    main()
