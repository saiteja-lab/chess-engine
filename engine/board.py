import copy
from .move import Move

# Piece constants
EMPTY = 0
wP, wN, wB, wR, wQ, wK = 1, 2, 3, 4, 5, 6
bP, bN, bB, bR, bQ, bK = 7, 8, 9, 10, 11, 12

PIECE_STR = {
    EMPTY: '.', 
    wP: 'P', wN: 'N', wB: 'B', wR: 'R', wQ: 'Q', wK: 'K',
    bP: 'p', bN: 'n', bB: 'b', bR: 'r', bQ: 'q', bK: 'k'
}
STR_PIECE = {v: k for k, v in PIECE_STR.items()}

WHITE = 0
BLACK = 1

class Board:
    def __init__(self, fen="rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.squares = [EMPTY] * 64
        self.turn = WHITE
        self.castling = {'K': True, 'Q': True, 'k': True, 'q': True}
        self.en_passant = None # Square index or None
        self.halfmove_clock = 0
        self.fullmove_number = 1
        self.parse_fen(fen)
        
        # History for unmake_move (simplified)
        self.history = []

    def parse_fen(self, fen):
        parts = fen.split()
        rows = parts[0].split('/')
        
        sq = 0
        for row in rows:
            for char in row:
                if char.isdigit():
                    sq += int(char)
                else:
                    self.squares[sq] = STR_PIECE[char]
                    sq += 1
        
        self.turn = WHITE if parts[1] == 'w' else BLACK
        
        self.castling = {
            'K': 'K' in parts[2],
            'Q': 'Q' in parts[2],
            'k': 'k' in parts[2],
            'q': 'q' in parts[2]
        }
        
        if parts[3] != '-':
            files = "abcdefgh"
            ranks = "87654321"
            f, r = parts[3][0], parts[3][1]
            self.en_passant = (ranks.index(r) * 8) + files.index(f)
        else:
            self.en_passant = None
            
        self.halfmove_clock = int(parts[4]) if len(parts) > 4 else 0
        self.fullmove_number = int(parts[5]) if len(parts) > 5 else 1

    def print_board(self):
        for r in range(8):
            line = ""
            for f in range(8):
                sq = r * 8 + f
                line += PIECE_STR[self.squares[sq]] + " "
            print(line)

    def is_square_attacked(self, square, by_color):
        # Simplified attack check
        # Check pawn attacks
        # Check knight attacks
        # Check sliding pieces (bishop, rook, queen)
        # Check king attacks
        # This is critical for legality checking
        
        # Directions for sliding pieces
        orthogonals = [-8, 8, -1, 1]
        diagonals = [-9, -7, 7, 9]
        
        # Enemy pieces
        if by_color == WHITE:
            pawns, knights, bishops, rooks, queens, king = wP, wN, wB, wR, wQ, wK
            pawn_dir = 8 # White pawns attack "up" (lower index) from their perspective? 
            # Wait, rank 0 is top (a8..h8). So index increases as we go down.
            # White pawns are at rank 6 (index 48-55) moving to rank 0.
            # So white pawns move -8. Attacks are -9 and -7.
            # Wait, standard FEN: r is rank 8 (top), R is rank 1 (bottom).
            # My parse_fen iterates rows from top to bottom.
            # So index 0 is a8, index 63 is h1.
            # White is at bottom (indices 48-63).
            # White moves UP (index decreases).
            pawn_attacks = [7, 9] # From target square, looking for white pawns below
        else:
            pawns, knights, bishops, rooks, queens, king = bP, bN, bB, bR, bQ, bK
            pawn_attacks = [-7, -9] # From target square, looking for black pawns above

        r, f = square // 8, square % 8

        # 1. Pawns
        for diff in pawn_attacks:
            src = square + diff
            if 0 <= src < 64:
                sr, sf = src // 8, src % 8
                if abs(sf - f) == 1: # Must be adjacent file
                    if self.squares[src] == pawns:
                        return True

        # 2. Knights
        knight_moves = [-17, -15, -10, -6, 6, 10, 15, 17]
        for diff in knight_moves:
            src = square + diff
            if 0 <= src < 64:
                sr, sf = src // 8, src % 8
                # Check if valid knight move (L-shape)
                if abs(sr - r) in [1, 2] and abs(sf - f) in [1, 2] and abs(sr-r)+abs(sf-f)==3:
                    if self.squares[src] == knights:
                        return True

        # 3. Sliding
        for directions, pieces in [(orthogonals, [rooks, queens]), (diagonals, [bishops, queens])]:
            for d in directions:
                curr = square
                while True:
                    curr += d
                    cr, cf = curr // 8, curr % 8
                    pr, pf = (curr - d) // 8, (curr - d) % 8
                    
                    # Boundary check: must handle wrapping
                    # If we moved -1 (left) and changed row, or +1 (right) and changed row, stop.
                    # Actually, simpler: check if we went off board or wrapped around.
                    if not (0 <= curr < 64): break
                    if abs(cr - pr) > 1 or abs(cf - pf) > 1: break # Wrapped around
                    
                    # Specific check for left/right wrapping
                    if d == 1 and cf == 0: break
                    if d == -1 and cf == 7: break
                    # Diagonals wrapping
                    if d == -9 and (cf == 7 or cr == 7): break # Up-Left? No, -9 is Up-Left (if 8 is width). 
                    # Let's rely on coordinate math.
                    
                    # Re-verify coordinate logic
                    # curr is valid index.
                    # Check if it's on a consistent ray.
                    # Ray logic is hard with 1D array without mailbox 0x88 or similar.
                    # Let's use coordinates.
                    
                    # Reset and do coordinate based ray casting
                    break
        
        # Re-implement sliding with coordinates for safety
        for directions, pieces in [(orthogonals, [rooks, queens]), (diagonals, [bishops, queens])]:
            for dr, df in [(-1, 0), (1, 0), (0, -1), (0, 1)] if pieces == [rooks, queens] else [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
                cr, cf = r, f
                while True:
                    cr += dr
                    cf += df
                    if not (0 <= cr < 8 and 0 <= cf < 8): break
                    idx = cr * 8 + cf
                    p = self.squares[idx]
                    if p != EMPTY:
                        if p in pieces: return True
                        break # Blocked by something else
        
        # 4. King
        for dr in [-1, 0, 1]:
            for df in [-1, 0, 1]:
                if dr == 0 and df == 0: continue
                cr, cf = r + dr, f + df
                if 0 <= cr < 8 and 0 <= cf < 8:
                    if self.squares[cr * 8 + cf] == king:
                        return True
                        
        return False

    def generate_moves(self):
        moves = []
        # Simplified generator: iterate all squares, find pieces of current turn, generate pseudo-legal
        # Then filter for legality (king not in check)
        
        my_color = self.turn
        opp_color = BLACK if self.turn == WHITE else WHITE
        
        for sq in range(64):
            p = self.squares[sq]
            if p == EMPTY: continue
            
            # Check color
            is_white = p in [wP, wN, wB, wR, wQ, wK]
            if (is_white and self.turn == BLACK) or (not is_white and self.turn == WHITE):
                continue
                
            r, f = sq // 8, sq % 8
            
            # Pawn moves
            if p == wP or p == bP:
                direction = -8 if is_white else 8
                start_rank = 6 if is_white else 1
                
                # Forward 1
                tgt = sq + direction
                if 0 <= tgt < 64 and self.squares[tgt] == EMPTY:
                    # Promotion?
                    tr = tgt // 8
                    if (is_white and tr == 0) or (not is_white and tr == 7):
                        promos = ['q', 'r', 'b', 'n']
                        for promo in promos:
                            moves.append(Move(sq, tgt, promotion=promo))
                    else:
                        moves.append(Move(sq, tgt))
                        
                    # Forward 2
                    if r == start_rank:
                        tgt2 = sq + direction * 2
                        if self.squares[tgt2] == EMPTY:
                            moves.append(Move(sq, tgt2))
                            
                # Captures
                for df in [-1, 1]:
                    if 0 <= f + df < 8:
                        tgt = sq + direction + df
                        if 0 <= tgt < 64:
                            target_p = self.squares[tgt]
                            if target_p != EMPTY:
                                # Check if enemy
                                is_enemy = (target_p >= bP) if is_white else (target_p <= wK)
                                if is_enemy:
                                    # Promotion check
                                    tr = tgt // 8
                                    if (is_white and tr == 0) or (not is_white and tr == 7):
                                        promos = ['q', 'r', 'b', 'n']
                                        for promo in promos:
                                            moves.append(Move(sq, tgt, promotion=promo))
                                    else:
                                        moves.append(Move(sq, tgt))
                            elif tgt == self.en_passant:
                                # En passant capture
                                moves.append(Move(sq, tgt, is_en_passant=True))

            # Knight moves
            elif p == wN or p == bN:
                dr_df = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
                for dr, df in dr_df:
                    nr, nf = r + dr, f + df
                    if 0 <= nr < 8 and 0 <= nf < 8:
                        tgt = nr * 8 + nf
                        tp = self.squares[tgt]
                        if tp == EMPTY or ((tp >= bP) if is_white else (tp <= wK)):
                            moves.append(Move(sq, tgt))

            # King moves
            elif p == wK or p == bK:
                for dr in [-1, 0, 1]:
                    for df in [-1, 0, 1]:
                        if dr == 0 and df == 0: continue
                        nr, nf = r + dr, f + df
                        if 0 <= nr < 8 and 0 <= nf < 8:
                            tgt = nr * 8 + nf
                            tp = self.squares[tgt]
                            if tp == EMPTY or ((tp >= bP) if is_white else (tp <= wK)):
                                moves.append(Move(sq, tgt))
                
                # Castling
                # This requires checking castling rights, empty squares, and not attacked squares
                # Simplified: just check rights and empty squares for now, legality check later?
                # No, castling rules are strict: cannot castle out of, through, or into check.
                # I'll implement basic rights check here.
                pass # TODO: Implement castling

            # Sliding moves (B, R, Q)
            else:
                dirs = []
                if p in [wB, bB, wQ, bQ]: dirs.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)])
                if p in [wR, bR, wQ, bQ]: dirs.extend([(-1, 0), (1, 0), (0, -1), (0, 1)])
                
                for dr, df in dirs:
                    nr, nf = r, f
                    while True:
                        nr += dr
                        nf += df
                        if not (0 <= nr < 8 and 0 <= nf < 8): break
                        tgt = nr * 8 + nf
                        tp = self.squares[tgt]
                        if tp == EMPTY:
                            moves.append(Move(sq, tgt))
                        else:
                            if (tp >= bP) if is_white else (tp <= wK):
                                moves.append(Move(sq, tgt))
                            break

        # Filter legal moves
        legal_moves = []
        for m in moves:
            self.make_move(m)
            # Find king
            king_val = wK if my_color == WHITE else bK
            king_pos = -1
            for i in range(64):
                if self.squares[i] == king_val:
                    king_pos = i
                    break
            
            if king_pos != -1 and not self.is_square_attacked(king_pos, opp_color):
                legal_moves.append(m)
            self.unmake_move(m)
            
        return legal_moves

    def make_move(self, move):
        # Save state
        self.history.append({
            'squares': self.squares[:],
            'turn': self.turn,
            'castling': self.castling.copy(),
            'en_passant': self.en_passant,
            'halfmove': self.halfmove_clock,
            'fullmove': self.fullmove_number
        })
        
        p = self.squares[move.start]
        self.squares[move.start] = EMPTY
        self.squares[move.end] = p
        
        # Promotion
        if move.promotion:
            # Map promo char to piece constant
            # 'q' -> wQ or bQ depending on turn
            offset = 0 if self.turn == WHITE else 6
            promo_map = {'q': wQ, 'r': wR, 'b': wB, 'n': wN}
            self.squares[move.end] = promo_map[move.promotion.lower()] + offset

        # En passant capture
        if move.is_en_passant:
            # Remove the captured pawn
            # If white moved to e6 (from e5) capturing d6 (ep square), the pawn was at d5.
            # Target is index of e6. Captured pawn is at target + 8 (if white) or -8 (if black)?
            # White moves up (-8). En passant target is behind the pawn.
            # If white moves P to ep square, the captured pawn is "below" the ep square (index + 8).
            cap_sq = move.end + 8 if self.turn == WHITE else move.end - 8
            self.squares[cap_sq] = EMPTY

        # Update En Passant rights
        self.en_passant = None
        if (p == wP or p == bP) and abs(move.start - move.end) == 16:
            self.en_passant = (move.start + move.end) // 2

        # Update turn
        self.turn = BLACK if self.turn == WHITE else WHITE
        
        # TODO: Update castling rights, halfmove clock, etc.

    def unmake_move(self, move):
        state = self.history.pop()
        self.squares = state['squares']
        self.turn = state['turn']
        self.castling = state['castling']
        self.en_passant = state['en_passant']
        self.halfmove_clock = state['halfmove']
        self.fullmove_number = state['fullmove']
