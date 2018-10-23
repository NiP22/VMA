def print_mat(mat, extended=True):
    for row in mat:
        if(extended):
            print(*row)
        else:
            print(*row[0:-1])
    print()


def pairwise_multiplication(v1, v2):
    if (len(v1) != len(v2)):
        print("vectors not equal")
        return
    ans = []
    for i in range(len(v1)):
        ans.append(v1[i]*v2[i])
    return ans


def TridiagMethod(mat, f):
    n = len(mat)
    psi = [0]*n
    eta = [0]*n
    a = [0]*n
    b = [0]*n
    c = [0]*n
    for i in range(n):
        if i != n - 1:
            a[i + 1] = -1*mat[i + 1][i]
            b[i] = -1*mat[i][i + 1]
        c[i] = mat[i][i]
    eta[n - 1] = f[n - 1]/c[n - 1]
    psi[n - 1] = a[n - 1]/c[n - 1]
    for i in range(n - 2, -1, -1):
        eta[i] = (f[i] + b[i]*eta[i + 1])/(c[i] - b[i]*psi[i + 1])
        if i != 0:
            psi[i] = a[i]/(c[i] - b[i]*psi[i + 1])
    x = [0]*n
    x[0] = eta[0]
    for i in range(1, n):
        x[i] = psi[i]*x[i-1] + eta[i]

    return psi, eta, x


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


print("initial extended matr: ")
print_mat(mat)
A = list(map(lambda row: row[:][:-1], mat))
Acopy = list(map(lambda row: row[:][:-1], mat))
b = list(map(lambda row: row[:][-1], mat))



Psi, Eta, ans = TridiagMethod(A, b)
solution = []
for i in range(len(ans)):
    mas = []
    mas.append(ans[i])
    solution.append(mas)
print("Solution x: ")
print_mat(solution)
print("Psi: ")
print(*Psi)
print("Eta: ")
print(*Eta)

print("Residual vector: A*x - b")
tmp = matMultiplikation(Acopy, solution)
Residual = []
for i in range(len(solution)):
    Residual.append(tmp[i][0] -b[i])
print(*Residual)
