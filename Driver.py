from Grid import Grid
import os




if __name__ == "__main__":
    
    for i in range(1, 11):
        curr_map = f"maps/map{i}"
        if not os.path.exists(curr_map):
            os.makedirs(curr_map)
        g = Grid()
        g.export_to_dir(curr_map, i)

        

    #grid = Grid(5, 5)
    #grid.print_obstacles()
    #grid.print_probabilities()
    #grid.move_down()
    #grid.print_probabilities()
    #grid.observe("N")
    #grid.print_probabilities()

