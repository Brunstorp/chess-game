import piece as Piece
import board as Board
import chessgame as ChessGame

class Mover:
    def __init__(self, chessgame: ChessGame):
        self.chessgame = chessgame
        self.chessboard = self.chessgame.chessboard
        
    def clear_moves_list(self, moves: list):
        pass
    
    def simulate_move(self, endpos, piece: Piece, startpos = None) -> bool:
        if startpos == None:
            startpos = piece.get_position()
    
        current_board = self.chessboard
        temp_board = current_board.copy()
        temp_piece = temp_board.get_piece_at_position(startpos)
        temp_board.clear_square(startpos)
        temp_board.place_piece(temp_piece, endpos)
        
        return temp_board
    
    # checks if a given colors chosen square is attacked
    def is_square_attacked(board: Board, position: tuple, color: str) -> bool:
        enemy_color = 'Black' if color == 'White' else enemy_color = 'White'
        
        if position in board.get_legal_moves_player(enemy_color):
            # returns true if the square is attacked
            return True
        return False
             
    def is_checkmate(self) -> bool:
        pass
    
    def is_big_pawn_move(self, start: tuple, end: tuple, piece: Piece) -> bool:
        pass
    
    