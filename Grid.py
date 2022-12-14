import math
import os
import random
import ast


class Grid:
    def __init__(self, row_num=-1, col_num=-1, mapname=None):
        if mapname is not None:
            self.obstacle_grid = []
            with open(mapname, "r") as f:
                for line in f:
                    self.obstacle_grid.append(ast.literal_eval(line))
        elif (row_num == -1 and col_num != -1) or (row_num != -1 and col_num == -1):
            raise Exception("either no row/col arguments or both row/col arguments")
        elif row_num == -1 and col_num == -1:
            preset = ["H", "H", "T", "N", "N", "N", "N", "B", "H"]
            n = 3
            self.obstacle_grid = [[" "] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    self.obstacle_grid[i][j] = preset[(n * i) + j]
        else:
            self.obstacle_grid = [[" "] * col_num for _ in range(row_num)]

            for i in range(row_num):
                for j in range(col_num):

                    rand_val = random.random()
                    if rand_val < .10:  # Blocked cell
                        self.obstacle_grid[i][j] = "B"
                    elif rand_val < .40:  # Hard to traverse cell
                        self.obstacle_grid[i][j] = "T"
                    elif rand_val < .70:  # Highway cell
                        self.obstacle_grid[i][j] = "H"
                    else:  # Normal cell
                        self.obstacle_grid[i][j] = "N"

        bs = 0
        for arr in self.obstacle_grid:
            for ele in arr:
                if ele == "B":
                    bs += 1

        unblocked = len(self.obstacle_grid) * len(self.obstacle_grid[0]) - bs
        distributed_prob = 1.0 / unblocked
        probability_field = [[0.0] * len(self.obstacle_grid[0]) for _ in range(len(self.obstacle_grid))]
        for row in range(len(probability_field)):
            for col in range(len(probability_field[row])):
                if self.obstacle_grid[row][col] == "B":
                    probability_field[row][col] = 0
                else:
                    probability_field[row][col] = distributed_prob

        self.obstacle_grid = self.obstacle_grid
        self.probability_field = probability_field

    def averageErrorFromTruth(self, truthname) -> list[float]:
        errDist = []
        with open(truthname, "r") as f:
            _ = ast.literal_eval(next(f))
            real_position_list = ast.literal_eval(next(f))
            moves_list = ast.literal_eval(next(f))
            observations_list = ast.literal_eval(next(f))
            i = 1
            for move, observation, real_pos in zip(moves_list, observations_list, real_position_list):
                if move == "U":
                    self.move_up()
                elif move == "D":
                    self.move_down()
                elif move == "L":
                    self.move_left()
                elif move == "R":
                    self.move_right()
                self.observe(observation)
                if i > 5:
                    val, cX, cY = self.mostProbable()
                    rpX, rpY = real_pos
                    errDist.append(math.sqrt((cX - rpX) ** 2 + (cY - rpY) ** 2))
                i += 1
        return errDist

    def run_from_truth_file(self, truthname):
        with open(truthname, "r") as f:
            real_moves_list = ast.literal_eval(next(f))
            real_position_list = ast.literal_eval(next(f))
            moves_list = ast.literal_eval(next(f))
            observations_list = ast.literal_eval(next(f))
            for move, observation in zip(moves_list, observations_list):
                if move == "U":
                    self.move_up()
                elif move == "D":
                    self.move_down()
                elif move == "L":
                    self.move_left()
                elif move == "R":
                    self.move_right()
                self.observe(observation)

    def step(self, inputs, visualization):
        realPosition, move, observation = inputs
        rpRow, rpCol = realPosition
        # Filter.do_filter(self.obstacle_grid, self.probability_field, move, observation)
        if move == "U":
            self.move_up()
        elif move == "D":
            self.move_down()
        elif move == "L":
            self.move_left()
        elif move == "R":
            self.move_right()
        else:
            print("ERROR")
        self.observe(observation)
        visualization.setRealPos(rpRow, rpCol)

    def stepOnce(self, inputs, visualization):
        self.step(inputs, visualization)

    def run_default_comms_and_obs(self):
        self.move_right()
        self.observe("N")
        self.print_probabilities()
        print("====")

        self.move_right()
        self.observe("N")
        self.print_probabilities()
        print("====")

        self.move_down()
        self.observe("H")
        self.print_probabilities()
        print("====")

        self.move_down()
        self.observe("H")
        self.print_probabilities()

    def observe(self, letter):
        for row in range(len(self.obstacle_grid)):
            for col in range(len(self.obstacle_grid[row])):
                if self.obstacle_grid[row][col] == letter:
                    self.probability_field[row][col] *= 0.9
                else:
                    self.probability_field[row][col] *= 0.05
        self.probability_field = self.normalize(self.probability_field)

    def generate_truths(self):
        start_row = random.randint(0, len(self.obstacle_grid) - 1)
        start_col = random.randint(0, len(self.obstacle_grid[0]) - 1)
        while self.obstacle_grid[start_row][start_col] == "B":
            start_row = random.randint(0, len(self.obstacle_grid) - 1)
            start_col = random.randint(0, len(self.obstacle_grid[0]) - 1)

        curr_position = [start_row, start_col]
        true_positions = []
        true_movements = []
        true_observations = []

        for i in range(100):
            vec = random.choice([[1, 0], [0, 1], [-1, 0], [0, -1]])  # Wouldn't this do the same as the function?
            # vec = self.generate_vector()
            possible = [0, 0]
            possible[0] = curr_position[0] + vec[0]
            possible[1] = curr_position[1] + vec[1]

            while (possible[0] < 0 or possible[0] >= len(self.obstacle_grid) or possible[1] < 0 or possible[1] >= len(
                    self.obstacle_grid[0]) or self.obstacle_grid[possible[0]][possible[1]] == "B"):
                vec = random.choice([[1, 0], [0, 1], [-1, 0], [0, -1]])
                possible = [0, 0]
                possible[0] = curr_position[0] + vec[0]
                possible[1] = curr_position[1] + vec[1]

            if random.random() < 0.9:  # 90% chance we move
                curr_position = possible

            true_positions.append((curr_position[0], curr_position[1]))

            if vec[0] == -1:
                true_movements.append("U")
            elif vec[0] == 1:
                true_movements.append("D")
            elif vec[1] == 1:
                true_movements.append("R")
            elif vec[1] == -1:
                true_movements.append("L")

            realTerrain = self.obstacle_grid[curr_position[0]][curr_position[1]]
            true_observations.append(self.randomTerrainObservation(realTerrain))

        return start_row, start_col, true_positions, true_movements, true_observations

    def mostProbable(self) -> tuple[float, int, int]:
        top = (0, -1, -1)
        for i in range(len(self.probability_field)):
            for j in range(len(self.probability_field[i])):
                if self.probability_field[i][j] > top[0]:
                    top = (self.probability_field[i][j], i, j)
        return top

    def randomTerrainObservation(self, realTerrain):  # 90% chance we observe the correct terrain type
        if random.random() < 0.9:
            return realTerrain
        else:
            return random.choice([i for i in ['H', 'N', 'T'] if i != realTerrain])

    # static function
    def export_10_maps(self):
        for i in range(1, 11):
            curr_map = f"maps/map{i}"
            if not os.path.exists(curr_map):
                os.makedirs(curr_map)
            g = Grid(row_num=100, col_num=50)
            g.export_to_dir(curr_map, i)

    def export_to_dir(self, filedir, mapnumber):
        mapname = f"{filedir}/map{mapnumber}"
        with open(mapname + ".txt", "w") as f:
            for arr in self.obstacle_grid:
                print(arr, file=f)
        for i in range(1, 11):
            truthfilename = f"{mapname}truth{i}.txt"
            start_row, start_col, true_positions, true_movements, true_observations = self.generate_truths()
            with open(truthfilename, "w") as f:
                print(f"{start_row}, {start_col}", file=f)
                print(true_positions, file=f)
                print(true_movements, file=f)
                print(true_observations, file=f)

    def move_up(self):  # Updates curr cords to move up one.
        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]
        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):

                if row - 1 < 0 or self.obstacle_grid[row - 1][col] == "B":
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row - 1][col] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        self.probability_field = new_prob_field
        # self.probability_field = self.normalize(new_prob_field)

    def move_down(self):  # Updates curr cords to move down one.

        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):

                if row + 1 >= len(self.probability_field) or self.obstacle_grid[row + 1][col] == "B":
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row + 1][col] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        self.probability_field = new_prob_field
        # self.probability_field = self.normalize(new_prob_field)

    def move_left(self):  # Updates curr cords to move left one.

        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):

                if col - 1 < 0 or self.obstacle_grid[row][col - 1] == "B":
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row][col - 1] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        self.probability_field = new_prob_field
        # self.probability_field = self.normalize(new_prob_field)

    def move_right(self):  # Updates curr cords to move right one.

        new_prob_field = [[0] * len(self.probability_field[0]) for _ in range(len(self.probability_field))]

        for row in range(len(self.probability_field)):
            for col in range(len(self.probability_field[row])):

                if col + 1 >= len(self.probability_field[row]) or self.obstacle_grid[row][col + 1] == "B":
                    new_prob_field[row][col] += self.probability_field[row][col]
                    continue
                new_prob_field[row][col + 1] += 0.9 * self.probability_field[row][col]
                new_prob_field[row][col] += 0.1 * self.probability_field[row][col]

        self.probability_field = new_prob_field
        # self.probability_field = self.normalize(new_prob_field)

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
