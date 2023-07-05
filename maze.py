
from random import choice, randint


from block import Block
from create_image import CreateImage

class MazeCreator:
    def __init__(self, rows: int, columns : int):
        self.rows = rows
        self.columns = columns

        self.__setup()
        CreateImage(self.grid)

    def __setup(self) -> None:
        self.grid = []
        self.__set_grid()
        self.__create_maze()

    # Initialize the grid with blocks
    def __set_grid(self):
        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
                block = Block(row, column)
                self.grid[-1].append(block)

    def __create_maze(self) -> None:
        block_stack = []

        start_block = self.__get_block(0,0)
        current_block  = self.__delete_wall_and_get_next_block(start_block)
        start_block.visited = True

        block_stack.append(start_block)

        while current_block != start_block:
            current_block = self.__delete_wall_and_get_next_block(current_block)
            if not current_block:
                block_stack.pop()
                current_block = block_stack[-1]
            else:
                block_stack.append(current_block)

        # Remove the walls of staritng and ending position
        self.__remove_start_and_end_walls()

    def __get_block(self, row, column) -> Block:
        return self.grid[row][column]

    def __delete_wall_and_get_next_block(self, block : Block):
        unvisited_neighbours =  self.__unvisited_neighbours(block)
        if len(unvisited_neighbours) == 0:
            return False 
        
        # Randomly selects next unvisited block
        direction, next_block = choice(unvisited_neighbours)

        # Remove the wall between current block and next block
        match direction:
            case (-1,0):
                block.remove_wall('left')
                next_block.remove_wall('right')
            case (1,0):
                block.remove_wall('right')
                next_block.remove_wall('left')
            case (0,-1):
                block.remove_wall('top')
                next_block.remove_wall('bottom')     
            case (0,1):
                block.remove_wall('bottom')
                next_block.remove_wall('top')

        next_block.visited = True

        return next_block

    # Return list of unvisited neighbours block
    def __unvisited_neighbours(self, block):
        unvisited_neighbours_list = []
        row,column = block.get_pos()

        adjancent_blocks = [
            (0,1), (0,-1), (1,0), (-1,0)   
        ]

        for i,j in adjancent_blocks:

            if not (0 <= row + j < self.rows and 0 <= column+i < self.columns):
                continue 
            block = self.__get_block(row+j, column+i)
            if not block.has_visited():
                unvisited_neighbours_list.append([(i,j), block])

        return unvisited_neighbours_list

    # Create the starting and ending of maze
    def __remove_start_and_end_walls(self):
        start_row = randint(0, self.rows-1)
        end_row = randint(0, self.rows-1)
        start_block = self.__get_block(start_row,0)
        end_block = self.__get_block(end_row, self.columns-1)

        start_block.remove_wall('left')
        end_block.remove_wall('right')
