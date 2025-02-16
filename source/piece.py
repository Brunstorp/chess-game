import board as Board
import move as Move

class Piece:
    def __init__(self, color, type, position, board: Board):
        self.color = color
        self.type = type
        self.position = position
        self.board = board  # Store the board as an instance variable
        self.is_pinned = False
        self.legal_moves = []

    def __str__(self):
        return self.color + self.type
    
    # this sets the position of the piece
    def set_position(self, position): 
        self.position = position
    
    # getter to above
    def get_position(self): 
        return self.position
        
    def update_legal_moves(self):
        self.legal_moves = self.calculate_legal_moves()
    
    #This returns the legal moves of the piece
    def get_legal_moves(self) -> list: 
        return self.legal_moves

    def calculate_legal_moves(self) -> list:
        raise NotImplementedError("Pieces must implement calculate_legal_moves method")
    
    def coordinate_to_position(self, coordinate: tuple) -> str:
        col, row = coordinate
        position = f'{chr(col + 97)}{row + 1}'  # Column to letter, row to 1-based index
        return position

    # Convert chess position (e.g., 'a1') to 0-7 coordinates
    def position_to_coordinate(self, position: str) -> tuple:
        col, row = position
        coordinate = (ord(col) - 97, int(row) - 1)  # Letter to column index, 1-based to 0-based
        return coordinate
    
    # this checks if the square is inside the grid, maybe not necessary but nice to have
    def is_valid_position(self, position): 
        if len(position) != 2:
            return False
        col, row = position
        if col not in 'abcdefgh' or row not in '12345678':
            return False
        return True
    
    # this checks if a move is valid, a move is then not a capture
    def is_valid_move(self,move_position: str):
        # since we cannot click outside the square this works
        if self.get_piece_on(move_position) == None: 
            return self.is_valid_position(move_position)
        else:
            # we check if it is not the same color as it's own and if it is a valid position
            return self.is_valid_position(move_position) and not self.get_piece_on(move_position).color == self.color 
        
    def get_piece_on(self, position):
        return self.board.get_piece_at_position(position)
    

class Pawn(Piece):
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Pawn', position, board)
        self.has_moved = False
        
    def en_passant(self):
        pass
    
    def promotion(self):
        pass
    
    def big_pawn_move(self):
        pass
        
    def calculate_legal_moves(self) -> list:
        possible_moves = []

        board = self.board
        x, y = self.position_to_coordinate(self.position)  # Get 0-7 coordinates
        
        # Determine direction based on color
        direction = 1 if self.color == 'White' else -1

        # Move forward by 1 square (only if the square is empty)
        if not board.get_piece_at_position(self.coordinate_to_position((x, y + direction))):
            possible_moves.append((x, y + direction))

        # Move forward by 2 squares on the first move (only if both squares are empty)
        if not self.has_moved and (x == 1 or x==6):
            
            intermediate_position = self.coordinate_to_position((x, y + direction))
            final_position = self.coordinate_to_position((x, y + 2 * direction))
            
            if not board.get_piece_at_position(intermediate_position) and not board.get_piece_at_position(final_position):
                possible_moves.append((x, y + 2 * direction))

        # Capture diagonally (check if the target square contains an enemy piece)
        for dx in [-1, 1]:  # Check both left (-1) and right (+1) diagonal
            target_x, target_y = x + dx, y + direction
            target_position = self.coordinate_to_position((target_x, target_y))
            
            target_piece = board.get_piece_at_position(target_position)
            if target_piece and target_piece.color != self.color:  # Enemy piece
                possible_moves.append((target_x, target_y))

        # Convert valid coordinates to positions and return only legal moves
        legal_moves = [
            self.coordinate_to_position(move) 
            for move in possible_moves 
            if self.is_valid_move(self.coordinate_to_position(move))
        ]
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves
     
