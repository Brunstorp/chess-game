class Piece:
    def __init__(self, color, type, position):
        self.color = color
        self.type = type
        self.position = position
        
    def __str__(self):
        return self.color + self.type
    
    def move(self):
        pass
    
    def capture(self):  
        pass
    
    def is_valid_move(self):
        pass
    
    def is_valid_capture(self):
        pass
    
    def is_valid_position(self):
        pass
    
    
class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'Pawn', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
    
class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, 'Rook', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
    
class Knight(Piece):    
    def __init__(self, color, position):
        super().__init__(color, 'Knight', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
    
class Bishop(Piece):        
    def __init__(self, color, position):
        super().__init__(color, 'Bishop', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
    
class Queen(Piece):    
    def __init__(self, color, position):
        super().__init__(color, 'Queen', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
    
class King(Piece):      
    def __init__(self, color, position):
        super().__init__(color, 'King', position)
        
    def move(self):
        pass
    
    def capture(self):
        pass
