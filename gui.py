from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.filedialog import askopenfile

from maze import MazeCreator
from maze_solution import MazeSolution

class GUI(Tk):
    def __init__(self):
        super().__init__()
        self.title('Maze Creator')
        self.geometry('500x400')
        self.wm_resizable(False, False)

        self.rows = IntVar() 
        self.columns = IntVar() 
        self.selected_file = None

        self.__place_title_label()

        self.__create_buttons_frame()

        self.maze_create_frame = self.__create_maze_frame()
        self.solve_maze_frame = self.__create_solver_frame()

        self.maze_create_frame.pack()

        self.mainloop()

    def __place_title_label(self):
        label = Label(self, text='Welcome to the Maze World!', font=('Arial Bold',24))
        label.pack(pady=10)

    def __create_buttons_frame(self):
        frame = Frame(self, relief=GROOVE, borderwidth=5)
        Button(frame,text="Create Maze", font=('Arial',15), command=self.__select_maze_create_frame).pack(side=LEFT, ipadx=10, ipady=10, padx=10)
        Button(frame,text="Solve Maze", font=('Arial',15), command=self.__select_maze_solver_frame).pack(side=LEFT, ipadx=10, ipady=10, padx=10)
        frame.pack(ipady=10)

    def __create_maze_frame(self):
        frame = Frame(self)
        self.__create_inputs(frame)
        self.__create_maze_button(frame)
        return frame

    def __create_inputs(self, frame):
        Label(frame, text='Rows', font=('Arial',18)).pack()
        Entry(frame, textvariable=self.rows , font=('Arial Bold',18)).pack(padx=10, pady=10)

        Label(frame, text='Columns', font=('Arial',18)).pack()
        Entry(frame, textvariable=self.columns, font=('Arial Bold',18)).pack(padx=10, pady=10)

    def __create_maze_button(self, frame):
        Button(frame, text='Create', font=('Arial Bold', 18),command=self.__create_maze ).pack(pady=10)

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

    def __create_solver_frame(self):
        frame = Frame(self)
        self.__create_file_chooser_button(frame)
        self.__create_solve_maze_button(frame)
        return frame
    
    def __create_file_chooser_button(self, frame):
        Button(frame, text='Select File', command=self.__choose_file, font=('Arial', 15)).pack(ipadx=5, ipady=5, pady = 10)

    def __choose_file(self):
        self.selected_file =  askopenfile(title='Select maze file',
        initialdir='.',
        filetypes=(('PNG', '*.png'),)).name

    def __create_solve_maze_button(self, frame):
        Button(frame, text='Solve', font=('Arial Bold', 18),command=self.__solve_maze ).pack(pady=10)

    def __solve_maze(self):
        MazeSolution(self.selected_file)
        showinfo('Maze Solved', 'Maze Solved')

    def __select_maze_create_frame(self):
        self.maze_create_frame.pack()
        self.solve_maze_frame.pack_forget()  
    def __select_maze_solver_frame(self):
        self.maze_create_frame.pack_forget()
        self.solve_maze_frame.pack()  
    
if __name__ == '__main__':
    GUI()