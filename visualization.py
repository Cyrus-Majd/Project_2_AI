from tkinter import *
from typing import List

from Grid import *


def lerp(a, b, t):
    return a * (1 - t) + b * t


def getColFromGradient(probability):
    LOWER_BOUND = [255, 0, 0]
    UPPER_BOUND = [0, 255, 0]
    return "#" + ''.join(map(lambda x: f'{int(x):x}'.zfill(2),
                             [lerp(c, w, probability) for c, w in zip(LOWER_BOUND, UPPER_BOUND)]))


class Node:
    SELECTED_COLOR = "cyan"
    EMPTY_COLOR = "black"
    START_COLOR = "green"
    END_COLOR = "red"
    NODE_SIZE_MOD = 0.4

    def __init__(self, master, x, y, size, padding):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.padding = padding
        self.selected = False
        self.start = False
        self.end = False

    def toggle(self):
        self.selected = not self.selected

    def set_start(self):
        self.start = True

    def set_goal(self):
        self.end = True

    def corners_screen_coords(self) -> tuple[tuple[int, int], tuple[int, int]]:
        x0 = int((self.abs * self.size) - Node.NODE_SIZE_MOD * self.size / 2 + self.padding)
        x1 = int(x0 + self.size * Node.NODE_SIZE_MOD)
        y0 = int((self.ord * self.size) - Node.NODE_SIZE_MOD * self.size / 2 + self.padding)
        y1 = int(y0 + self.size * Node.NODE_SIZE_MOD)
        return (x0, y0), (x1, y1)

    def draw(self):
        if self.master is not None:
            bcol = "black"
            if self.end:
                col = Node.END_COLOR
                if self.selected:
                    bcol = Node.SELECTED_COLOR
            elif self.start:
                col = Node.START_COLOR
                if self.selected:
                    bcol = Node.SELECTED_COLOR
            elif self.selected:
                col = Node.SELECTED_COLOR
            else:
                col = Node.EMPTY_COLOR

            (x0, y0), (x1, y1) = self.corners_screen_coords()

            self.master.create_oval(x0, y0, x1, y1, fill=col, outline=bcol)


class Cell:
    heatMapCol = "red"
    BLOCKED_COLOR = "black"
    EMPTY_COLOR = 'white'
    BORDER_COLOR = "black"

    def __init__(self, master, x, y, size, padding):
        self.master = master
        self.abs = x
        self.ord = y
        self.size = size
        self.padding = padding
        self.filled = False

    def setCol(self, heatMapCol):
        self.heatMapCol = heatMapCol

    def draw(self):
        if self.master is not None:
            col = Cell.BLOCKED_COLOR
            if not self.filled:
                col = self.heatMapCol

            x0 = self.abs * self.size + self.padding
            x1 = x0 + self.size
            y0 = self.ord * self.size + self.padding
            y1 = y0 + self.size

            self.master.create_rectangle(x0, y0, x1, y1, outline=Cell.BORDER_COLOR, fill=col)
            """if not self.filled:
                self.master.create_line(x0, y0, x1, y1)
                self.master.create_line(x0, y1, x1, y0)"""


class PathSegment:
    LINE_COLOR = "magenta"

    def __init__(self, master, p0: tuple[int, int], p1: tuple[int, int], size: float, padding: float):
        self.master = master
        self.abs, self.ord = p0
        self.abs2, self.ord2 = p1
        self.size = size
        self.padding = padding
        self.filled = False

    def corners_screen_coords(self) -> tuple[tuple[int, int], tuple[int, int]]:
        x0 = int((self.abs * self.size) + self.padding)
        x1 = int((self.abs2 * self.size) + self.padding)
        y0 = int((self.ord * self.size) + self.padding)
        y1 = int((self.ord2 * self.size) + self.padding)
        return (x0, y0), (x1, y1)

    def draw(self):
        if self.master is not None:
            (x0, y0), (x1, y1) = self.corners_screen_coords()
            self.master.create_line(x0, y0, x1, y1, fill=PathSegment.LINE_COLOR, width=2, tags="pathsegment")


class GuiGrid(Canvas):
    heatmap = []

    def __init__(self, master, row_num: int, col_num: int, cell_size: int, padding: int, *args, **kwargs):
        Canvas.__init__(self, master, width=cell_size * col_num + padding * 2,
                        height=cell_size * row_num + padding * 2, *args, **kwargs)

        self.cellSize = cell_size
        self.padding = padding

        self.cells = []
        for row in range(row_num):
            line = []
            for column in range(col_num):
                line.append(Cell(self, column, row, cell_size, padding))

            self.cells.append(line)

    def bind_grid(self, heatmap: List[List[float]]):
        self.heatmap = heatmap

    def draw(self, heatmap):
        for row in range(len(self.cells)):
            for col in range(len(self.cells[0])):
                cellCol = getColFromGradient(heatmap[row][col])
                self.cells[row][col].setCol(cellCol)
                self.cells[row][col].draw()

    def fill_obstacle(self, row: int, col: int):
        self.cells[row][col].filled = True
        self.cells[row][col].draw()


def load_map(map_file: str) -> tuple[Tk, GuiGrid]:
    with open(map_file) as f:
        cell_grid = []
        for line in f:
            cell_grid.append(ast.literal_eval(line))

        app = Tk()

        gui_grid = GuiGrid(app, len(cell_grid), len(cell_grid[0]), 10, 8)
        gui_grid.grid(row=0, column=0)
        # gui_grid.pack(pady=10, padx=10)
        # values_label.pack()

        for row in range(len(cell_grid)):
            for col in range(len(cell_grid[row])):
                if cell_grid[row][col] == 'B':
                    gui_grid.fill_obstacle(row, col)

        return app, gui_grid


def run_app(app):
    app.mainloop()
