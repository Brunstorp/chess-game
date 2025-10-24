import pygame
import chessgame as ChessGame  # Assuming you have a separate `board.py` with a Board class.
import chess

# Initialize pygame
pygame.init()

class GUI:
    def __init__(self, chessgame: ChessGame, size=600, white_view=True):
        self.chessgame = chessgame
        self.white_view = white_view

        # Window settings
        self.WIDTH = self.HEIGHT = size
        self.SQUARE_SIZE = self.WIDTH // 8
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Game")

        # Colors
        self.colors = [(255, 255, 255), (139, 69, 19)]  # white, brown

        # Selection
        self.selected_piece = None
        self.selected_position = None

        self.running = False
        self.board_history = []  # store previous boards

        # Initial draw
        self.draw_squares()

    # ---------- view toggle ----------
    def toggle_flip_view(self):
        self.white_view = not self.white_view
        self.draw_squares()

    # ---------- mapping helpers ----------
    # background coords: never flip
    def get_board_coordinates(self, position: str) -> tuple:
        file_index = ord(position[0]) - 97
        rank_index = int(position[1]) - 1
        x = file_index * self.SQUARE_SIZE
        y = (7 - rank_index) * self.SQUARE_SIZE
        return (x, y)

    # piece/dot coords: flip when black view
    def get_window_coordinates(self, position: str) -> tuple:
        file_index = ord(position[0]) - 97
        rank_index = int(position[1]) - 1
        if not self.white_view:
            file_index = 7 - file_index
            rank_index = 7 - rank_index
        x = file_index * self.SQUARE_SIZE
        y = (7 - rank_index) * self.SQUARE_SIZE
        return (x, y)

    # inverse: pixels -> algebraic under current view
    def get_position_from_coordinates(self, x: int, y: int) -> str:
        file_index = x // self.SQUARE_SIZE
        rank_index = 7 - (y // self.SQUARE_SIZE)
        if not self.white_view:
            file_index = 7 - file_index
            rank_index = 7 - rank_index
        return f"{chr(file_index + 97)}{rank_index + 1}"

    # ---------- piece utils ----------
    def piece_to_string(self, piece):
        if piece is None:
            return None
        color = "white" if piece.color == chess.WHITE else "black"
        piece_name = {
            chess.PAWN: "pawn",
            chess.KNIGHT: "knight",
            chess.BISHOP: "bishop",
            chess.ROOK: "rook",
            chess.QUEEN: "queen",
            chess.KING: "king",
        }[piece.piece_type]
        return f"{color}_{piece_name}"

    # ---------- drawing ----------
    def get_window_color(self, sq: chess.Square) -> tuple:
        f = chess.square_file(sq)
        r = chess.square_rank(sq)
        # Make (f+r)==0 map to dark, not light
        return self.colors[1 - ((f + r) % 2)]

    def draw_square(self, square: chess.Square):
        square_str = chess.square_name(square)
        x, y = self.get_board_coordinates(square_str)  # never flipped
        color = self.get_window_color(square)
        pygame.draw.rect(self.screen, color, pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_piece(self, piece: chess.Piece, square: chess.Square):
        square_str = chess.square_name(square)
        x, y = self.get_window_coordinates(square_str)  # view-aware
        piece_name = self.piece_to_string(piece)
        if piece_name:
            image = pygame.image.load(f"../pictures/{piece_name}.png")
            image = pygame.transform.scale(image, (self.SQUARE_SIZE, self.SQUARE_SIZE))
            self.screen.blit(image, (x, y))

    def draw_move_dots(self):
        if self.selected_piece and self.selected_position:
            selected_square = chess.parse_square(self.selected_position)
            legal_moves = [m for m in self.chessgame.get_board().legal_moves if m.from_square == selected_square]
            dot_color = (0, 255, 100)
            radius = self.SQUARE_SIZE // 8
            for move in legal_moves:
                dest_square_str = chess.square_name(move.to_square)
                dest_x, dest_y = self.get_window_coordinates(dest_square_str)  # view-aware
                center_x = dest_x + self.SQUARE_SIZE // 2
                center_y = dest_y + self.SQUARE_SIZE // 2
                pygame.draw.circle(self.screen, dot_color, (center_x, center_y), radius)
            pygame.display.flip()

    def draw_squares(self):
        # background: fixed orientation
        for sq in chess.SQUARES:
            self.draw_square(sq)
        # pieces: orientation depends on view
        for sq in chess.SQUARES:
            piece = self.chessgame.get_board().piece_at(sq)
            if piece:
                self.draw_piece(piece, sq)
        pygame.display.flip()

    # ---------- input handling ----------
    def play_turn(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            clicked_position = self.get_position_from_coordinates(mouse_x, mouse_y)  # view-aware
            clicked_square = chess.parse_square(clicked_position)

            if self.selected_piece is None:
                piece = self.chessgame.get_board().piece_at(clicked_square)
                if piece:
                    self.selected_piece = piece
                    self.selected_position = clicked_position
                    self.draw_move_dots()
            else:
                from_square = chess.parse_square(self.selected_position)
                to_square = clicked_square
                destination_piece = self.chessgame.get_board().piece_at(to_square)

                if destination_piece and destination_piece.color == self.selected_piece.color:
                    self.selected_piece = destination_piece
                    self.selected_position = clicked_position
                    self.draw_squares()
                    self.draw_move_dots()
                else:
                    old_board = self.chessgame.get_board().copy()
                    success = self.chessgame.play_turn(from_square, to_square)
                    if success:
                        self.board_history.append(old_board)
                        self.draw_squares()
                    # Deselect regardless
                    self.selected_piece = None
                    self.selected_position = None

    def handle_keydown(self, event):
        if event.key == pygame.K_f:
            self.toggle_flip_view()
            print("Flipped view!")
        if self.board_history and event.key == pygame.K_LEFT:
            old_board = self.board_history.pop()
            self.chessgame.set_board(old_board)
            self.draw_squares()
            if old_board:
                print("Went back in history!")

    # ---------- main loop ----------
    def run(self):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self.play_turn(event)
        pygame.quit()