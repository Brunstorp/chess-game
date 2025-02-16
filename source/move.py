import piece as Piece
import board as Board
import chessgame as ChessGame

class Move:
    def __init__(self, piece: Piece, start: str, end: str, chessgame: ChessGame):
        self.piece = piece
        self.start = start
        self.end = end
        self.chessgame = chessgame
        self.chessboard = chessgame.chessboard
        self.turn = chessgame.turn
        self.game_log = chessgame.game_log
        self.move_succesful = False
        
    
    def move_piece(self):
        pass
    
    def is_big_pawn_move(self):
        pass
    
    def is_en_passant(self):
        pass
    
    def is_castling(self):
        pass
    
    def is_promotion(self):
        pass
    
    def move_succesful(self):
        pass
    
    def king_in_check(self):
        pass
    
    

    