from PIL import ImageDraw
import PIL.Image
from random import choice, randint
from tkinter import *
from tkinter.messagebox import showinfo, showerror


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

class MazeCreator:
    def __init__(self, rows: int, columns : int):
        self.rows = rows
        self.columns = columns

        self.__setup()
        self.__create_image()

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

    def __create_image(self):
        grid_block = 20
        line_width = 2

        image_width = self.columns * grid_block + line_width
        image_height = self.rows * grid_block + line_width
        image = PIL.Image.new("RGB", (image_width, image_height))

        draw = ImageDraw.Draw(image)

        for row, block_row in enumerate(self.grid):
            for column, block in enumerate(block_row):
                top_left = ( column*grid_block, row*grid_block )
                top_right = ( (column + 1)*grid_block, row*grid_block )
                bottom_right = ( (column + 1) *grid_block, (row + 1)*grid_block)
                bottom_left = ( column*grid_block, (row + 1)*grid_block )

                if block.has_wall('left'):
                    coords = ( top_left, bottom_left )
                    draw.line(coords, fill=(255,0,0), width=line_width)

                if block.has_wall('right'):
                    coords = ( top_right, bottom_right )
                    draw.line(coords, fill=(255,0,0), width=line_width)

                if block.has_wall('top'):
                    coords = ( top_left, top_right )
                    draw.line(coords, fill=(255,0,0), width=line_width)

                if block.has_wall('bottom'):
                    coords = ( bottom_left, bottom_right )
                    draw.line(coords, fill=(255,0,0), width=line_width)
        image.save('maze.png', 'PNG')


class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title('Maze Creator')
        self.geometry('500x300')

        self.rows = IntVar() 
        self.columns = IntVar() 

        self.__place_title_label()
        self.__create_inputs()
        self.__create_maze_button()
        self.mainloop()

    def __place_title_label(self):
        label = Label(self, text='Welcome to the Maze Generator!', font=('Arial Bold',18))
        label.pack()

    def __create_inputs(self):
        Label(self, text='Rows', font=('Arial',18)).pack()
        Entry(self, textvariable=self.rows , font=('Arial Bold',18)).pack(padx=10, pady=10)

        Label(self, text='Columns', font=('Arial',18)).pack()
        Entry(self, textvariable=self.columns, font=('Arial Bold',18)).pack(padx=10, pady=10)

    def __create_maze_button(self):
        Button(self, text='Create', font=('Arial Bold', 18),command=self.__create_maze ).pack(pady=10)

    def __create_maze(self):
        try:
            rows = self.rows.get()
            columns = self.columns.get()

            if rows and columns:
                MazeCreator(rows, columns)
                showinfo('Maze Created', 'Maze Created')
            else:
                    showerror('Invalid', 'Invalid row or column')
        except:
            showerror('Invalid', 'Invalid row or column')

        self.rows.set(0)
        self.columns.set(0)

if __name__ == '__main__':
    GUI()
    # rows = int(input('Enter number of rows in maze: '))
    # columns = int(input('Enter number of columns in maze: '))
    # MazeCreator(10,10)