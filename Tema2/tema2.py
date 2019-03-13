import sys
import math
import numpy as np
from numpy.linalg import inv

n = int(input("Chose n value:"))
t = int(input("Chose t value:"))
eps = 10 ** -t

A = []
U = []
L = []


def LU():
    for p in range(0, n):
        for j in range(p, n):
            sum = 0.0
            for i in range(0, p):
                sum = sum + L[j][i] * U[i][p]
            L[j][p] = A[j][p] - sum

        if abs(L[p][p] < eps):
            sys.exit("Error: Divide by 0")
        else:
            for j in range(p + 1, n):
                sum = 0.0
                for i in range(0, p):
                    sum = sum + L[p][i] * U[i][j]
                U[p][j] = L[p][p] ** -1 * (A[p][j] - sum)


def norma2(vector):
    rez = 0
    for i in range(0, len(vector)):
        rez = rez + vector[i] ** 2
    return math.sqrt(rez)


b = [1.0, 2.0, 3.0]


def copyMatrix(matrix):
    copy = []
    for line in matrix:
        lineCpy = []
        for element in line:
            lineCpy.append(element)
        copy.append(lineCpy)

    return copy


A = [[1.5, 3, 3], [2, 6.5, 14], [1, 3, 8]]
Ainit = copyMatrix(A)

for i in range(0, n):
    columnU = []
    columnL = []
    for j in range(0, n):
        columnL.append(0 / 1.0)
        if i == j:
            columnU.append(1 / 1.0)
        else:
            columnU.append(0 / 1.0)
    U.append(columnU)
    L.append(columnL)
# Ex1
print("Exercitiul 1:")
LU()

for i in range(0, len(L)):
    for j in range(0, i + 1):
        A[i][j] = L[i][j]
for i in range(0, len(U)):
    for j in range(i + 1, len(U)):
        A[i][j] = U[i][j]
for i in A:
    print(i)
print("Exercitiul 2:")
detA = 1
for i in range(0, n):
    detA *= L[i][i]
print("Determinatul matricii A - ", detA)

print("Exercitiul 3:")
y = [0] * n
x = [0] * n
y[0] = b[0] / A[0][0]
for i in range(1, n):
    sum = 0
    for j in range(0, i):
        sum += A[i][j] * y[j]
    y[i] = (b[i] - sum) / A[i][i]
x[n - 1] = y[n - 1]
for i in range(n - 1, -1, -1):
    sum = 0
    for j in range(i + 1, n):
        sum += A[i][j] * x[j]
    x[i] = y[i] - sum
print("X -", x)
print("Exercitiul 4 ")
AX = [0 for _ in range(n)]

for i in range(0, n):
    suma = 0
    for j in range(0, n):
        suma = suma + Ainit[i][j] * x[j]
    AX[i] = suma - b[i]

normValue = norma2(AX)
print("Norma este: ", normValue)

print("Exercitiul 5")

Xlib = np.linalg.solve(np.array(Ainit), np.array(b))
Arev = inv(np.array(Ainit))
ArevBinit = np.matmul(Arev, b)

rez1 = []
rez2 = []

for i in range(0, n):
    rez1.append(x[i] - Xlib[i])
    rez2.append(x[i] - ArevBinit[i])

print("||xLU−xlib||2 = ", norma2(rez1))
print("||xLU−A−1libBinit||2", norma2(rez2))
