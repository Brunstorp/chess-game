import board as Board
import gui as GUI
import piece as Piece
import chessgame as ChessGame

def test_castling(chessboard: Board):
    king = Piece.King('White', 'e1', chessboard)
    chessboard.place_piece(king, king.get_position())  
    chessboard.place_piece(Piece.Rook('Black', 'a8', chessboard), 'a8') 

if __name__ == '__main__':
    testboard = Board.Board()
    
    chessgame = ChessGame.ChessGame(testboard)
    chessgame.testing = True
    test_castling(testboard)
    
    gui = GUI.GUI(chessgame, 900, testboard)
    gui.run()