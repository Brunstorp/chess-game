import pieces as P

class Board:
    def __init__(self):
        self.board = {}
        for row in range(1, 9):
            for col in 'abcdefgh':
                self.board[f'{col}{row}'] = None
        self.winner = None
        self.turn = 'W'
        
    def setup(self):
        pieces = ['Rook', 'Knight', 'Bishop', 'Queen', 'King', 'Bishop', 'Knight', 'Rook']
        for i, col in enumerate('abcdefgh'):
            self.board[f'{col}2'] = P.Pawn('W', f'{col}2')
            self.board[f'{col}7'] = P.Pawn('B', f'{col}7')
            self.board[f'{col}1'] = getattr(P, pieces[i])('W', f'{col}1')
            self.board[f'{col}8'] = getattr(P, pieces[i])('B', f'{col}8')
        
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
        
    
        