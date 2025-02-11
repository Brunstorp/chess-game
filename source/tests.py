import board as B
import gui as G
import pieces as P

def test_castling(chessboard: B):
    king = P.King('White', 'e1', chessboard)
    chessboard.place_piece(king, king.get_position())  
    chessboard.place_piece(P.Rook('Black', 'a8', chessboard), 'a8') 

if __name__ == '__main__':
    testboard = B.Board()
    testboard.testing = False
    test_castling(testboard)
    testboard.setup_pieces_dict()
    gui = G.GUI(900, testboard)
    gui.run()