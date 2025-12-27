from .board import wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK, WHITE, BLACK, EMPTY

# Material values
VALUES = {
    wP: 100, wN: 320, wB: 330, wR: 500, wQ: 900, wK: 20000,
    bP: -100, bN: -320, bB: -330, bR: -500, bQ: -900, bK: -20000,
    EMPTY: 0
}

# Simplified Piece-Square Tables (PST)
# Just for pawns and knights to encourage development
PAWN_TABLE = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5,-10,  0,  0,-10, -5,  5,
    5, 10, 10,-20,-20, 10, 10,  5,
    0,  0,  0,  0,  0,  0,  0,  0
]

KNIGHT_TABLE = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

def evaluate(board):
    score = 0
    
    # Material and PST
    for i in range(64):
        p = board.squares[i]
        if p == EMPTY: continue
        
        score += VALUES[p]
        
        # Add PST (flip for black)
        r, c = i // 8, i % 8
        if p == wP:
            score += PAWN_TABLE[i]
        elif p == bP:
            # Flip index for black
            mirror_i = (7 - r) * 8 + c
            score -= PAWN_TABLE[mirror_i]
        elif p == wN:
            score += KNIGHT_TABLE[i]
        elif p == bN:
            mirror_i = (7 - r) * 8 + c
            score -= KNIGHT_TABLE[mirror_i]
            
    # Return score from perspective of side to move?
    # Usually minimax expects score for white.
    # If it's black's turn, we might want to return -score if using negamax.
    # But for standard minimax, we return white's advantage.
    
    return score
