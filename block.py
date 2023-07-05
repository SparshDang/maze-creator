class Block:
    def __init__(self, row, columm):
        self.row = row
        self.column = columm
        self.visited = False
        self.walls = {'top':True, 'bottom':True, 'left':True, 'right':True}

    def  get_pos(self):
        return self.row, self.column
    
    def has_visited(self):
        return self.visited

    def has_wall(self, place):
        return self.walls.get(place)
    
    def remove_wall(self, place):
        self.walls.update({place: False})
