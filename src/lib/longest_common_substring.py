
def longest_common_substring(a: str, b: str) -> tuple[str, list[list[int]]]:
    """
    Let's say a = "bananas", and that  b = "ananas" (a word for pineapple in south america.)

    We first build a matrix 'bananas' wide (x), and 'ananas' tall (y).

    # |  b a n a n a s
    ------------------
    a |  0 1 0 0 0 0 0
    n |  0 0 2 0 0 0 0
    a |  0 0 0 3 0 0 0
    n |  0 0 0 0 4 0 0
    a |  0 0 0 0 0 5 0
    s |  0 0 0 0 0 0 6

    As we traverse the matrix, we'll have (x, y) coordinate pairs.

    the x-coordinate will map to a character in `a` (bananas, in our case),
    and the y-coordinate values will map to characters in `b` (ananas.)

    while traversing, we also make note of the maximum column and row values.
    """
    row = [0 for _ in range(len(a))]
    matrix = [row[::] for _ in range(len(b))]

    max_value = 0
    max_value_row = -1
    max_value_col = 0

    # `x` can index into string `a`,
    # since the width is determined by the `a` string.
    for x in range(len(row)):
        # `y` can index into string `b`,
        # since the height, or y-axis is determined by the `b` string.
        for y in range(len(matrix)):
            a_char = a[x]
            b_char = b[y]

            if b_char != a_char:
                continue

            up_left = 0
            if x > 0 and y > 0:
                up_left = matrix[y-1][x-1]

            matrix[y][x] = 1 + up_left
            if matrix[y][x] > max_value:
                max_value = matrix[y][x]
                max_value_row = x
                max_value_col = y
            else:
                matrix[y][x] = 0

    start_index = max_value_row - max_value + 1
    return a[start_index:max_value_row+1], matrix
