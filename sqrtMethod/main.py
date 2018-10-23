import math
import copy
determinant = 1

def eliminate_first_non_zero(row1, row2):
    first = 0
    while(row1[first] == 0):
        first += 1
    row2First = row2[first]
    for i in range(first, len(row1)):
        row2[i] = row2[i] - row1[i] * row2First / row1[first]

def elimination(mat):
    for iteration in range(len(mat) - 1):
        for step in range(iteration + 1, len(mat)):
            eliminate_first_non_zero(mat[iteration], mat[step])

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

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

def findS(A):
    S = [[0] * len(A) for i in range(len(A))]

    for i in range(len(A)):
        tmpSum = 0
        for k in range(i):
            tmpSum += math.pow(S[k][i], 2)
        S[i][i] = math.sqrt(abs(A[i][i] - tmpSum))
        global determinant
        determinant *= S[i][i]
        for j in range(i, len(A)):
            tmpSum = 0
            for k in range(i):
                tmpSum += S[k][i]*S[k][j]
            S[i][j] = (A[i][j] - tmpSum)/(S[i][i])
    return S


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
    return ans


def sqrtMethod(A, b):
    S = findS(A)
    Scopy = copy.deepcopy(S)
    Scopy = transpose(Scopy)
    for i in range(len(Scopy)):
        Scopy[i].append(b[i])
    elimination(Scopy)
    y = [0] * len(Scopy)
    for i in range(len(Scopy)):
        y[i] = Scopy[i][4] / Scopy[i][i]
    for i in range(len(S)):
        S[i].append(y[i])
    x = back_substitution(S)
    return x


def reversMat(A):
    A = matMultiplikation(A, transpose(A))
    Acopy = copy.deepcopy(A)
    identityMat = [[0] * len(A) for i in range(len(mat))]
    for i in range(len(A)):
        identityMat[i][i] = 1
    reversedMatr = []
    for row in identityMat:
        tmp = sqrtMethod(A, row)
        reversedMatr.append(tmp)
        A = copy.deepcopy(Acopy)
    reversedMatr = transpose(reversedMatr)
    return reversedMatr

f = open("matr.txt", 'r')
mat = []
for line in f:
    mat.append(list(map(float, line.split())))

A = list(map(lambda row: row[:][:-1], mat))
b = list(map(lambda row: row[:][-1], mat))
Acopy = copy.deepcopy(A)
print("initial extended matrix: ")
print_mat(mat)
A = matMultiplikation(A, transpose(A))
x = sqrtMethod(A, b)
solution = []
for i in range(len(x)):
    mas = []
    mas.append(x[i])
    solution.append(mas)
print("solution: ")
print_mat(solution)
print("determinant: ")
print(determinant)
print("\nResidual vector: A*x - b")
tmp = matMultiplikation(A, solution)
Residual = []
for i in range(len(solution)):
    Residual.append(tmp[i][0] -b[i])
print(Residual)
reversedMat = reversMat(Acopy)
print("\nreversed matrix: ")
print_mat(reversedMat)
print("(A^-1)*A : ")
print_mat(matMultiplikation(A, reversedMat))

