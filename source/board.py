import piece as Piece

# this class keeps track of all the pieces on the board and the board itself and their positions etc. No move logic here
class Board:
    def __init__(self, board: dict = {}):
        self.board = board # setup for the actual data representation of the board
        
        self.pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        self.colors = ['White', 'Black']
        
    def setup(self):
        pieces = self.pieces
        colors = self.colors
            
        for i, col in enumerate('abcdefgh'):
            white_pawn = Piece.Pawn(colors[0], f'{col}2',self)
            black_pawn = Piece.Pawn(colors[1], f'{col}7',self)
            self.board[f'{col}7'] = black_pawn
            self.board[f'{col}2'] = white_pawn
            
            white_piece = getattr(Piece, pieces[i])(colors[0], f'{col}1',self)
            black_piece = getattr(Piece, pieces[i])(colors[1], f'{col}8',self)
            
            self.board[f'{col}1'] = white_piece
            self.board[f'{col}8'] = black_piece
            
    def get_board_state(self):
        return self.board
    
    # clears a square on the board
    def clear_square(self, position: str):
        self.board.pop(position)
    
    def place_piece(self, piece: Piece, position: str):
        self.board[position] = piece
        piece.set_position(position)
    
    # returns the piece (or None) at a given position
    def get_piece_at_position(self, position: str) -> Piece:
        return self.board.get(position)
        
    def copy(self):
        """Creates a new instance of the same class with the same attributes."""
        return Board(board = self.board.copy())
        
    def __str__(self):
        board = ''
        for row in range(8, 0, -1):
            for col in 'abcdefgh':
                piece = self.board[f'{col}{row}']
                if piece:
                    board += str(piece) + ' '
                else:
                    board += ''
            board += '\n'
        return board   
    
    
        