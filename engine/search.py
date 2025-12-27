import time
from .eval import evaluate
from .board import WHITE, BLACK

INF = 1000000

# Transposition Table
tt = {}

def clear_tt():
    global tt
    tt = {}

def search(board, max_depth, time_limit=5.0):
    best_move = None
    start_time = time.time()
    
    print(f"Starting search to depth {max_depth}...")
    
    for depth in range(1, max_depth + 1):
        # Check time
        if time.time() - start_time > time_limit:
            break
            
        score, move = root_search(board, depth, -INF, INF)
        best_move = move
        print(f"Depth {depth}: Score {score}, Best Move {move}")
        
    return best_move

def root_search(board, depth, alpha, beta):
    best_move = None
    best_score = -INF
    
    moves = board.generate_moves()
    if not moves:
        return 0, None # Draw or Mate logic needed
        
    # Move ordering could go here
    
    for move in moves:
        board.make_move(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.unmake_move(move)
        
        if score > best_score:
            best_score = score
            best_move = move
            
        if score > alpha:
            alpha = score
            
        if alpha >= beta:
            break
            
    return best_score, best_move

def negamax(board, depth, alpha, beta):
    # Check TT
    # (Simplified: not implementing full Zobrist hashing here, just using board string or similar for demo)
    # board_hash = str(board.squares) + str(board.turn)
    # if board_hash in tt: ...
    
    if depth == 0:
        # Quiescence search could go here
        # For now, just static eval
        # Eval returns white score. If black to move, negate it?
        # My eval returns white advantage.
        # If turn is white, return eval. If black, return -eval.
        score = evaluate(board)
        return score if board.turn == WHITE else -score

    moves = board.generate_moves()
    if not moves:
        # Checkmate or Stalemate
        # If check, return -INF + ply (to prefer shorter mates)
        # If not check, return 0
        return 0 # Simplified
        
    best_score = -INF
    
    for move in moves:
        board.make_move(move)
        score = -negamax(board, depth - 1, -beta, -alpha)
        board.unmake_move(move)
        
        if score > best_score:
            best_score = score
            
        alpha = max(alpha, score)
        if alpha >= beta:
            break
            
    return best_score
