import board as B

class Piece:
    def __init__(self, color, type, position, board: B):
        self.color = color
        self.type = type
        self.position = position
        self.board = board  # Store the board as an instance variable
        self.is_pinned = False
        self.legal_moves = []
        self.special_moves = []

    def __str__(self):
        return self.color + self.type
    
    def get_piece_on(self,position): # this returns the piece on the board of position
        return self.board.get_at_position(position)
    
    '''def clear_up_checking_moves(self, moves):
        #print(f'{moves} are the moves')
        from_position = self.position
        for move in moves:
            if self.board.move_puts_king_in_check(from_position, move):
                moves.remove(move)
        return moves'''
    
    def update_legal_moves(self):
        self.legal_moves = self.calculate_legal_moves()
    
    def get_legal_moves(self) -> list: #This returns the legal moves of the piece, and clears the moves which would put the king in check for that person
        return  self.legal_moves

    def calculate_legal_moves(self) -> list:
        pass
    
    def get_special_moves(self) -> list:
        return self.special_moves
    
    def calculate_special_moves(self):
        pass
    
    def update_special_moves(self):
        self.special_moves = self.calculate_special_moves()
    
    def is_pinned(self):
        pass
    
    def set_position(self, position): # this sets the position of the piece
        self.position = position
    
    def get_position(self): # getter to above
        return self.position
    
    def get_coordinates(self):
        return self.position_to_coordinate(self.position)

    def is_valid_position(self, position): # this checks if the square is inside the grid, maybe not necessary but nice to have
        if len(position) != 2:
            return False
        col, row = position
        if col not in 'abcdefgh' or row not in '12345678':
            return False
        return True
    
    # this checks if a move is valid, a move is then not a capture
    def is_valid_move(self,move_position: str):
        if self.get_piece_on(move_position) == None: # since we cannot click outside the square this works
            return self.is_valid_position(move_position)
        else:
            return self.is_valid_position(move_position) and not self.get_piece_on(move_position).color == self.color # we check if it is not the same color as it's own and
    
    def coordinate_to_position(self, coordinate: tuple) -> str:
        col, row = coordinate
        position = f'{chr(col + 97)}{row + 1}'  # Column to letter, row to 1-based index
        return position

    # Convert chess position (e.g., 'a1') to 0-7 coordinates
    def position_to_coordinate(self, position: str) -> tuple:
        col, row = position
        coordinate = (ord(col) - 97, int(row) - 1)  # Letter to column index, 1-based to 0-based
        return coordinate
    
    # below we override equal function and hash function to make sure we can compare pieces and use them in dicts and sets
    def __eq__(self, other):
        if other is None:
            return False
        return self.color == other.color and self.type == other.type and self.position == other.position
    
    def __hash__(self):
        return hash((self.color, self.type, self.position))


class Pawn(Piece):
    def __init__(self, color, position, board: B):
        super().__init__(color, 'Pawn', position, board)
        self.has_moved = False
        
    # this needs to handle enpassant and promotion
    def calculate_special_moves(self):
        pass
        
    def calculate_legal_moves(self) -> list:
        possible_moves = []
        if self.is_pinned:
            return possible_moves  # Pawns cannot move if pinned

        board = self.board
        x, y = self.position_to_coordinate(self.position)  # Get 0-7 coordinates
        
        # Determine direction based on color
        direction = 1 if self.color == 'White' else -1

        # Move forward by 1 square (only if the square is empty)
        if not board.get_at_position(self.coordinate_to_position((x, y + direction))):
            possible_moves.append((x, y + direction))

        # Move forward by 2 squares on the first move (only if both squares are empty)
        if not self.has_moved:
            intermediate_position = self.coordinate_to_position((x, y + direction))
            final_position = self.coordinate_to_position((x, y + 2 * direction))
            if not board.get_at_position(intermediate_position) and not board.get_at_position(final_position):
                possible_moves.append((x, y + 2 * direction))

        # Capture diagonally (check if the target square contains an enemy piece)
        for dx in [-1, 1]:  # Check both left (-1) and right (+1) diagonal
            target_x, target_y = x + dx, y + direction
            target_position = self.coordinate_to_position((target_x, target_y))
            target_piece = board.get_at_position(target_position)
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
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Rook', position, board)
        self.has_moved = False

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        if self.is_pinned:
            print('Pinned')
            return legal_moves
        
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:  # Four possible directions for the rook
            for i in range(1, 8):  # Maximum range for a rook
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.coordinate_to_position((target_x, target_y))
                
                if not self.is_valid_move(target_position):  # Check if the position is valid, either that it is blocked by friendly piece or outside the board
                    break  # Stop searching in this direction
                target_piece = board.get_at_position(target_position)
                
                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop looking further in this direction if blocked by any piece
                
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Knight(Piece):
    def __init__(self, color, position, board: B):
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
            
            target_piece = board.get_at_position(target_position)

            if not target_piece:  # Empty square
                legal_moves.append(target_position)
            else:
                if target_piece.color != self.color:  # Opponent's piece
                    legal_moves.append(target_position)
              
        
        return legal_moves

class Bishop(Piece):
    
    def __init__(self, color, position, board: B):
        super().__init__(color, 'Bishop', position, board)

    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        if self.is_pinned:
            print('Pinned')
            return legal_moves  # Bishop cannot move if pinned

        # Diagonal directions for the bishop
        for dx, dy in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:  # Four diagonals
            for i in range(1, 8):  # Maximum range for a bishop
                target_x, target_y = x + i * dx, y + i * dy
                target_position = self.coordinate_to_position((target_x, target_y))
                if not self.is_valid_move(target_position):  # Check if within bounds
                    break  # Stop searching in this direction
                
                target_piece = board.get_at_position(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class Queen(Piece):
    def __init__(self, color, position, board: B):
        super().__init__(color, 'Queen', position, board)
        
    def calculate_legal_moves(self):
        board = self.board
        x, y = self.position_to_coordinate(self.position)
        
        legal_moves = []
        if self.is_pinned:
            print('Pinned')
            return legal_moves  # Queen cannot move if pinned

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
                
                target_piece = board.get_at_position(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        #print(f'{legal_moves} are the legal moves')
        return legal_moves

class King(Piece):
    
    def __init__(self, color, position, board: B):
        super().__init__(color, 'King', position, board)
        self.has_moved = False
        self.is_checked = False
        
    # This needs to handle castling
    def calculate_special_moves(self):
        pass
                        
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
            
            if not board.is_square_safe(target_position, self.color):
                continue  # Skip this direction if the king is moving into check.
            
            target_piece = board.get_at_position(target_position)
            
            # A move is legal if the target square is empty or contains an opponent's piece.
            if not target_piece or target_piece.color != self.color:
                legal_moves.append(target_position)
        
        #print(f'{legal_moves} are the legal moves for the King.')
        return legal_moves


