from PIL import  ImageDraw
import PIL.Image

class CreateImage:
    def __init__(self, grid, solution=None):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])
        self.solution = solution

        self.__setup()
        self.__create_image()

    def __setup(self):
        self.grid_block = 20
        self.line_width = 2

        image_width = self.columns * self.grid_block + self.line_width
        image_height = self.rows * self.grid_block + self.line_width

        self.image = PIL.Image.new("RGB", (image_width, image_height))
        self.draw = ImageDraw.Draw(self.image)

    def __create_image(self):

        if self.solution:
            self.__draw_solution()
        self.__draw_maze()

        self.image.save('maze.png' if not self.solution else 'maze_solution.png', 'PNG')

    def __draw_solution(self):
            for block in self.solution:
                row,column = block.get_pos()
                top_left = ( column*self.grid_block, row*self.grid_block )
                bottom_right = ( (column + 1) *self.grid_block, (row + 1)*self.grid_block)
                self.draw.rectangle( ((top_left), (bottom_right)), fill=(255,255,255) )

    def __draw_maze(self):
        for row, block_row in enumerate(self.grid):
            for column, block in enumerate(block_row):
                top_left = ( column*self.grid_block, row*self.grid_block )
                top_right = ( (column + 1)*self.grid_block, row*self.grid_block )
                bottom_right = ( (column + 1) *self.grid_block, (row + 1)*self.grid_block)
                bottom_left = ( column*self.grid_block, (row + 1)*self.grid_block )

                self.__draw_wall(block, place='left', coords= ( top_left, bottom_left ) )
                self.__draw_wall(block, place='right', coords= ( top_right, bottom_right ) )
                self.__draw_wall(block, place='top', coords= ( top_left, top_right ) )
                self.__draw_wall(block, place='bottom', coords= ( bottom_left, bottom_right ))

    def __draw_wall(self, block, place, coords):
            if block.has_wall(place):
                    self.draw.line(coords, fill=(255,0,0), width=self.line_width)
