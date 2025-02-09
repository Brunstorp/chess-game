class Piece:
    def __init__(self, color, type, position, board: dict):
        self.color = color
        self.type = type
        self.position = position
        self.board = board  # Store the board as an instance variable
        self.is_pinned = False

    def __str__(self):
        return self.color + self.type
    
    def get_piece_on(self,position):
        return self.board.get(position)

    def get_legal_moves(self) -> list:
        pass

    def is_valid_position(self, position): # this checks if the square is inside the grid, maybe not necessary but nice to have
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

    def get_coordinates(self):
        return self.position_to_coordinate(self.position)
    
    def get_position(self):
        return self.position
    

class Pawn(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Pawn', position, board)
        self.has_moved = False
        
    def get_legal_moves(self) -> list:
        possible_moves = []
        if self.is_pinned:
            return possible_moves  # Pawns cannot move if pinned

        board = self.board
        x, y = self.position_to_coordinate(self.position)  # Get 0-7 coordinates
        
        # Determine direction based on color
        direction = 1 if self.color == 'White' else -1

        # Move forward by 1 square (only if the square is empty)
        if  not board.get(self.coordinate_to_position((x, y + direction))):
            possible_moves.append((x, y + direction))

        # Move forward by 2 squares on the first move (only if both squares are empty)
        if not self.has_moved:
            intermediate_position = self.coordinate_to_position((x, y + direction))
            final_position = self.coordinate_to_position((x, y + 2 * direction))
            if not board.get(intermediate_position) and not board.get(final_position):
                possible_moves.append((x, y + 2 * direction))

        # Capture diagonally (check if the target square contains an enemy piece)
        for dx in [-1, 1]:  # Check both left (-1) and right (+1) diagonal
            target_x, target_y = x + dx, y + direction
            target_position = self.coordinate_to_position((target_x, target_y))
            target_piece = board.get(target_position)
            if target_piece and target_piece.color != self.color:  # Enemy piece
                possible_moves.append((target_x, target_y))

        # Convert valid coordinates to positions and return only legal moves
        legal_moves = [
            self.coordinate_to_position(move) 
            for move in possible_moves 
            if self.is_valid_move(self.coordinate_to_position(move))
        ]
        
        print(f'{legal_moves} are the legal moves')
        return legal_moves
     
class Rook(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Rook', position, board)
        self.has_moved = False

    def get_legal_moves(self):
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
                target_piece = board.get(target_position)
                
                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop looking further in this direction if blocked by any piece
                
        print(f'{legal_moves} are the legal moves')
        return legal_moves

        


class Knight(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Knight', position, board)

    def get_legal_moves(self):
        # Example: Implement knight-specific logic using self.board
        pass


class Bishop(Piece):
    
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Bishop', position, board)

    def get_legal_moves(self):
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
                if not self.is_valid_position(target_position):  # Check if within bounds
                    break  # Stop searching in this direction
                
                
                target_piece = board.get(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        print(f'{legal_moves} are the legal moves')
        return legal_moves


class Queen(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Queen', position, board)

    def get_legal_moves(self):
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
                if not self.is_valid_position(target_position):  # Check if within bounds
                    break  # Stop searching in this direction
                
                
                target_piece = board.get(target_position)

                if not target_piece:  # Empty square
                    legal_moves.append(target_position)
                else:
                    if target_piece.color != self.color:  # Opponent's piece
                        legal_moves.append(target_position)
                    break  # Stop searching further in this direction if blocked by any piece
        
        print(f'{legal_moves} are the legal moves')
        return legal_moves



class King(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'King', position, board)
        self.has_moved = False

    def get_legal_moves(self):
        # Example: Implement king-specific logic using self.board
        pass

