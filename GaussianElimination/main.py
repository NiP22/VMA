import copy


numberOfSwaps = 0
determinant = 1
colSwaps = []

def transpose(mat):
    mat = list(map(list, zip(*mat)))
    return mat

def print_mat(mat, extended=True):
    for row in mat:
        if(extended):
            print(*row)
        else:
            print(*row[0:-1])
    print()

def swap_rows(mat, i, j, InElimination = True):
    if (i == j):
        return
    if(InElimination):
        global numberOfSwaps
        numberOfSwaps += 1
    mat[i], mat[j] = mat[j], mat[i]


def swap_columns(mat, i ,j):
    if (i == j):
        return
    global numberOfSwaps
    numberOfSwaps += 1
    for current in range(len(mat)):
        mat[current][i], mat[current][j] = mat[current][j], mat[current][i]
    global colSwaps
    colSwaps.append([i, j])

def eliminate_first_non_zero(row1, row2):
    first = 0
    while(row1[first] == 0):
        first += 1
    row2First = row2[first]
    for i in range(first, len(row1)):
        row2[i] = row2[i] - row1[i] * row2First / row1[first]

def max_in_mat(mat):
    mx = mat[0][0]
    mxRow = 0
    mxCol = 0
    for i in range(len(mat)):
        iterMax = max(mat[i])
        if (mx < iterMax):
            mx = iterMax
            mxCol = mat[i].index(iterMax)
            mxRow = i
    if(mx == 0):
        print("zero matrix")
        exit(0)
    return mxRow, mxCol

def pick_largest_elem(mat, iterationNumber):
    row, coloumn = max_in_mat(list(map(lambda row: row[iterationNumber:][:-1] ,mat[iterationNumber:]))) #рассматриваю матрицу без iterationNumber строк и столбцов
    swap_rows(mat, iterationNumber, row + iterationNumber)
    swap_columns(mat, iterationNumber, coloumn + iterationNumber)
    return mat

def elimination(mat):
    for iteration in range(len(mat) - 1):
        mat = pick_largest_elem(mat ,iteration)
        global determinant
        determinant *= mat[iteration][iteration]
        for step in range(iteration + 1, len(mat)):
            eliminate_first_non_zero(mat[iteration], mat[step])

def pairwise_multiplication(v1, v2):
    if (len(v1) != len(v2)):
        print("vectors not equal")
        return
    ans = []
    for i in range(len(v1)):
        ans.append(v1[i]*v2[i])
    return ans

def back_substitution(mat):
    ans = [0 for i in range(len(mat))]
    ans[-1] = mat[-1][-1]/mat[-1][-2]
    for numberOfVaraible in range(len(mat) - 2, -1, -1):
        tmp = sum(pairwise_multiplication(mat[numberOfVaraible][:-1], ans))
        ans[numberOfVaraible] = (mat[numberOfVaraible][-1] - tmp)/(mat[numberOfVaraible][numberOfVaraible])
    #перестановки чтобы получить правильный вектор ответов
    global colSwaps
    colSwaps.reverse()
    for each in colSwaps:
        swap_rows(ans, each[1], each[0], False)
    colSwaps = []
    return ans

def gaussian_elim(mat):
    elimination(mat)
    global determinant
    determinant *= mat[-1][-2]
    return back_substitution(mat)

def matMultiplikation(mat1, mat2):
    sum = 0  # сумма
    tmp = []  # временная матрица
    mat3 = []  # конечная матрица

    for z in range(0, len(mat1)):
        for j in range(0, len(mat2[0])):
            for i in range(0, len(mat1[0])):
                sum += mat1[z][i] * mat2[i][j]
            tmp.append(sum)
            sum = 0
        mat3.append(tmp)
        tmp = []
    return mat3


f = open("matr.txt", 'r')
mat = []
for line in f:
    mat.append(list(map(float, line.split())))

A = list(map(lambda row: row[:][:-1], mat))
Acopy = list(map(lambda row: row[:][:-1], mat))
b = list(map(lambda row: row[:][-1], mat))
print("solution: ")
tmp = gaussian_elim(mat)
solution = []
for i in range(len(tmp)):
    mas = []
    mas.append(tmp[i])
    solution.append(mas)

print_mat(solution)
print("determinant of a matrix: ")
print(determinant*pow(-1, numberOfSwaps))
print()

identityMat = [[0] * len(mat) for i in range(len(mat))]
for i in range(len(mat)):
    identityMat[i][i] = 1
reversedMatr = []
for row in identityMat:
    for i in range(len(mat)):
        A[i].append(row[i])
    reversedMatr.append(gaussian_elim(A))
    A = copy.deepcopy(Acopy)

print("reversed matr:")
reversedMatr = transpose(reversedMatr)
print_mat(reversedMatr)


print("A*A-1")
print_mat(matMultiplikation(Acopy, reversedMatr))
print("Residual vector: A*x - b")
tmp = matMultiplikation(Acopy, solution)
Residual = []
for i in range(len(solution)):
    Residual.append(tmp[i][0] -b[i])
print(Residual)
