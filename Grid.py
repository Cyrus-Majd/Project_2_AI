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



    
    def observe(self, letter):
        for row in range(len(self.obstacle_grid)):
            for col in range(len(self.obstacle_grid[row])):
                if(self.obstacle_grid[row][col] == letter):
                    self.probability_field[row][col] *= 0.9
                else:
                    self.probability_field[row][col] *= 0.05

        self.probability_field = self.normalize(self.probability_field)

                    

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