import pieces as P

class Board:
    def __init__(self):
        self.board = {}
        
        self.winner = None
        self.turn = 'White'
        self.pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        self.colors = ['White', 'Black']
        self.legal_moves_players = {'White': {}, 'Black': {}} # stores all legal moves for each player
        self.testing = False
        # Game log
        self.game_log = []
        
    def setup(self):
        pieces = self.pieces
        colors = self.colors
        
        for i, col in enumerate('abcdefgh'):
            self.board[f'{col}2'] = P.Pawn(colors[0], f'{col}2',self.board)
            self.board[f'{col}7'] = P.Pawn(colors[1], f'{col}7',self.board)
            self.board[f'{col}1'] = getattr(P, pieces[i])(colors[0], f'{col}1',self.board)
            self.board[f'{col}8'] = getattr(P, pieces[i])(colors[1], f'{col}8',self.board)
        
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
    
    def clear_square(self, position: str):
        self.board.pop(position)
    
    def update_game_log(self, start_pos: tuple, end_pos: tuple, piece: str):
        self.game_log.append(f'{self.turn} {piece} from {start_pos} to {end_pos}') # will fix a much nicer version here like an official chess game log
    
    def switch_turn(self):  
        self.turn = 'White' if self.turn == 'Black' else 'Black'
        
    def calculate_all_legal_moves(self):
        for piece in self.board.values():
            if piece:
                piece.update_legal_moves()
                
    def get_all_legal_moves(self, color: str) -> list: # returns all legal moves for a given color as a long list so we can check if a square is safe
        legal_moves_player = []
        for piece in self.board.values():
            if piece.color == color:
                legal_moves_player.extend(piece.get_legal_moves())
        return legal_moves_player
    
    def set_all_legal_moves(self):
        self.legal_moves_players['White'] = self.get_all_legal_moves('White')
        self.legal_moves_players['Black'] = self.get_all_legal_moves('Black')
    
    def check_square_safe(self, position: tuple) -> bool: #checks if a given square is safe
        other_player = 'Black' if self.turn == 'White' else 'White'
        if position in self.legal_moves_players[other_player]:
            return False
        return True
    
    def place_piece(self, piece: P, position: tuple):
        self.board[position] = piece
                
    def move_piece(self, start: tuple, end: tuple, piece: P) -> bool:
        if piece.color != self.turn:
                print(f'Not {piece.color}s turn')
                return False
        
        legal_moves = piece.get_legal_moves()
        
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
        self.calculate_all_legal_moves()
        piece = self.board.get(start)
        
        if piece:
            piece_moved = self.move_piece(start, end, piece)
            if piece_moved:
            
                if isinstance(piece,P.Pawn) or isinstance(piece,P.Rook) or isinstance(piece,P.King):
                    piece.has_moved = True
                    
                self.calculate_all_legal_moves()
                self.set_all_legal_moves()
                self.update_game_log(start, end, piece)
                if not self.testing: self.switch_turn() # I use the testing variable to avoid switching turns when testing
                
                return True
        
        else:
            print('No piece at that position')
            return False
        