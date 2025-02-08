import pieces as P

class Board:
    def __init__(self):
        self.board = {}
        for row in range(1, 9):
            for col in 'abcdefgh':
                self.board[f'{col}{row}'] = None
        self.winner = None
        self.turn = 'W'
        self.pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        self.colors = ['White', 'Black']
        
    def setup(self):
        pieces = self.pieces
        colors = self.colors
        for i, col in enumerate('abcdefgh'):
            self.board[f'{col}2'] = P.Pawn(colors[0], f'{col}2')
            self.board[f'{col}7'] = P.Pawn(colors[1], f'{col}7')
            self.board[f'{col}1'] = getattr(P, pieces[i])(colors[0], f'{col}1')
            self.board[f'{col}8'] = getattr(P, pieces[i])(colors[1], f'{col}8')
        
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
    
    # this takes in two tuples as (x,y) coordinates and moves the piece from the start to the end regardless of what piece is there and regardless of the legality of the move
    def move_piece(self, start: tuple, end: tuple) -> bool:
        piece = self.board[start]
        legal_moves = piece.get_legal_moves(self.board)
        if piece:
            self.board[end] = piece
            self.board[start] = None
            piece.position = end
            return True
        else:
            print('No piece at that position')
            return False
        
    
        