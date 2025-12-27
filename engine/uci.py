import sys
from .board import Board
from .move import Move
from .search import search

def uci_loop():
    board = Board()
    
    while True:
        try:
            line = sys.stdin.readline()
            if not line: break
            line = line.strip()
        except EOFError:
            break
            
        parts = line.split()
        if not parts: continue
        
        cmd = parts[0]
        
        if cmd == "uci":
            print("id name SimpleChessEngine")
            print("id author Antigravity")
            print("uciok")
            sys.stdout.flush()
        elif cmd == "isready":
            print("readyok")
            sys.stdout.flush()
        elif cmd == "position":
            # position startpos moves e2e4 ...
            # position fen ... moves ...
            idx = 1
            if parts[idx] == "startpos":
                board = Board()
                idx += 1
            elif parts[idx] == "fen":
                # Find 'moves' to know where fen ends
                if "moves" in parts:
                    moves_idx = parts.index("moves")
                    fen_parts = parts[idx+1:moves_idx]
                    idx = moves_idx
                else:
                    fen_parts = parts[idx+1:]
                    idx = len(parts)
                
                fen = " ".join(fen_parts)
                board = Board(fen)
            
            if idx < len(parts) and parts[idx] == "moves":
                for m_str in parts[idx+1:]:
                    legal_moves = board.generate_moves()
                    found = False
                    for lm in legal_moves:
                        if lm.to_uci() == m_str:
                            board.make_move(lm)
                            found = True
                            break
                    if not found:
                        # Fallback: create move from UCI and trust it (risky but keeps it moving)
                        # This happens if our generator misses something or promotion syntax differs
                        m = Move.from_uci(m_str)
                        board.make_move(m)

        elif cmd == "go":
            depth = 3
            if "depth" in parts:
                depth = int(parts[parts.index("depth") + 1])
            
            # Simple time management
            time_limit = 5.0
            if "movetime" in parts:
                time_limit = int(parts[parts.index("movetime") + 1]) / 1000.0
            
            best_move = search(board, depth, time_limit)
            if best_move:
                print(f"bestmove {best_move.to_uci()}")
            else:
                # Should not happen unless mate/stalemate
                print("bestmove 0000")
            sys.stdout.flush()
            
        elif cmd == "quit":
            break

if __name__ == "__main__":
    uci_loop()
