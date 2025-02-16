import board as Board


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
    
    def add_move_to_legal_moves(self, move: str, legal_moves: list) -> bool:
        if self.board.is_valid_move(move, self):
            legal_moves.append(move)
            return True
        return False
    
    
class Pawn(Piece):
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Pawn', position, board)
        self.has_moved = False
        
    def en_passant(self):
        pass
    
    def promote(self, choice: Piece):
        if choice.type not in ['Queen', 'Rook', 'Bishop', 'Knight']:
            print('Invalid promotion choice')
            return False
        
        # Create a new piece of the chosen type and place it on the board
        new_piece = getattr(Piece, choice)(self.color, self.position, self.board)
        self.board.place_piece(new_piece, self.position)
        return True
            
    # this append the legal moves of the pawn to the list of legal moves
    def big_pawn_move(self, x:int, y:int, direction, possible_moves: list):
        
         # Move forward by 2 squares on the first move (only if both squares are empty)
        if not self.has_moved and (y == 1 or y == 6):
            
            intermediate_position = self.board.coordinate_to_position((x, y + direction))
            final_position = self.board.coordinate_to_position((x, y + 2 * direction))
            
            if not self.board.get_piece_at_position(intermediate_position) and not self.board.get_piece_at_position(final_position):
                possible_moves.append((x, y + 2 * direction))
                
    def diagonal_capture(self, x:int, y:int, direction: int, possible_moves):
        for dx in [-1, 1]:  # Check both left (-1) and right (+1) diagonal
            target_x, target_y = x + dx, y + direction
            target_position = self.board.coordinate_to_position((target_x, target_y))
            
            target_piece = self.board.get_piece_at_position(target_position)
            
            if target_piece and target_piece.color != self.color:  # Enemy piece
                possible_moves.append((target_x, target_y))

    def calculate_legal_moves(self) -> list:
        possible_moves = []

        # I have accidentally made it so x is the column and y is the row
        x, y = self.board.position_to_coordinate(self.position)  # Get 0-7 coordinates
        print(f'{x,y} are the coordinates, {self.position} is the position')
        
        # Determine direction based on color
        direction = 1 if self.color == 'White' else -1

        # Move forward by 1 square (only if the square is empty)
        if not self.board.get_piece_at_position(self.board.coordinate_to_position((x, y + direction))):
            possible_moves.append((x, y + direction))

        #can we add a big pawn move here?
        self.big_pawn_move(x, y, direction, possible_moves)
        
        # Capture diagonally (check if the target square contains an enemy piece)
        self.diagonal_capture(x, y, direction, possible_moves)
        
        # Convert valid coordinates to positions and return only legal moves
        legal_moves = [
            self.board.coordinate_to_position(move) 
            for move in possible_moves 
            if self.board.is_valid_move(self.board.coordinate_to_position(move), self)
        ]
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves
     
class Rook(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Rook', position, board)
        self.has_moved = False

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.board.position_to_coordinate(self.position)
        
        legal_moves = []
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Four possible directions for the rook
            for i in range(1, 8):  # Maximum range for a rook
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.board.coordinate_to_position((target_x, target_y))
                
                if not self.add_move_to_legal_moves(target_position, legal_moves):
                    break  # Stop searching in this direction if blocked by any piece
                
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Knight(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Knight', position, board)

    def calculate_legal_moves(self):
        # Retrieve the current board state and convert the knight's position (e.g., 'g1') into (x, y) coordinates.
        board = self.board
        x, y = self.board.position_to_coordinate(self.position)
        
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
            target_position = self.board.coordinate_to_position((target_x, target_y))
            #print(f'{target_position }is targetposition for {self.color}{self.position} knight')
            
            if not self.add_move_to_legal_moves(target_position, legal_moves):
                continue  # Skip this move if it goes off the board
            
        return legal_moves

class Bishop(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Bishop', position, board)

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.board.position_to_coordinate(self.position)
        
        legal_moves = []

        # Diagonal directions for the bishop
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Four diagonals
            for i in range(1, 8):  # Maximum range for a bishop
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.board.coordinate_to_position((target_x, target_y))
                if not self.add_move_to_legal_moves(target_position, legal_moves):
                    break
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Queen(Piece):
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'Queen', position, board)
        
    def calculate_legal_moves(self):
        board = self.board
        x, y = self.board.position_to_coordinate(self.position)
        
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
                target_position = self.board.coordinate_to_position((target_x, target_y))
                
                if not self.add_move_to_legal_moves(target_position, legal_moves):
                    break
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class King(Piece):
    
    def __init__(self, color, position, board: Board):
        super().__init__(color, 'King', position, board)
        self.has_moved = False
    
    def castle(self):
        pass
    
    def is_in_check(self):
        pass
                        
    def calculate_legal_moves(self):
        # Get the current board and convert the king's position (e.g., 'e4') to (x, y) coordinates.
        board = self.board
        x, y = self.board.position_to_coordinate(self.position)
        
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
            target_position = self.board.coordinate_to_position((target_x, target_y))
            
            if not self.add_move_to_legal_moves(target_position, legal_moves):
                continue
        
        #print(f'{legal_moves} are the legal moves for the King.')
        return legal_moves


