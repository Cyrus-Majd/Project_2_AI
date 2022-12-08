from Grid import Grid



if __name__ == "__main__":
    preset = ["H", "H", "T", "N", "N", "N", "N", "B", "H"]
    n = 3
    mat = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            mat[i][j] = preset[(n * i) + j]

    for arr in mat:
        print(arr)
    print()

    grid = Grid(mat)
    grid.print_probabilities()
    grid.move_down()
    grid.print_probabilities()
    grid.observe("N")
    grid.print_probabilities()