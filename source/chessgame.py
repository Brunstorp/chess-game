import board as Board
import piece as Piece

# this class keeps track of all the game logic
class ChessGame:
    
    def __init__(self, chessboard: Board):
        self.chessboard = chessboard
        self.turn = 'White'
        # Game log
        self.game_log = {}
        self.current_move_number = 0 # used for keeping track of the current move number
        
        self.update_all_legal_moves()
        
        #boolean used for testing
        self.testing = False
    
    # switches the turn
    def switch_turn(self):  
        self.turn = 'White' if self.turn == 'Black' else 'Black'
        
    def get_last_move(self):
        if len(self.game_log) == 0:
            print('No moves have been played yet')
            return None
        
        else:      
            return self.game_log[self.current_move_number - 1]
        
    # updates and keeps track of which moves has happened
    def update_game_log(self, start_pos: tuple, end_pos: tuple, piece: str, old_board: Board):
        self.game_log[self.current_move_number] = (start_pos, end_pos, piece, old_board)
        #print(self.game_log)
        
    # updates all legal moves for each piece on the board
    def update_all_legal_moves(self):
        current_board = self.chessboard.get_board_state()
        for piece in current_board.values():
            if piece:
                piece.update_legal_moves()
    
    def move_piece(self, start: tuple, end: tuple, piece: Piece) -> bool:
        
        legal_moves = piece.get_legal_moves()
        
        print("The legal moves are: ", legal_moves)
        
        if piece.color != self.turn:
                print(f'Not {piece.color}s turn')
                return False
        
        if end in legal_moves:
            self.chessboard.place_piece(piece, end)
            self.chessboard.clear_square(start)

            piece.set_position(end)
            
            if isinstance(piece,Piece.Pawn) or isinstance(piece,Piece.Rook) or isinstance(piece,Piece.King):
                    piece.has_moved = True
                    
            return True
        
        if end not in legal_moves:
            print('Invalid move')
            return False
        
    # tries to play the turn the piece from start to end and returns true if successful
    def play_turn(self, start: str, end: str) -> bool:
        
        self.update_all_legal_moves()
        
        old_board = self.chessboard.get_board_state()
        
        piece = self.chessboard.get_piece_at_position(start)
        
        if piece:
            
            piece_moved = self.move_piece(start, end, piece)
            
            if piece_moved:
                
                # here we update the game log
                self.update_game_log(start, end, piece, old_board)
                self.current_move_number += 1
                
                # I use the testing variable to avoid switching turns when testing
                if not self.testing: self.switch_turn() 
                
                return True
        
        else:
            print('No piece at that position')
            return False    
        