class Rook(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Rook', position, board)
        self.has_moved = False

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Four possible directions for the rook
            for i in range(1, 8):  # Maximum range for a rook
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.coordinate_to_position((target_x, target_y))
                
                if not self.is_valid_move(target_position):  # Check if the position is valid, either that it is blocked by friendly piece or outside the board
                    break  # Stop searching in this direction
                
                target_piece = board.get_piece_at_position(target_position)
                
                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop looking further in this direction if blocked by any piece
                
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Knight(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Knight', position, board)

    def calculate_legal_moves(self):
        # Retrieve the current board state and convert the knight's position (e.g., 'g1') into (x, y) coordinates.
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        
        # Define all eight L-shaped moves for a knight.
        # Each tuple represents (dx, dy): the change in x and y coordinates.
        moves = [
            (2, 1),    # Two squares right, one square up.
            (2, -1),   # Two squares right, one square down.
            (-2, 1),   # Two squares left, one square up.
            (-2, -1),  # Two squares left, one square down.
            (1, 2),    # One square right, two squares up.
            (1, -2),   # One square right, two squares down.
            (-1, 2),   # One square left, two squares up.
            (-1, -2)   # One square left, two squares down.
        ]
        
        # Iterate over each possible knight move.
        for dx, dy in moves:
            target_x, target_y = x + dx, y + dy
            target_position = self.coordinate_to_position((target_x, target_y))
            #print(f'{target_position }is targetposition for {self.color}{self.position} knight')
            
            target_position = self.coordinate_to_position((target_x, target_y))
            if not self.is_valid_move(target_position):  # Check if valid move
                continue  # Skip this move if it goes off the board
            
            target_piece = board.get_piece_at_position(target_position)

            if not target_piece:  # Empty square
                legal_moves.append(target_position)
                
            else:
                if target_piece.color != self.color:  # Opponent's piece
                    legal_moves.append(target_position)
              
        
        return legal_moves

class Bishop(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Bishop', position, board)

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []

        # Diagonal directions for the bishop
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Four diagonals
            for i in range(1, 8):  # Maximum range for a bishop
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.coordinate_to_position((target_x, target_y))
                if not self.is_valid_move(target_position):  # Check if within bounds
                    break  # Stop searching in this direction
                
                target_piece = board.get_piece_at_position(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Queen(Piece):
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Queen', position, board)
        
    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []

        # Directions for the queen (diagonal + straight-line)
        directions = [
            (1, 1), (1, -1), (-1, 1), (-1, -1),  # Diagonal
            (0, 1), (0, -1), (1, 0), (-1, 0)     # Horizontal and vertical
        ]

        # Iterate over all possible directions
        for dx, dy in directions:
            for i in range(1, 8):  # Maximum range for a queen
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.coordinate_to_position((target_x, target_y))
                
                if not self.is_valid_move(target_position):  # Check if within bounds
                    break  # Stop searching in this direction
                
                target_piece = board.get_piece_at_position(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class King(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'King', position, board)
        self.has_moved = False
        self.is_checked = False
                        
    def calculate_legal_moves(self):
        # Get the current board and convert the king's position (e.g., 'e4') to (x, y) coordinates.
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        
        # The king can move one square in any of the eight directions.
        directions = [
            (1, 1),   # Up-Right
            (1, -1),  # Down-Right
            (-1, 1),  # Up-Left
            (-1, -1), # Down-Left
            (0, 1),   # Up
            (0, -1),  # Down
            (1, 0),   # Right
            (-1, 0)   # Left
        ]
        
        # Check each direction for a valid move.
        for dx, dy in directions:
            # Calculate the target coordinates by moving one square in the given direction.
            target_x, target_y = x + dx, y + dy
            target_position = self.coordinate_to_position((target_x, target_y))
            
            # Ensure the target position is on the board.
            if not self.is_valid_move(target_position):
                continue  # Skip this direction if it goes off the board.
            
            target_piece = board.get_piece_at_position(target_position)
            
            # A move is legal if the target square is empty or contains an opponent's piece.
            if not target_piece or target_piece.color != self.color:
                legal_moves.append(target_position)
        
        #print(f'{legal_moves} are the legal moves for the King.')
        return legal_moves


