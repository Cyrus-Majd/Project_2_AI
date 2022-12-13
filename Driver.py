import visualization
from Grid import Grid
import os

if __name__ == "__main__":
    grid = Grid(mapname="maps/map1/map1.txt")
    app, gui_grid = visualization.load_map("maps/map1/map1.txt")
    gui_grid.bind_grid(grid.probability_field)
    grid.run_from_truth_file("maps/map1/map1truth1.txt")
    gui_grid.draw(grid.probability_field)
    app.mainloop()

    # grid = Grid(mapname="maps/map1/map1.txt")
    # grid.print_obstacles()
    # grid.print_probabilities()
    # grid.move_down()
    # grid.print_probabilities()
    # grid.observe("N")
    # grid.print_probabilities()
