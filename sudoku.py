import heapq

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
    queue = [(rank(mask, i, j), i, j) for i,j in queue]
    heapq.heapify(queue)
    return (mask, queue)

def process(queue, mask, puzzle):
    if len(queue)==0:
        return [puzzle]
    result = []
    newQueue = queue[:]
    _, i, j = heapq.heappop(newQueue)
    a = available(mask, i, j)
    for value in a:
        newMask = [x[:] for x in mask]
        newPuzzle = [x[:] for x in puzzle]
        newPuzzle[i][j] = value
        setMask(newMask, i, j, value)
        newQueue = [(rank(mask, i, j), i, j) for _, i, j in newQueue]
        if len(newQueue)==0:
            return [newPuzzle]
        heapq.heapify(newQueue)
        if newQueue[0][0] > 0:
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
