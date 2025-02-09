import pygame
import board as B  # Assuming you have a separate `board.py` with a Board class.
from pieces import Piece
# Initialize pygame
pygame.init()

class GUI:
    def __init__(self, size=600):
        # Initialize board
        self.chessboard = B.Board()
        self.chessboard.setup()
        
        # Window settings
        self.WIDTH = self.HEIGHT = size
        self.SQUARE_SIZE = self.WIDTH // 8
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Game")
        
        # Load piece images
        self.load_images()
        
        # Draw the board and pieces intially
        self.colors = [(255, 255, 255), (139, 69, 19)]  # White and Brown color codes
        self.draw_board()
        self.draw_pieces()
        
        # Selected piece
        self.selected_piece = None
        self.selected_position = None
        
        # Run the game
        self.run()
        
    def load_images(self):
        # Load piece images
        self.piece_images = {}
        colors = self.chessboard.colors
        piece_types = self.chessboard.pieces.copy()  # Add pawn to the list of pieces and copy so we don't change in the original list
        piece_types.append('Pawn')
        
        for color in colors:
            for piece_type in piece_types:
                piece_name = f"{color}_{piece_type}".lower()  # Example: "white_pawn"
                image = pygame.image.load(f"../pictures/{piece_name}.png")
                self.piece_images[piece_name] = pygame.transform.scale(
                    image,
                    (self.SQUARE_SIZE, self.SQUARE_SIZE)  # Scale to match board squares
                )
          
    # this is to go from say 'a1' to whatever that becomes in the window      
    def get_window_coordinates(self, position: str) -> tuple:
        col, row = position
        x = (ord(col) - 97) * self.SQUARE_SIZE
        y = (8 - int(row)) * self.SQUARE_SIZE
        return x, y
    
    # and this is obviously just the inverse of the above function
    def get_position(self, x: int, y: int) -> str:
        col = chr(x // self.SQUARE_SIZE + 97)
        row = str(8 - y // self.SQUARE_SIZE)
        return f'{col}{row}'
        
    # this draws the pieces initially
    def draw_pieces(self):
        for row in range(8, 0, -1):  # Rows 8 to 1 (standard chess notation)
            for col in 'abcdefgh':  # Columns a to h
                position = f'{col}{row}'
                if position in self.chessboard.board:
                    self.draw_piece(self.chessboard.board.get(position), position)
           
    # this is to draw a generic piece         
    def draw_piece(self, piece: Piece, position: tuple, ):
        col, row = position
        if piece:
            piece_name = f"{piece.color}_{piece.type}".lower()
            x,y = self.get_window_coordinates(position)
            self.screen.blit(self.piece_images[piece_name], (x, y))
            
    def draw_square(self,x:int,y:int): # this takes in the coordinates in the window
        color = self.colors[((x + y) // self.SQUARE_SIZE) % 2]
        pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(x, y, self.SQUARE_SIZE, self.SQUARE_SIZE)
                )
        
    # this clears up the square    
    def clear_square(self, position: str):
        x, y = self.get_window_coordinates(position)
        print(f'trying to clear {position} with coordinates {x,y}')
        self.draw_square(x,y)
        
    # this moves the piece in the window, I think I can use this later when implementing special moves like castling
    # position here is the position we are going to move the piece to, selected is the the one selected already
    def move_piece(self, piece: Piece, position: str):
        self.clear_square(position)
        self.draw_piece(piece, position)
        self.clear_square(self.selected_position)

    # this draws the board
    def draw_board(self):
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
            clicked_position = self.get_position(mouse_x, mouse_y)  # Convert pixel position to board position

            if not self.selected_piece:
                # First click: Select a piece
                selected_piece = self.chessboard.board.get(clicked_position)
                
                if selected_piece:  # Check if there's a piece on the selected square
                    self.selected_piece = selected_piece
                    self.selected_position = clicked_position
                    print('Selected:', self.selected_piece, self.selected_position)
                    legal_moves = selected_piece.get_legal_moves()
                    
            else:
                # Second click: Attempt to move the piece
                print(f'Trying to move {self.selected_piece} from {self.selected_position} to {clicked_position}') 
                # here I want to add that if we try to move to a square that is occupied by a piece of the same color, that square shpuld just be selected instead
                success = self.chessboard.move_piece(self.selected_position, clicked_position)
                if success:
                    self.move_piece(self.selected_piece, clicked_position)  # Update the board state and GUI
                    print('Move successful!')
                else:
                    print('Did not move, try again.')
                
                # Deselect the piece after the move attempt
                self.selected_piece = None
                self.selected_position = None
    
    # here we run the game
    def run(self):
        """ Main game loop """
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
                if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    self.play_turn(event)
            
            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()

# Run the GUI
if __name__ == '__main__':
    gui = GUI(900)
