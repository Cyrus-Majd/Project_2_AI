import random


class Grid:
    def __init__(self, row_num = -1, col_num = -1):
        if((row_num == -1 and col_num != -1) or (row_num != -1 and col_num == -1)):
            raise Exception("either no positional arguments or both positional arguments")
        elif(row_num == -1 and col_num == -1):
            preset = ["H", "H", "T", "N", "N", "N", "N", "B", "H"]
            n = 3
            self.obstacle_grid = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    self.obstacle_grid[i][j] = preset[(n * i) + j]

        else:
            self.obstacle_grid = [[0] * row_num for _ in range(col_num)]
            for i in range(row_num):
                for j in range(col_num):
                    rand_val = random.random()
                    if (rand_val < .10):    # Blocked cell
                        self.obstacle_grid[i][j] = "B"
                    elif (rand_val < .40):  # Hard to traverse cell
                        self.obstacle_grid[i][j] = "T"
                    elif (rand_val < .70):  # Highway cell
                        self.obstacle_grid[i][j] = "H"
                    else:                   # Normal cell
                        self.obstacle_grid[i][j] = "N"
            

        bs = 0
        for arr in self.obstacle_grid:
            for ele in arr:
                if(ele == "B"):
                    bs += 1

        unblocked = len(self.obstacle_grid) * len(self.obstacle_grid[0]) - bs
        distributed_prob = 1 / unblocked
        probability_field = [[0] * len(self.obstacle_grid) for _ in range(len(self.obstacle_grid[0]))]
        for row in range(len(probability_field)):
            for col in range(len(probability_field[row])):
                if (self.obstacle_grid[row][col] == "B"):
                    probability_field[row][col] = 0
                else:
                    probability_field[row][col] = distributed_prob

        self.obstacle_grid = self.obstacle_grid
        self.probability_field = probability_field

    def run_default_comms_and_obs(self):
        self.move_right()
        self.observe("N")
        self.print_probabilities()

        self.move_right()
        self.observe("N")
        self.print_probabilities()

        self.move_down()
        self.observe("H")
        self.print_probabilities()

        self.move_down()
        self.observe("H")
        self.print_probabilities()

    
    def observe(self, letter):
        for row in range(len(self.obstacle_grid)):
            for col in range(len(self.obstacle_grid[row])):
                if(self.obstacle_grid[row][col] == letter):
                    self.probability_field[row][col] *= 0.9
                else:
                    self.probability_field[row][col] *= 0.05

        self.probability_field = self.normalize(self.probability_field)


    def generate_vector():
        vector = [0, 0]
        ud_or_rl = random.randint(0, 1)
        if(ud_or_rl == 1):
            #up or down
            vector[0] = random.choice([-1, 1])
            vector[1] = 0
        else:
            vector[0] = 0
            vector[1] = random.choice([-1, 1])
        return vector
        
    def generate_truths(self):
        start_row = random.randint(0, len(self.obstacle_grid) - 1)
        start_col = random.randint(0, len(self.obstacle_grid[0]) - 1)
        while(self.obstacle_grid[start_row][start_col] == "B"):
            start_row = random.randint(0, len(self.obstacle_grid) - 1)
            start_col = random.randint(0, len(self.obstacle_grid[0]) - 1)

        curr_position = [start_row, start_col]
        true_positions = []
        true_movements = []
        true_observations = []
        
        for i in range(100):
            vec = Grid.generate_vector()
            possible = [0, 0]
            possible[0] = curr_position[0] + vec[0]
            possible[1] = curr_position[1] + vec[1]
            
            while(possible[0] < 0 or possible[0] >= len(self.obstacle_grid) or possible[1] < 0 or possible[1] >= len(self.obstacle_grid[0]) or self.obstacle_grid[possible[0]][possible[1]] == "B"):
                vec = Grid.generate_vector()
                possible = [0, 0]
                possible[0] = curr_position[0] + vec[0]
                possible[1] = curr_position[1] + vec[1]


            curr_position = possible
            
            true_positions.append((curr_position[0], curr_position[1]))

            if(vec[0] == 1):
                true_movements.append("U")
            elif(vec[0] == -1):
                true_movements.append("D")
            elif(vec[1] == 1):
                true_movements.append("R")
            elif(vec[1] == -1):
                true_movements.append("L")

            true_observations.append(self.obstacle_grid[curr_position[0]][curr_position[1]])

        return (start_row, start_col, true_positions, true_movements, true_observations)
            
                

        

    def export_to_dir(self, filedir, mapnumber):
        mapname = f"{filedir}/map{mapnumber}"
        with open(mapname, "w") as f:
            for arr in self.obstacle_grid:
                print(arr, file=f)
        for i in range(1, 11):
            truthfilename = f"{mapname}truth{i}"
            start_row, start_col, true_positions, true_movements, true_observations = self.generate_truths()
            with open(truthfilename, "w") as f:
                print(f"{start_row}, {start_col}", file=f)
                print(true_positions, file=f)
                print(true_movements, file=f)
                print(true_observations, file=f)

                    

    def move_up(self): # Updates curr cords to move up one.
        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]
        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):
                
                if(row - 1 < 0 or self.obstacle_grid[row - 1][col] == "B"):
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row - 1][col] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        self.probability_field = self.normalize(new_prob_field)
  

    def move_down(self): # Updates curr cords to move down one.
        
        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):
                
                if(row + 1 >= len(self.probability_field) or self.obstacle_grid[row + 1][col] == "B"):
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row + 1][col] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]


        self.probability_field = self.normalize(new_prob_field)

    def move_left(self): # Updates curr cords to move left one.

        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):
                
                if(col - 1 < 0 or self.obstacle_grid[row][col - 1] == "B"):
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row][col - 1] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        

        self.probability_field = self.normalize(new_prob_field)

    def move_right(self): # Updates curr cords to move right one.

        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):
                
                if(col + 1 >= len(self.probability_field[row]) or self.obstacle_grid[row][col + 1] == "B"):
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row][col + 1] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]


        self.probability_field = self.normalize(new_prob_field)


    def normalize(self, new_prob_field):
        total = 0
        for arr in new_prob_field:
            total += sum(arr)

        alpha = 1 / total
        for row in range(len(new_prob_field)):
            for col in range(len(new_prob_field[row])):
                new_prob_field[row][col] *= alpha
        return new_prob_field

    def print_probabilities(self):
        for arr in self.probability_field:
            print(["{0:.4f}".format(a) for a in arr])
        print()
        
    def print_obstacles(self):
        for arr in self.obstacle_grid:
            print(arr)
        print()