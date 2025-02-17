import gui as GUI
import chessgame as ChessGame
import chess

if __name__ == '__main__':
    board = chess.Board()
    chessgame = ChessGame.ChessGame(board, testing=False)
    gui = GUI.GUI(chessgame, 900)
    gui.run()
    #test_promotion(board)