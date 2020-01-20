popcount = [[]] * 2 ** 9
for i in range(len(popcount)):
    popcount[i] = [index for index, a in enumerate(format(i, '09b')[::-1],start=1) if a == '0']

def box(i : int, j : int):
    return (i // 3) * 3 + (j // 3)

def available(mask : list, i: int, j : int):
    m = mask[0][i] | mask[1][j] | mask[2][box(i,j)]
    return popcount[m]

def rank(mask : list, i: int, j : int):
    return len(available(mask, i, j))

def setMask(mask, i : int, j: int, value: int):
    bit = 1 << (value - 1)
    k = box(i,j)
    assert(mask[0][i] & bit == 0)
    assert(mask[1][j] & bit == 0)
    assert(mask[2][k] & bit == 0)
    mask[0][i]|=bit
    mask[1][j]|=bit
    mask[2][k]|=bit

def prepare(puzzle):
    mask = [[0 for i in range(9)] for j in range(3)]
    queue = []
    for i in range(9):
        for j in range(9):
            value = puzzle[i][j]
            assert(value>=0 and value<=9)
            if value != 0:
                setMask(mask, i, j, value)
            else:
                queue.append((i,j))
    return (mask, queue)

def process(queue, mask, puzzle):
    if len(queue)==0:
        return [puzzle]
    result = []
    i, j = min(queue,key=lambda p: rank(mask, p[0], p[1]))
    newQueue = queue.copy()
    newQueue.remove((i,j))
    a = available(mask, i, j)
    for value in a:
        newMask = [x[:] for x in mask]
        newPuzzle = [x[:] for x in puzzle]
        newPuzzle[i][j] = value
        setMask(newMask, i, j, value)
        
        result += process(newQueue, newMask, newPuzzle)
        if len(result) > 1:
            return result
    return result

def sudoku_solver(puzzle):
    assert(len(puzzle) == 9)
    assert(all([len(x) == 9 for x in puzzle]))
    mask, queue = prepare(puzzle)
    assert(len(queue) <= 64)
    result = process(queue, mask, puzzle)
    assert(len(result)==1)
    return result[0]

if __name__ == "__main__":
    puzzle = [[0, 0, 6, 0, 0, 7, 0, 9, 0],
        [0, 0, 1, 0, 4, 0, 6, 0, 0],
        [0, 0, 0, 8, 0, 6, 0, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 6, 4, 0, 8, 0, 3, 7, 0],
        [0, 3, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 3, 0, 4, 0, 0, 0],
        [0, 0, 8, 0, 1, 0, 4, 0, 0],
        [0, 1, 0, 5, 0, 0, 2, 0, 0]]
    print(sudoku_solver(puzzle))
