import chess
from chess import Move
# this class keeps track of all the game logic
class ChessGame:
    def __init__(self, board, testing: bool = False):
        self.chessboard = board
        self.turn = self.chessboard.turn
        self.testing = testing
        
    def get_board(self):
        return self.chessboard
    
    def set_board(self, board):
        self.chessboard = board
        
    def get_turn(self):
        return self.turn
    
    def set_turn(self, turn):
        self.turn = turn
        self.chessboard.turn = turn
        
    def is_valid_move(self, move: Move) -> bool:
        if move in self.chessboard.legal_moves:
            return True
        return False
    
    def check_for_promotion(self, move: Move) -> bool:
        # Check if it's a pawn reaching the last rank
        piece = self.chessboard.piece_at(move.from_square)
        if piece and piece.piece_type == chess.PAWN:
            if chess.square_rank(move.to_square) in [0, 7]:  # Last rank
                return True
        return False
    
    def promote_pawn(self, move: Move, promotion_piece: chess.Piece = chess.QUEEN) -> None:
        return chess.Move(move.from_square, move.to_square, promotion=promotion_piece)

    def move(self, from_square, to_square)  -> bool:
        
        move = chess.Move(from_square, to_square)
        
        if self.check_for_promotion(move):
            move = self.promote_pawn(move)
            
        if self.is_valid_move(move):
            self.chessboard.push(move)
            return True
        
        return False
        
    def is_game_over(self) -> bool:
        return self.chessboard.is_game_over()    
        
    def play_turn(self, from_square, to_square):
        
        moved = self.move(from_square, to_square)

        if self.testing:
            print(self.chessboard.turn)
            self.set_turn(not self.chessboard.turn)
        
        return moved
    
    
        
    