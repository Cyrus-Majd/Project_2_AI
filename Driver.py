from Grid import Grid
import os




if __name__ == "__main__":
    
    grid = Grid(mapname = "maps/map1/map1.txt")
    grid.run_from_truth_file("maps/map1/map1truth1.txt")
    grid.print_probabilities()

        

    #grid = Grid(5, 5)
    #grid.print_obstacles()
    #grid.print_probabilities()
    #grid.move_down()
    #grid.print_probabilities()
    #grid.observe("N")
    #grid.print_probabilities()

