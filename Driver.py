import ast

import visualization
from Grid import Grid


def run100Experiments():
    allErrs = []
    avgErrs = []
    for mapNum in range(1, 11):
        for truth in range(1, 11):
            print(f'running {(mapNum - 1) * 10 + truth}')
            grid = Grid(mapname=f"maps/map{mapNum}/map{mapNum}.txt")
            allErrs.append(grid.averageErrorFromTruth(f"maps/map{mapNum}/map{mapNum}truth{truth}.txt"))
    for i in range(0, 95):
        columnSum = 0.0
        for err in allErrs:
            columnSum += err[i]
        avgErrs.append(columnSum / len(allErrs))
        with(open("outFiles/out1.txt", "w")) as f:
            f.writelines(list(map(lambda x: f"({x[0] + 6}, {x[1]})\n", [(i, y) for i, y in enumerate(avgErrs)])))


if __name__ == "__main__":
    # run100Experiments()

    # grid = Grid(mapname="maps/map2/map2.txt")
    #
    # with open("maps/map2/map2truth6.txt") as f:
    #     real_moves_list = ast.literal_eval(next(f))
    #     real_position_list = ast.literal_eval(next(f))
    #     moves_list = ast.literal_eval(next(f))
    #     observations_list = ast.literal_eval(next(f))
    #     instructions = zip(real_position_list, moves_list, observations_list)
    #
    # app, gui_grid = visualization.load_map("maps/map2/map2.txt", instructions)
    # gui_grid.bind_grid(grid)
    # # grid.run_from_truth_file("maps/map1/map1truth1.txt")
    # gui_grid.draw()
    # app.mainloop()
    #
    # grid = Grid()
    # Grid.export_10_maps()

    grid = Grid()
    grid.print_probabilities()
    grid.run_default_comms_and_obs()

    # grid = Grid(5, 5)
    # grid.print_obstacles()
    # grid.print_probabilities()
    # grid.move_down()
    # grid.print_probabilities()
    # grid.observe("N")
    # grid.print_probabilities()
    # Grid(5, 5).export_10_maps()
