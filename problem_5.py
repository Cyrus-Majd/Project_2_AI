import argparse
import random
from typing import Tuple
import os

def print_mat(mat : list, probability_field : list, n : int):
    print("=" * (n * 5))
    for i in range(n):
        print(mat[i], "\t", probability_field[i])
    # for each in mat:
    #     print(each)
    # for each in probability_field:
    #     print(each)
    print("=" * n * 5)

def init_field(n : int) -> list:
    arr = [['X'] * n for _ in range(n)]
    return arr

def add_noise(mat : list, n : int) -> list: # Randomly assigns cell types
    for i in range(n):
        for j in range(n):
            rand_val = random.random()
            if (rand_val < .10):    # Blocked cell
                mat[i][j] = "B"
            elif (rand_val < .40):  # Hard to traverse cell
                mat[i][j] = "T"
            elif (rand_val < .70):  # Highway cell
                mat[i][j] = "H"
            else:                   # Normal cell
                mat[i][j] = "N"
    return mat

def example_field(mat : list, n : int) -> list: # Recreate example in assignment PDF
    preset = ["H", "H", "T", "N", "N", "N", "N", "B", "H"]
    for i in range(n):
        for j in range(n):
            mat[i][j] = preset[(n * i) + j]
    return mat

def change_at(mat : list, x : int, y : int, val : int) -> list: # Set a specific cell to a specified cell type.
    x = x - 1   # Sub 1 because assignment does not zero-index coordinates
    y = y - 1
    mat[x][y] = val
    return mat

def count_unblocked(mat : list) -> int: # Return number of unblocked cells
    ctr = 0
    for row in mat:
        for elem in row:
            if elem != "B":
                ctr += 1
    return ctr

def spawn(mat : list) -> list: # Spawn randomly on matrix
    randPos = random.randrange(1, count_unblocked(mat))
    for i in range(len(mat)):
        for j in range(len(mat[i])):
            if mat[i][j] == "B":
                continue
            else:
                if randPos == 0:
                    cords = []
                    cords.append(i + 1)
                    cords.append(j + 1)
                    return cords
                else:
                    randPos -= 1
                
def peek(mat : list, x : int, y : int) -> str: # Peek into a specified cell
    x = x - 1
    y = y - 1
    return mat[x][y]

def make_field(n : int) -> Tuple: # Makes field of size n
    DEBUG = True
    mat = init_field(n)
    if (DEBUG == False):
        mat = add_noise(mat, n)
    else:
        mat = example_field(mat, n)
    currCords = spawn(mat)
    return (mat, currCords)
    # mat = change_at(mat, currCords[0], currCords[1], 'F')
    # mat = change_at(mat, 2, 3, 'F')
    # print_mat(mat, n)

def check_up(mat : list, currCords : list): # Checks if up is a valid move given our position
    if currCords[0] == 1:
        print("Cannot perform action; player is at top of the board.")
        return False
    elif peek(mat, currCords[0] - 1, currCords[1]) == "B":
        print("Cannot peform action; player is beneath blocked cell.")
        return False
    else:
        return True

def check_down(mat : list, currCords : list): # Checks if down is a valid move given our position
    if currCords[0] == len(mat):
        print("Cannot perform action; player is at bottom of the board.")
        return False
    elif peek(mat, currCords[0] + 1, currCords[1]) == "B":
        print("Cannot peform action; player is above blocked cell.")
        return False
    else:
        return True

def check_left(mat : list, currCords : list): # Checks if left is a valid move given our position
    if currCords[1] == 1:
        print("Cannot perform action; player is at left of the board.")
        return False
    elif peek(mat, currCords[0], currCords[1] - 1) == "B":
        print("Cannot peform action; player to the right of a blocked cell.")
        return False
    else:
        return True

def check_right(mat : list, currCords : list): # Checks if right is a valid move given our position
    if currCords[1] == len(mat):
        print("Cannot perform action; player is at right of the board.")
        return False
    elif peek(mat, currCords[0], currCords[1] + 1) == "B":
        print("Cannot peform action; player to the left of a blocked cell.")
        return False
    else:
        return True

def move_up(currCords : list): # Updates curr cords to move up one.
    currCords[0] -= 1
    return currCords

def move_down(currCords : list): # Updates curr cords to move down one.
    currCords[0] += 1
    return currCords

def move_left(currCords : list): # Updates curr cords to move left one.
    currCords[1] -= 1
    return currCords

def move_right(currCords : list): # Updates curr cords to move right one.
    currCords[1] += 1
    return currCords

def play_manually(field : Tuple, probability_field : list):
    mat = field[0]
    currCords = field[1]
    conditional = True
    while(conditional):
        print_mat(mat, probability_field, len(mat))
        print("CURRENT POSITION:", currCords, "VALUE:", peek(mat, currCords[0], currCords[1]))
        cmd = input("Next move [U, D, L, R] (Q to quit): ")
        if cmd == "Q":
            exit()
        elif cmd == "U" and check_up(mat, currCords):
            currCords = move_up(currCords)
        elif cmd == "D" and check_down(mat, currCords):
            currCords = move_down(currCords)
        elif cmd == "L" and check_left(mat, currCords):
            currCords = move_left(currCords)
        elif cmd == "R" and check_right(mat, currCords):
            currCords = move_right(currCords)

def init_probability_field(mat : list, n : int) -> list:
    probability_field = [[0] * n for _ in range(n)]
    num_of_unblocked = float(count_unblocked(mat))
    for i in range(n):
        for j in range(n):
            if (mat[i][j] == "B"):
                probability_field[i][j] = 0.0
            else:
                probability_field[i][j] = 1.0/num_of_unblocked
    return probability_field

def play_preset(field, probability_field, preset):
    command = "R"
    n = len(field[0])
    for i in range(n):
        for j in range(n):
            print(probability_field[i][j])
            if command == "R":
                #if ()
                print("right detected")
            elif command == "L":
                print()
            elif command == "D":
                print()
            elif command == "U":

def main():
    args = parser.parse_args()
    field = make_field(int(args.mat_size[0]))
    probability_field = init_probability_field(field[0], int(args.mat_size[0]))
    print_mat(field[0], probability_field, int(args.mat_size[0]))
    # play_manually(field, probability_field)
    preset = ["R", "R", "D", "D"]
    play_preset(field, probability_field, preset)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Problem 5')
    parser.add_argument('mat_size', metavar='1', type=int, nargs='+',
                    help='size of the matrix')
    main()
