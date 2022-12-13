from tkinter import *
from typing import List

from Grid import *


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
    heatMapCol = "black"
    EMPTY_COLOR = "white"
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
            col = self.heatMapCol
            if not self.filled:
                col = Cell.EMPTY_COLOR

            x0 = self.abs * self.size + self.padding
            x1 = x0 + self.size
            y0 = self.ord * self.size + self.padding
            y1 = y0 + self.size

            self.master.create_rectangle(x0, y0, x1, y1, outline=Cell.BORDER_COLOR, fill=col)
            if not self.filled:
                self.master.create_line(x0, y0, x1, y1)
                self.master.create_line(x0, y1, x1, y0)


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
    def __init__(self, master, row_num: int, col_num: int, cell_size: int, padding: int,
                 values_label: Label, *args, **kwargs):
        Canvas.__init__(self, master, width=cell_size * col_num + padding * 2,
                        height=cell_size * row_num + padding * 2, *args, **kwargs)

        self.cellSize = cell_size
        self.padding = padding
        self.vertex_values_label = values_label

        """self.nodes = []
        for row in range(row_num + 1):
            line = []
            for column in range(col_num + 1):
                line.append(Node(self, column, row, cell_size, padding))

            self.nodes.append(line)"""

        self.cells = []
        """self.paths = []
        self.robs = []"""
        for row in range(row_num):
            line = []
            for column in range(col_num):
                line.append(Cell(self, column, row, cell_size, padding))

            self.cells.append(line)

        # self.bind("<Button-1>", self.handle_mouse_click)

        self.draw()
        # self.selected = None
        # self.start = None
        # self.end = None
        self.heatmap = None

    def bind_grid(self, heatmap: List[List[float]]):
        self.heatmap = heatmap

    def lerp(self, a, b, t):
        return a * (1 - t) + b * t

    def getColFromGradient(self, probability):
        LOWER_BOUND = [255, 0, 0]
        UPPER_BOUND = [0, 255, 0]
        return "#" + ''.join([self.lerp(c, w, probability) for c, w in zip(LOWER_BOUND, UPPER_BOUND)])

    def draw(self):
        for row in range(len(self.cells)):
            for col in range(row):
                cellCol = self.getColFromGradient(self.heatmap[row][col])
                self.cells[row][col].setCol(cellCol)
                self.cells[row][col].draw()
        """for row in self.cells:
            for cell in row:
                cell.draw()

        for row in self.nodes:
            for cell in row:
                cell.draw()"""

    """def event_grid_coords(self, event: Event):
        row = int((event.y + self.cellSize / 2 - self.padding) / self.cellSize)
        column = int((event.x + self.cellSize / 2 - self.padding) / self.cellSize)
        return row, column

    def handle_mouse_click(self, event: Event):
        row, col = self.event_grid_coords(event)
        if row > len(self.nodes) - 1 or col > len(self.nodes[0]) - 1:
            return
        cell = self.nodes[row][col]
        if self.selected is not None:
            self.selected.toggle()
            self.selected.draw()
        self.selected = cell
        self.selected.toggle()
        self.selected.draw()
        self.update_vertex_info(self.path_grid.terrain[col][row])
        print(self.path_grid.terrain[col][row].print())"""

    def fill_obstacle(self, row: int, col: int):
        self.cells[row][col].filled = True
        self.cells[row][col].draw()
        self.robs.append((row, col))

    def clear_obstacle(self, row: int, col: int):
        self.cells[row][col].filled = False
        self.cells[row][col].draw()
        self.robs.remove((row, col))

    """def set_start(self, row: int, col: int):
        if self.start is not None:
            self.start.start = False
            self.nodes[row][col].draw()
        self.nodes[row][col].start = True
        self.nodes[row][col].draw()
        self.start = self.nodes[row][col]

    def set_end(self, row: int, col: int):
        if self.end is not None:
            self.end.end = False
            self.nodes[row][col].draw()
        self.nodes[row][col].end = True
        self.nodes[row][col].draw()
        self.end = self.nodes[row][col]

    def add_path(self, p0: tuple[int, int], p1: tuple[int, int]):
        path = PathSegment(self, p0, p1, self.cellSize, self.padding)
        self.paths.append(path)
        path.draw()

    def remove_path(self, p0, p1):
        self.paths = [x for x in self.paths if x.p0 != p0 and x.p1 != p1]

    def update_vertex_info(self, node):
        self.vertex_values_label.config(text=node.print())"""


"""def trace(pathfinding_grid: Grid, gui_grid: GuiGrid):
    current_vert = pathfinding_grid.goal_node
    while current_vert.parent is not None and (current_vert.x_coordinate, current_vert.y_coordinate) != (
            pathfinding_grid.start_node.x_coordinate, pathfinding_grid.start_node.y_coordinate):
        print((current_vert.x_coordinate, current_vert.y_coordinate))
        parent_node = current_vert.parent
        gui_grid.add_path((current_vert.x_coordinate, current_vert.y_coordinate),
                          (parent_node.x_coordinate, parent_node.y_coordinate))
        current_vert = parent_node
        # (pathfinding_grid.goal_node.x_coordinate, pathfinding_grid.goal_node.y_coordinate)
    print((current_vert.x_coordinate, current_vert.y_coordinate))"""


# Todo refactor and make generic
def load_map(map_file: str) -> tuple[Tk, GuiGrid]:
    with open(map_file) as f:
        start_col, start_row = list(map(int, f.readline().strip().split()))
        end_col, end_row = list(map(int, f.readline().strip().split()))
        cols, rows = list(map(int, f.readline().strip().split()))

        app = Tk()

        values_label = Label(app, text="Click on a node to start")
        gui_grid = GuiGrid(app, rows, cols, 20, 8, values_label)
        gui_grid.grid(row=0, column=0)
        values_label.grid(row=0, column=1)
        # gui_grid.pack(pady=10, padx=10)
        # values_label.pack()

        gui_grid.set_start(start_row - 1, start_col - 1)
        gui_grid.set_end(end_row - 1, end_col - 1)

        lines = f.readlines()
        for line in lines:
            col, row, val = list(map(int, line.strip().split()))
            if val == 1:
                gui_grid.fill_obstacle(row - 1, col - 1)

        return app, gui_grid


def run_app(app):
    app.mainloop()
