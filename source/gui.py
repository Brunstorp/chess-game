import pygame

# Initialize pygame
pygame.init()

class GUI:
    def __init__(self):
        # Window settings
        self.WIDTH, self.HEIGHT = 600, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Chess Game")
        chessboard = pygame.image.load("../pictures/chess_board.png")
        self.chessboard = pygame.transform.scale(chessboard, (self.WIDTH, self.HEIGHT))
        
        self.run()
        
    def run(self):
        # Main game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Draw the board
            self.screen.blit(self.chessboard, (0, 0))

            # Update the display
            pygame.display.flip()

        # Quit Pygame
        pygame.quit()
        
# Run the GUI
if __name__ == '__main__':
    gui = GUI()
