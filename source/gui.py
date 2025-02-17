import pygame
import chessgame as ChessGame  # Assuming you have a separate `board.py` with a Board class.
import chess


# Initialize pygame
pygame.init()

class GUI:
    def __init__(self, chessgame: ChessGame, size=600, white_view = True):
        
        self.chessgame = chessgame
        
        # Set default view (True means white's view, False means black's view)
        self.white_view = white_view
        
        # Window settings
        self.WIDTH = self.HEIGHT = size
        self.SQUARE_SIZE = self.WIDTH // 8
        
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        pygame.display.set_caption("Chess Game")
        
        # Draw the board and pieces intially
        self.colors = [(255, 255, 255), (139, 69, 19)]  # White and Brown color codes
        self.draw_squares()
        
        # Selected piece
        self.selected_piece = None
        self.selected_position = None
        
        # Run the game
        self.running = False
        
        self.board_history = []  # to store move notations
        
    def toggle_flip_view(self):
        """Toggle the board view between white and black."""
        self.white_view = not self.white_view
        
    def piece_to_string(self,piece):
        """Converts a chess.Piece object to a string like 'black_queen' or 'white_knight'."""
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
          
    # this is to go from say 'a1' to whatever that becomes in the window      
    def get_window_coordinates(self, position: str) -> tuple:
        file_index = ord(position[0]) - 97
        rank_index = int(position[1]) - 1
        if self.white_view:
            x = file_index * self.SQUARE_SIZE
            y = (7 - rank_index) * self.SQUARE_SIZE
        else:
            # Black view: invert the file and rank
            x = (7 - file_index) * self.SQUARE_SIZE
            y = rank_index * self.SQUARE_SIZE
        return (x, y)

    
    # and this is obviously just the inverse of the above function
    def get_position_from_coordinates(self, x: int, y: int) -> str:
        if self.white_view:
            file_index = x // self.SQUARE_SIZE
            rank_index = 7 - (y // self.SQUARE_SIZE)
        else:
            file_index = 7 - (x // self.SQUARE_SIZE)
            rank_index = y // self.SQUARE_SIZE
        return f"{chr(file_index + 97)}{rank_index + 1}"

           
    # this is to draw a generic piece         
    def draw_piece(self, piece: chess.Piece, square: chess.Square):
        
        square_str = chess.square_name(square)
        
        x, y = self.get_window_coordinates(square_str)
        
        piece_name = self.piece_to_string(piece)
        
        if piece_name:
            image = pygame.image.load(f"../pictures/{piece_name}.png")
            
            image = pygame.transform.scale(
                    image,
                    (self.SQUARE_SIZE, self.SQUARE_SIZE)  # Scale to match board squares
                )
            
            self.screen.blit(image, (x, y))
            
    def draw_square(self,square: chess.Square): 
        """Draw a square background on the chessboard, given a square as string."""
        square_str = chess.square_name(square)
            
        window_x, window_y = self.get_window_coordinates(square_str)
        # Determine square color from its file and rank (independent of view)
        color = self.get_window_color(square)
        
        pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(window_x, window_y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

    def get_window_color(self, sq: chess.Square) -> tuple:
        """Return the color of a square."""
        f = chess.square_file(sq)
        r = chess.square_rank(sq)
        expression = (f + r) % 2
        
        if not self.white_view:
            expression = 1 - expression

        color = self.colors[expression]
        return color
        
    # this draws the board, meaning the background
    def draw_squares(self):
        """Draw the chessboard squares using algebraic positions."""
        chess_squares = chess.SQUARES
        
        if not self.white_view:
            chess_squares = reversed(chess_squares)
            
        for sq in chess_squares: 
            self.draw_square(sq)
            
            piece = self.chessgame.get_board().piece_at(sq)
            
            if piece:
                self.draw_piece(piece, sq)
        
        # Update the display
        pygame.display.flip()
        
    def draw_move_dots(self):
        if self.selected_piece and self.selected_position:
            selected_square = chess.parse_square(self.selected_position)
            legal_moves = [move for move in self.chessgame.get_board().legal_moves if move.from_square == selected_square]
            
            # Choose a dot color and radius
            dot_color = (0, 255, 100)  # Green, for example
            radius = self.SQUARE_SIZE // 8
            
            for move in legal_moves:
                # Get the destination square as an algebraic string
                dest_square_str = chess.square_name(move.to_square)
                # Convert it to window coordinates
                dest_x, dest_y = self.get_window_coordinates(dest_square_str)
                
                # Calculate the center of the square
                center_x = dest_x + self.SQUARE_SIZE // 2
                center_y = dest_y + self.SQUARE_SIZE // 2
                
                # Draw the circle (dot)
                pygame.draw.circle(self.screen, dot_color, (center_x, center_y), radius)
                pygame.display.flip()
                
    # later I might have to implemet a way for the computer to access aswell
    def play_turn(self, event):
        """Handle mouse clicks to select a piece or attempt a move."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            
            mouse_x, mouse_y = pygame.mouse.get_pos()
            print(f"Mouse clicked at ({mouse_x}, {mouse_y})")
            
            clicked_position = self.get_position_from_coordinates(mouse_x, mouse_y)
            
            print(f"Clicked position: {clicked_position}")
            clicked_square = chess.parse_square(clicked_position)
            print(f"Clicked square: {clicked_square}")
            
            # If no piece is selected, try to select one.
            if self.selected_piece is None:
                piece = self.chessgame.get_board().piece_at(clicked_square)
                if piece:
                    self.selected_piece = piece
                    self.selected_position = clicked_position
                    print(f"Selected: {piece} at {clicked_position}")
                    
                    # when a piece is selected, draw the dots
                    self.draw_move_dots()
                    
            else:
                # A piece is already selected; determine what to do on second click.
                from_square = chess.parse_square(self.selected_position)
                to_square = clicked_square
                
                destination_piece = self.chessgame.get_board().piece_at(to_square)
                # If the destination contains a piece of the same color, reselect it.
                if destination_piece and destination_piece.color == self.selected_piece.color:
                    self.selected_piece = destination_piece
                    self.selected_position = clicked_position
                    print(f"Reselected: {destination_piece} at {clicked_position}")
                    
                    # redraw the dots, first clearing the board
                    self.draw_squares()
                    self.draw_move_dots()
                    
                else:
                    print(f"Attempting to move {self.selected_piece} from {self.selected_position} to {clicked_position}")
                    old_board = self.chessgame.get_board().copy()
                    
                    # Attempt to move.
                    success = self.chessgame.play_turn(from_square, to_square)
                    
                    if success:
                        # Record the move using standard algebraic notation (or your own format).
                         
                        self.board_history.append(old_board)
                        print("Move successful!")
                        
                        # Update the display
                        self.draw_squares()
                    else:
                        print("Invalid move, try again.")
                        
                    # Deselect after move attempt.
                    self.selected_piece = None
                    self.selected_position = None   
                    
    def handle_keydown(self, event):
        """Handle keydown events."""
        if event.key == pygame.K_f:
            self.toggle_flip_view()
            self.draw_squares()
            print("Flipped view!")
        
        if self.board_history:
            if event.key == pygame.K_LEFT:
                
                # Handle going back in history
                old_board = self.board_history.pop()
                self.chessgame.set_board(old_board)
                self.draw_squares()
                
                if old_board:
                    print("Went back in history!")
                
        # Handle going forward in history   

    
    # here we run the game
    def run(self):
        """ Main game loop """
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                # Listen for keydown events
                if event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)
                    
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self.play_turn(event)
                    
            
            
            
            
           

        # Quit Pygame
        pygame.quit()
    
