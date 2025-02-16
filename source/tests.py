import board as Board
import gui as GUI
import piece as Piece
import chessgame as ChessGame

def test_castling(chessboard: Board):
    king = Piece.King('White', 'e1', chessboard)
    chessboard.place_piece(king, king.get_position())  
    chessboard.place_piece(Piece.Rook('Black', 'a8', chessboard), 'a8') 
    
def test_rook(chessboard: Board):
    rook = Piece.Rook('White', 'a1', chessboard)
    chessboard.place_piece(rook, rook.get_position())

def test_queen(chessboard: Board):
    queen = Piece.Queen('White', 'd1', chessboard)
    chessboard.place_piece(queen, queen.get_position())
    
def test_knight(chessboard: Board):
    knight = Piece.Knight('White', 'b1', chessboard)
    chessboard.place_piece(knight, knight.get_position())
    
def test_bishop(chessboard: Board):
    bishop = Piece.Bishop('White', 'c1', chessboard)
    chessboard.place_piece(bishop, bishop.get_position())
    
def test_pawn(chessboard: Board):
    pawn = Piece.Pawn('White', 'a3', chessboard)
    chessboard.place_piece(pawn, pawn.get_position())

if __name__ == '__main__':
    testboard = Board.Board()
    
    chessgame = ChessGame.ChessGame(testboard)
    chessgame.testing = True
    #test_castling(testboard)
    #test_rook(testboard)
    #test_queen(testboard)
    #test_knight(testboard)
    #test_bishop(testboard)
    test_pawn(testboard)
    
    gui = GUI.GUI(chessgame, 900, testboard)
    gui.run()