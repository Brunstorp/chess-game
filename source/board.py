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
    
    # Column to letter, row to 1-based index
    def coordinate_to_position(self, coordinate: tuple) -> str:
        col, row = coordinate
        position = f'{chr(col + 97)}{row + 1}'  
        return position

    # Convert chess position (e.g., 'a1') to 0-7 coordinates
    def position_to_coordinate(self, position: str) -> tuple:
        col, row = position
        coordinate = (ord(col) - 97, int(row) - 1)  # Letter to column index, 1-based to 0-based
        return coordinate
    
    # this checks if the square is inside the grid
    def is_valid_position(self, position: str): 
        if len(position) != 2:
            return False
        
        col, row = position
        if col not in 'abcdefgh' or row not in '12345678':
            return False
        return True
    
    # this checks if a move is valid, i.e doesnt go outside and is not the same color as the piece
    def is_valid_move(self, move_position: str, piece: Piece) -> bool:
        # since we cannot click outside the square this works
        is_valid_position = self.is_valid_position(move_position)
        
        if self.get_piece_at_position(move_position) == None: 
            return is_valid_position
        else:
            # we check if it is not the same color as it's own and if it is a valid position
            return is_valid_position and not self.get_piece_at_position(move_position).color == piece.color 
        
    def get_legal_moves_player(self, color: str) -> list:
        legal_moves = []
        for position, piece in self.board.items():
            if piece and piece.color == color:
                legal_moves.extend(piece.get_legal_moves())
        return legal_moves
    
    
        