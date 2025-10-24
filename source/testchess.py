import chess
import gui as GUI
import chessgame as ChessGame

def test_promotion(board):
    board.clear()
    square = chess.parse_square("e2")  # Square e4
    piece = chess.Piece(chess.PAWN, chess.WHITE)  # White Queen

    # Place the piece on the board
    board.set_piece_at(square, piece)
    chessgame = ChessGame.ChessGame(board, testing=True)
    gui = GUI.GUI(chessgame, 900)
    gui.run()
    
def test_normal(board):
    chessgame = ChessGame.ChessGame(board, testing=False)
    
    gui = GUI.GUI(chessgame, 900)
    
    gui.run()
    
    
if __name__ == '__main__':
    board=chess.Board.from_chess960_pos(519)
    test_normal(board)
    #test_promotion(board)