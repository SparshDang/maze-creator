from PIL import  ImageDraw
import PIL.Image

class CreateImage:
    def __init__(self, grid, solution=None):
        self.grid = grid
        self.rows = len(grid)
        self.columns = len(grid[0])

        self.solution = solution

        self.__create_image()

    def __create_image(self):
        grid_block = 20
        line_width = 2

        image_width = self.columns * grid_block + line_width
        image_height = self.rows * grid_block + line_width
        image = PIL.Image.new("RGB", (image_width, image_height))

        draw = ImageDraw.Draw(image)

        if self.solution:
            for block in self.solution:
                row,column = block.get_pos()
                top_left = ( column*grid_block, row*grid_block )
                bottom_right = ( (column + 1) *grid_block, (row + 1)*grid_block)
                draw.rectangle( ((top_left), (bottom_right)), fill=(255,255,255) )


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
        image.save('maze.png' if not self.solution else 'maze_solution.png', 'PNG')