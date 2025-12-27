class Move:
    def __init__(self, start, end, promotion=None, is_castling=False, is_en_passant=False):
        self.start = start
        self.end = end
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant

    def __eq__(self, other):
        return (self.start == other.start and 
                self.end == other.end and 
                self.promotion == other.promotion)

    def __repr__(self):
        # Simple algebraic notation helper (not full SAN)
        files = "abcdefgh"
        ranks = "12345678"
        s = files[self.start % 8] + ranks[7 - (self.start // 8)]
        e = files[self.end % 8] + ranks[7 - (self.end // 8)]
        promo = self.promotion if self.promotion else ""
        return f"{s}{e}{promo}"

    def to_uci(self):
        return self.__repr__()

    @staticmethod
    def from_uci(uci_str):
        # This will need board context to be fully robust (for validation), 
        # but for parsing coordinates it's fine.
        # uci_str example: "e2e4", "a7a8q"
        files = "abcdefgh"
        ranks = "87654321" # 0-index is rank 8
        
        f1, r1 = uci_str[0], uci_str[1]
        f2, r2 = uci_str[2], uci_str[3]
        
        start = (ranks.index(r1) * 8) + files.index(f1)
        end = (ranks.index(r2) * 8) + files.index(f2)
        
        promotion = None
        if len(uci_str) > 4:
            promotion = uci_str[4]
            
        return Move(start, end, promotion)
