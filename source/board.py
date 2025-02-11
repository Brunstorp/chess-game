import pieces as P

class Board:
    def __init__(self):
        self.board = {} # setup for the actual data representation of the board
        self.pieces_dict = {}
        self.winner = None
        
        self.turn = 'White'
        self.pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        self.colors = ['White', 'Black']
        
        # stores all legal moves for each player currently in the game
        self.legal_moves_players = {'White': {}, 'Black': {}} # stores all legal moves for each player
        
        #boolean used for testing
        self.testing = False
        
        # Game log
        self.game_log = []
        
        # setup pieces dict
        if len(self.board) > 0:
            self.setup_pieces_dict()
        
    def setup(self):
        pieces = self.pieces
        colors = self.colors
        
        for i, col in enumerate('abcdefgh'):
            white_pawn = P.Pawn(colors[0], f'{col}2',self)
            black_pawn = P.Pawn(colors[1], f'{col}7',self)
            self.board[f'{col}2'] = white_pawn
            self.board[f'{col}7'] = black_pawn
            
            white_piece = getattr(P, pieces[i])(colors[0], f'{col}1',self)
            black_piece = getattr(P, pieces[i])(colors[1], f'{col}8',self)
            
            self.board[f'{col}1'] = white_piece
            self.board[f'{col}8'] = black_piece
            
    # this also needs to be called outside of the init function to make sure the pieces_dict is updated
    def setup_pieces_dict(self):
        for piece in self.board.values():
            if piece:
                self.pieces_dict[str(piece)] = piece
        
                                 
    def access_piece(self, color_type: str) -> P:
        return self.pieces_dict.get(color_type)
            
    def is_king_in_check(self, color: str) -> bool:
        search_string = f'{color}King'
        print("search str is:", search_string)
        king = self.access_piece(search_string)
        
        if king:
            king_position = king.get_position()
            if not self.is_square_safe(king_position, color):
                print(f'{color} King is in check at {king_position}')
                return True
        return False 
    
    # clears a square on the board
    def clear_square(self, position: str):
        self.board.pop(position)
    
    # updates and keeps track of which moves has happened
    def update_game_log(self, start_pos: tuple, end_pos: tuple, piece: str):
        self.game_log.append(f'{self.turn} moved {piece} from {start_pos} to {end_pos}') # will fix a much nicer version here like an official chess game log
    
    # switches the turn
    def switch_turn(self):  
        self.turn = 'White' if self.turn == 'Black' else 'Black'
        
    # this actually updates the legal moves for all pieces
    def update_all_legal_moves(self): 
        for piece in self.board.values():
            if piece:
                piece.update_legal_moves()
                
    # returns all legal moves for a given color as a long list so we can check if a square is safe for a given player
    def get_all_legal_moves(self, color: str) -> list: 
        legal_moves_player = []
        for piece in self.board.values():
            if piece.color == color:
                legal_moves_player.extend(piece.get_legal_moves())
        #print("Legal moves for", color, legal_moves_player)
        return legal_moves_player
    
    # returns a list with all calculated legal moves for a given color, so we can check one move ahead and stuff (like what would happen if we moved there)
    def calculate_all_legal_moves(self, color: str) -> dict: 
        legal_moves_player = []
        for piece in self.board.values():
            if piece.color == color:
                legal_moves_player.extend(piece.calculate_legal_moves())
        return legal_moves_player
        
    # sets all legal moves for each player
    def set_all_legal_moves(self): 
        self.legal_moves_players['White'] = self.get_all_legal_moves('White')
        self.legal_moves_players['Black'] = self.get_all_legal_moves('Black')
    
    def is_square_safe(self, position: str, color: str, legal_moves = None) -> bool: #checks if a given square is safe for a given player to move to, default checks current legal moves
        other_player = 'Black' if color == 'White' else 'White'
        
        if not legal_moves:
            legal_moves = self.legal_moves_players[other_player]
        
        #print("Checking if square is safe for", color, position)
        if position in legal_moves:
            return False
        return True
    
    def place_piece(self, piece: P, position: str):
        self.board[position] = piece
    
    def remove_piece(self, position: str):
        self.board.pop(position)
        self.pieces_set.remove(self.board[position])
        
    def get_at_position(self, position: str) -> P: # returns the piece (or None) at a given position
        return self.board.get(position)
     
    def move_piece(self, start: tuple, end: tuple, piece: P) -> bool:
        if piece.color != self.turn:
                print(f'Not {piece.color}s turn')
                return False
            
        legal_moves = piece.get_legal_moves()
        #special_moves = piece.get_special_moves()
        
        if end in legal_moves:
            self.board[end] = piece
            self.board.pop(start)
            piece.set_position(end)
            return True
        
        if end not in legal_moves:
            print('Invalid move')
            return False
        
    def play_turn(self, start: tuple, end: tuple) -> bool: # tries to play the turn the piece from start to end and returns true if successful
        # Initialize board with legal moves
        self.update_all_legal_moves()
        
        # check who's turn it is
        is_king_in_check = self.is_king_in_check(self.turn)
        
        piece = self.board.get(start)
        
        if piece:
            piece_moved = self.move_piece(start, end, piece)
            
            if piece_moved:
                if isinstance(piece,P.Pawn) or isinstance(piece,P.Rook) or isinstance(piece,P.King):
                    piece.has_moved = True
                    
                self.update_all_legal_moves()
                self.set_all_legal_moves()
                self.update_game_log(start, end, piece)
                if not self.testing: self.switch_turn() # I use the testing variable to avoid switching turns when testing
                
                return True
        
        else:
            print('No piece at that position')
            return False
        
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
        