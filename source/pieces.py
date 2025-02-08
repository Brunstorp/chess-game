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

    def is_valid_position(self, position):
        col, row = position
        if col not in 'abcdefgh' or row not in '12345678':
            return False
        return True
    
    # this checks if a move is valid, a move is then not a capture
    def is_valid_move(self,move_position: str):
        if self.get_piece_on(move_position) == None:
            return self.is_valid_position(move_position)
        else:
            return self.is_valid_position(move_position) and not self.get_piece_on(move_position).color == self.color
        
    # this checks if a capture is valid, a capture is then a capture
    def is_valid_capture(self,capture_position: str):
        if self.get_piece_on(capture_position) != None:
            return self.is_valid_position(capture_position) and not self.get_piece_on(capture_position).color == self.color
        else:
            return False
    
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
        
        board = self.board
        x,y = self.get_coordinates()
        possible_moves = []
        bw = 1 if self.color == 'White' else -1 # black or white, determines which direction the pawn moves
        
        
        # I will add all to the possible moves in terms of coordinates, and then change them to positions
        # I will also add every possible move, and then check if it is a valid position and clean the list afterwards
        if not self.has_moved:
            possible_moves.append((x,y+2*bw))
            
        possible_moves.append((x,y+bw))
            
        legal_moves = [self.coordinate_to_position(move) for move in possible_moves if self.is_valid_move(self.coordinate_to_position(move))]
        print(f'{legal_moves} are the legal moves')
        return legal_moves

    def get_legal_captures(self):
        pass


class Rook(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Rook', position, board)
        self.has_moved = False

    def get_possible_moves(self):
        # Example: Implement rook-specific logic using self.board
        pass

    def get_legal_captures(self):
        pass


class Knight(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Knight', position, board)

    def get_possible_moves(self):
        # Example: Implement knight-specific logic using self.board
        pass

    def get_legal_captures(self):
        pass


class Bishop(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Bishop', position, board)

    def get_possible_moves(self):
        # Example: Implement bishop-specific logic using self.board
        pass

    def get_legal_captures(self):
        pass


class Queen(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'Queen', position, board)

    def get_possible_moves(self):
        # Example: Implement queen-specific logic using self.board
        pass

    def get_legal_captures(self):
        pass


class King(Piece):
    def __init__(self, color, position, board: dict):
        super().__init__(color, 'King', position, board)
        self.has_moved = False

    def get_possible_moves(self):
        # Example: Implement king-specific logic using self.board
        pass

    def get_legal_captures(self):
        pass
