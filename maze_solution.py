from PIL import Image
import numpy as np
from block import Block
from create_image import CreateImage

class MazeSolution:
    def __init__(self, image_path):
        self.image = Image.open(image_path).convert('L')
        self.image_array = np.asarray(self.image)

        self.width = self.image.width-2
        self.height = self.image.height-2

        self.rows = self.height//20
        self.columns = self.width//20

        self.grid = []

        self.__set_grid()
        self.__set_vertical_walls()
        self.__set_horizontal_walls()
        solution = self.__solve_maze()
        CreateImage(self.grid, solution=solution )

    def __set_grid(self):
        for row in range(self.rows):
            self.grid.append([])
            for column in range(self.columns):
                block = Block(row, column)
                self.grid[-1].append(block)

    def __set_horizontal_walls(self):
        current_x = 10
        current_y = 20

        while current_x != self.width + 10:
            current_y = 20
            while current_y != self.height:
                if self.image_array[current_y][current_x] == 0:
                    row = current_y // 20 - 1
                    column = current_x // 20
                    block1 = self.__get_block(row, column)
                    block2 = self.__get_block(row+1, column)

                    block1.remove_wall('bottom')
                    block2.remove_wall('top')

                current_y+=20
            current_x+=20

    def __set_vertical_walls(self):
        current_x = 20
        current_y = 10

        while current_y != self.height + 10:
            current_x = 20
            while current_x != self.width:
                if self.image_array[current_y][current_x] == 0:
                    row = current_y // 20
                    column = current_x // 20 - 1
                    block1 = self.__get_block(row, column)
                    block2 = self.__get_block(row, column+1)

                    block1.remove_wall('right')
                    block2.remove_wall('left')

                current_x+=20
            current_y+=20
                 
    def __get_block(self, row,column) -> Block:
        return self.grid[row][column]

    def __solve_maze(self):
        solution = []
        starting_coords = (self.__get_maze_starting_row(), 0)
        ending_coords = (self.__get_maze_ending_row(), self.columns-1)

        start_block = self.__get_block(*starting_coords)
        solution.append(start_block)
        start_block.visited = True

        end_block = self.__get_block(*ending_coords)

        current_block = start_block


        while current_block != end_block:
            movable_blocks = self.__get_movable_blocks(current_block)
            if not movable_blocks:
                solution.pop()
                current_block = solution[-1]
            else:
               current_block = movable_blocks[0][1]
               solution.append(current_block)
               current_block.visited = True


        solution.append(end_block)
        
        return solution

    def __get_movable_blocks(self, block):
        movable_blocks_list = []
        row,column = block.get_pos()

        adjancent_blocks = [
            (0,1), (0,-1), (1,0), (-1,0)   
        ]

        for i,j in adjancent_blocks:
            if not (0 <= row + j < self.rows and 0 <= column+i < self.columns):
                continue 
            block = self.__get_block(row+j, column+i)
            if not block.has_visited():
                match (i,j):
                    case (0,1):
                        if block.has_wall('top'):
                            continue
                    case (0,-1):
                        if block.has_wall('bottom'):
                            continue
                    case (-1,0):
                        if block.has_wall('right'):
                            continue
                    case (1,0):
                        if block.has_wall('left'):
                            continue
                movable_blocks_list.append([(i,j), block])
            
        return movable_blocks_list

    def __get_maze_starting_row(self):
        for index,data  in enumerate(self.image_array):
            if  not data[0]:
                return index//20
    def __get_maze_ending_row(self):
        for index,data  in enumerate(self.image_array):
            if  not data[-1]:
                return index//20


if __name__ == '__main__':
    m = MazeSolution('./maze.png')