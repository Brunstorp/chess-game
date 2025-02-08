import pygame
import board as B  # Assuming you have a separate `board.py` with a Board class.
from pieces import Piece
# Initialize pygame
pygame.init()

class GUI:
    def __init__(self):
        # Initialize board
        self.chessboard = B.Board()
        self.chessboard.setup()
        
        # Window settings
        self.WIDTH, self.HEIGHT = 600, 600
        self.SQUARE_SIZE = self.WIDTH // 8
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Game")
        
        # Load piece images
        self.load_images()
        
        # Draw the board and pieces intially
        self.draw_board()
        self.draw_pieces()
        
        # Run the game
        self.run()
        
    def load_images(self):
        # Load piece images
        self.piece_images = {}
        for color in ["white", "black"]:
            for piece_type in ["pawn", "rook", "knight", "bishop", "queen", "king"]:
                piece_name = f"{color}_{piece_type}"  # Example: "white_pawn"
                image = pygame.image.load(f"../pictures/{piece_name}.png")
                self.piece_images[piece_name] = pygame.transform.scale(
                    image,
                    (self.SQUARE_SIZE, self.SQUARE_SIZE)  # Scale to match board squares
                )
                
    def get_coordinates(self, position: str) -> tuple:
        col, row = position
        x = (ord(col) - 97) * self.SQUARE_SIZE
        y = (8 - int(row)) * self.SQUARE_SIZE
        return x, y
        
    def draw_pieces(self):
        for row in range(8, 0, -1):  # Rows 8 to 1 (standard chess notation)
            for col in 'abcdefgh':  # Columns a to h
                position = f'{col}{row}'
                self.draw_piece(self.chessboard.board.get(position), position)
           
    # this is to draw a generic piece         
    def draw_piece(self, piece: Piece, position: str):
        piece = self.chessboard.board.get(position)
        col, row = position
        if piece:
            piece_name = f"{piece.color}_{piece.type}".lower()
            x,y = self.get_coordinates(position)
            self.screen.blit(self.piece_images[piece_name], (x, y))
            
    def clear_square(self, position: str):
        x, y = self.get_coordinates(position)
        color = self.colors[(x + y) % 2]
        pygame.draw.rect(
            self.screen,
            color,
            pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
        )

    def draw_board(self):
        """ Draw the chessboard """
        self.colors = [(255, 255, 255), (139, 69, 19)]  # White and Brown
        for row in range(8):
            for col in range(8):
                color = self.colors[(row + col) % 2]  # Alternate between white and black
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

    def run(self):
        """ Main game loop """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.clear_square('a1')
            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

# Run the GUI
if __name__ == '__main__':
    gui = GUI()
