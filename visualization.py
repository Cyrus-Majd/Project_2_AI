from tkinter import *

from Grid import *


def lerp(a, b, t):
    return a * (1 - t) + b * t


def getColFromGradient(probability):
    LOWER_BOUND = [4095, 0, 0]
    UPPER_BOUND = [0, 4095, 0]
    return "#" + ''.join(map(lambda x: f'{int(x):x}'.zfill(3),
                             [lerp(c, w, probability) for c, w in zip(LOWER_BOUND, UPPER_BOUND)]))


class Cell:
    heatMapCol = "red"
    BLOCKED_COLOR = "black"
    EMPTY_COLOR = 'white'
    BORDER_COLOR = "black"
    REAL_POSITION_COLOR = 'cyan'

    def __init__(self, master, x, y, size, padding):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.padding = padding
        self.filled = False
        self.realPos = False
        self.redraw = True

    def setRealPos(self, newVal):
        self.realPos = newVal
        self.redraw = True

    def setCol(self, heatMapCol):
        if self.heatMapCol != heatMapCol:
            self.heatMapCol = heatMapCol
            self.redraw = True

    def draw(self):
        if self.master is not None and self.redraw:
            col = Cell.BLOCKED_COLOR
            if not self.filled:
                col = self.heatMapCol

            x0 = self.abs * self.size + self.padding
            x1 = x0 + self.size
            y0 = self.ord * self.size + self.padding
            y1 = y0 + self.size

            self.master.create_rectangle(x0, y0, x1, y1,
                                         outline=Cell.REAL_POSITION_COLOR if self.realPos else Cell.BORDER_COLOR,
                                         fill=col)
            # if self.realPos:
            qSize = int((x1 - x0) / 2.0)
            self.master.create_oval(x0 + qSize, y0- qSize, x1- qSize, y1- qSize, fill=Cell.REAL_POSITION_COLOR, outline=Cell.REAL_POSITION_COLOR)
            """if not self.filled:
                self.master.create_line(x0, y0, x1, y1)
                self.master.create_line(x0, y1, x1, y0)"""
        self.redraw = False


class GuiGrid(Canvas):

    def __init__(self, master, row_num: int, col_num: int, cell_size: int, padding: int, *args, **kwargs):
        Canvas.__init__(self, master, width=cell_size * col_num + padding * 2,
                        height=cell_size * row_num + padding * 2, *args, **kwargs)

        self.cellSize = cell_size
        self.padding = padding

        self.realPosCell = None
        self.cells = []
        # for row in range(row_num):
        #     line = []
        #     for column in range(col_num):
        #         line.append(Cell(self, column, row, cell_size, padding))
        #
        #     self.cells.append(line)
        for row in range(row_num):
            line = []
            for col in range(col_num):
                line.append(Cell(self, col, row, cell_size, padding))

            self.cells.append(line)

    def bind_grid(self, grid):
        self.grid = grid

    def setRealPos(self, row, col):
        if self.realPosCell is not None:
            self.realPosCell.setRealPos(False)
        self.realPosCell = self.cells[row][col]
        self.realPosCell.setRealPos(True)

    def draw(self):
        maxProb: float = max(map(lambda x: max(x), self.grid.probability_field))
        normalizedHeatmap = [[x / maxProb for x in i] for i in self.grid.probability_field]
        # print(self.grid.mostProbable())
        # print(normalizedHeatmap)
        for row in range(len(self.cells)):
            for col in range(len(self.cells[row])):
                cellCol = getColFromGradient(normalizedHeatmap[row][col])
                self.cells[row][col].setCol(cellCol)
                self.cells[row][col].draw()

    def fill_obstacle(self, row: int, col: int):
        self.cells[row][col].filled = True
        self.cells[row][col].draw()


instructionsQ = []


def load_map(map_file: str, instructions) -> tuple[Tk, GuiGrid]:
    with open(map_file) as f:
        cell_grid = []
        for line in f:
            cell_grid.append(ast.literal_eval(line))

        app = Tk()

        gui_grid = GuiGrid(app, len(cell_grid), len(cell_grid[0]), 10, 8)
        gui_grid.grid(row=0, column=0)

        for instruction in instructions:
            instructionsQ.insert(0, instruction)

        def stepOnceCB():
            gui_grid.grid.stepOnce(instructionsQ.pop(), gui_grid)
            gui_grid.draw()

        def stepTenCB():
            for i in range(10):
                gui_grid.grid.stepOnce(instructionsQ.pop(), gui_grid)
            gui_grid.draw()

        def stepAllCB():
            for i in range(len(instructionsQ)):
                gui_grid.grid.stepOnce(instructionsQ.pop(), gui_grid)
            gui_grid.draw()

        btnFrame = Frame(app)
        forwardOneBtn = Button(btnFrame, text="Forward 1 step", command=stepOnceCB)
        forwardTenBtn = Button(btnFrame, text="Forward 10 steps", command=stepTenCB)
        forwardAllBtn = Button(btnFrame, text="Forward all steps", command=stepAllCB)
        gui_grid.grid(row=0, column=0)
        btnFrame.grid(row=0, column=1)
        # forwardOneBtn.grid(row=0, column=1)
        # forwardTenBtn.grid(row=0, column=1)
        # forwardAllBtn.grid(row=0, column=1)
        # gui_grid.pack(pady=10, padx=10)
        forwardOneBtn.pack()
        forwardTenBtn.pack()
        forwardAllBtn.pack()

        # values_label.pack()

        for row in range(len(cell_grid)):
            for col in range(len(cell_grid[row])):
                if cell_grid[row][col] == 'B':
                    gui_grid.fill_obstacle(row, col)

        return app, gui_grid


def run_app(app):
    app.mainloop()
