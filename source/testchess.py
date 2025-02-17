import chess
import gui as GUI
import chessgame as ChessGame
    
if __name__ == '__main__':
    board = chess.Board()
    board.clear()
    square = chess.parse_square("e2")  # Square e4
    piece = chess.Piece(chess.PAWN, chess.WHITE)  # White Queen

    # Place the piece on the board
    board.set_piece_at(square, piece)
    chessgame = ChessGame.ChessGame(board, testing=True)
    gui = GUI.GUI(chessgame, 900)
    gui.run()
    