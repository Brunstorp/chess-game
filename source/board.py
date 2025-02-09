import pieces as P

class Board:
    def __init__(self):
        self.board = {}
        for row in range(1, 9):
            for col in 'abcdefgh':
                self.board[f'{col}{row}'] = None
        self.winner = None
        self.turn = 'White'
        self.pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        self.colors = ['White', 'Black']
        
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
    
    def update_game_log(self, start_pos: tuple, end_pos: tuple, piece: str):
        self.game_log.append(f'{self.turn} {piece} from {start_pos} to {end_pos}') # will fix a much nicer version here like an official chess game log
    
    def switch_turn(self):  
        self.turn = 'White' if self.turn == 'Black' else 'Black'
    
    def move_piece(self, start: tuple, end: tuple) -> bool:
        piece = self.board.get(start)
        
        if piece:
            if piece.color != self.turn:
                print(f'Not {piece.color}s turn')
                return False
            
            legal_moves = piece.get_legal_moves()
            if end not in legal_moves:
                print('Invalid move')
                return False
            
            self.board[end] = piece
            self.board[start] = None
            piece.position = end
            
            if isinstance(piece,P.Pawn) or isinstance(piece,P.Rook) or isinstance(piece,P.King):
                piece.has_moved = True
            
            self.update_game_log(start, end, piece)
            self.switch_turn()
            
            return True
        
        else:
            print('No piece at that position')
            return False
        
    
        