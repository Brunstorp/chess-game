import pygame
import chessgame as ChessGame  # Assuming you have a separate `board.py` with a Board class.
import chess


# Initialize pygame
pygame.init()

class GUI:
    def __init__(self, chessgame: ChessGame, size=600):
        
        self.chessgame = chessgame
        self.chessboard = chessgame.get_board()
        
        # Window settings
        self.WIDTH = self.HEIGHT = size
        self.SQUARE_SIZE = self.WIDTH // 8
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        
        pygame.display.set_caption("Chess Game")
        
        # Draw the board and pieces intially
        self.colors = [(255, 255, 255), (139, 69, 19)]  # White and Brown color codes
        self.draw_squares()
        self.draw_pieces()
        
        # Selected piece
        self.selected_piece = None
        self.selected_position = None
        
        # Run the game
        self.running = False
        
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
        col, row = position
        x = (ord(col) - 97) * self.SQUARE_SIZE
        y = (8 - int(row)) * self.SQUARE_SIZE
        return x, y
    
    # and this is obviously just the inverse of the above function
    def get_position_from_coordinates(self, x: int, y: int) -> str:
        col = chr(x // self.SQUARE_SIZE + 97)
        row = str(8 - y // self.SQUARE_SIZE)
        return f'{col}{row}'
        
    # this draws all th epieces on the board
    def draw_pieces(self):
        for row in range(8, 0, -1):  # Rows 8 to 1 (standard chess notation)
            for col in 'abcdefgh':  # Columns a to h
                square_str = f'{col}{row}'
                square = chess.parse_square(square_str)
                piece = self.chessboard.piece_at(square)
                if piece:
                    self.draw_piece(piece, square)
           
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
            
    def draw_square(self,x:int,y:int): # this takes in the coordinates in the window
        color = self.colors[((x + y) // self.SQUARE_SIZE) % 2]
        pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

    # this draws the board, meaning the background
    def draw_squares(self):
        """ Draw the chessboard """
        for row in range(8):
            for col in range(8):
                x = row*self.SQUARE_SIZE
                y = col*self.SQUARE_SIZE
                self.draw_square(x,y)
                
    # later I might have to implemet a way for the computer to access aswell
    def play_turn(self, event):
        """Handle mouse clicks to select and move pieces."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button clicked
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            col = mouse_x // self.SQUARE_SIZE
            row = mouse_y // self.SQUARE_SIZE
            
            clicked_position = self.get_position_from_coordinates(mouse_x, mouse_y)  # Convert pixel position to board position
            
            if not self.selected_piece:
                # First click: Select a piece
                selected_square = chess.parse_square(clicked_position)
                selected_piece = self.chessboard.piece_at(selected_square)
                
                if selected_piece:  # Check if there's a piece on the selected square
                    self.selected_piece = selected_piece
                    self.selected_position = clicked_position
                    print('Selected:', self.selected_piece, self.selected_position)
                       
            else:
                
                # Second click: Attempt to move the piece
                print(f'Trying to move {self.selected_piece} from {self.selected_position} to {clicked_position}') 
                
                # here I want to add that if we try to move to a square that is occupied by a piece of the same color, that square shpuld just be selected instead
                from_square = chess.parse_square(self.selected_position)
                to_square = chess.parse_square(clicked_position)
                
                success = self.chessgame.play_turn(from_square, to_square)
                
                if success:
                    print('Move successful!')
                    
                else:
                    print('Did not move, try again.')
                    
                # Deselect the piece after the move attempt
                self.selected_piece = None
                self.selected_position = None
                
                
    
    # here we run the game
    def run(self):
        """ Main game loop """
        self.running = True
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                    
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self.play_turn(event)
            
            # realized it is so fast that I can just brute force the whole thing, sometimes it is nice to be lazy engineering
            self.draw_squares()
            self.draw_pieces()
            
            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
    
