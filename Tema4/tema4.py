import sys
import numpy as np
from scipy import linalg
import copy

eps = 10 ** -5

kmax = 10000


class Matrix:
    dimension = 0
    data = []
    b = []
    omega = dict()

    def __init__(self, path):
        with open(path) as fp:
            line = fp.readline()
            self.dimension = int(line)

            self.data = [[] for i in range(self.dimension)]
            self.b = []

            while line:
                line = fp.readline()
                if len(line) == 0:
                    continue

                values = line.strip('\n').split(', ')
                if len(values) == 3:
                    value, lin, col = float(values[0]), int(values[1]), int(values[2])
                    flag = False

                    pairNo = -1
                    for pair in self.data[lin]:
                        pairNo += 1
                        if pair[1] == col:
                            self.data[lin][pairNo][0] += value
                            flag = True

                    if not flag:
                        self.data[lin].append([value, col])

                elif len(values) == 1:
                    if values[0] != '':
                        self.b.append(float(values[0]))

                else:
                    print("Caz netratat: *" + line + '*')

        for line in self.data:
            line.sort(key=lambda elem: elem[1])

    def compareMatrix(self, mat, matDimension):
        if self.dimension != matDimension:
            return False

        for lineNo in range(self.dimension):
            myLineElemNo = len(self.data[lineNo])
            otherLineElemNo = len(mat[lineNo])

            if (myLineElemNo != otherLineElemNo):
                return False

            for pairSelf in self.data[lineNo]:
                exists = False

                for pairOther in mat[lineNo]:
                    if abs(pairSelf[0] - pairOther[0]) < eps and pairSelf[1] == pairOther[1]:
                        exists = True
                        break

                if not exists:
                    return False

        return True

    def compareVector(self, vector):
        if self.dimension != len(vector):
            return False

        for index in range(self.dimension):
            if abs(self.b[index] - vector[index]) >= eps:
                return False

        return True

    def printMatrix(self):
        for line in self.data:
            print(line)

    def matrixVectorMultiply(self, x):
        result = []
        # x = [self.dimension - i for i in range(0, self.dimension)]
        for line in self.data:
            sum = 0
            for pair in line:
                sum += pair[0] * x[pair[1]]

            result.append(sum)

        return result

    def getTranspose(self):
        result = [[] for i in range(self.dimension)]

        for lineIndex in range(self.dimension):
            for pair in self.data[lineIndex]:
                val, colIndex = pair[0], pair[1]
                result[colIndex].append([val, lineIndex])

        for line in result:
            line.sort(key=lambda elem: elem[1])
        return result

    def checkMainDiag(self):
        for lineNo in range(self.dimension):
            flag = False
            sum = 0
            mainDiagElementVal = 0

            if len(self.data[lineNo]) == 0:
                return False

            for pair in self.data[lineNo]:
                if pair[1] > lineNo and not flag:
                    return False

                if pair[1] == lineNo:
                    if abs(pair[0]) <= eps:
                        return False

                    else:
                        mainDiagElementVal = pair[0]
                        flag = True
                else:
                    sum += pair[0]

            if mainDiagElementVal <= sum:
                return False

            if not flag:
                return False

        return True

    def getXBySOR(self, omegaValue):
        xc = [0 for i in range(self.dimension)]

        k = 0

        while True:
            xp = copy.copy(xc)
            x = [0 for i in range(self.dimension)]

            for lineIndex in range(self.dimension):

                sum = self.b[lineIndex]

                mainDiagElementVal = 0
                for pair in self.data[lineIndex]:

                    if pair[1] < lineIndex:
                        sum -= pair[0] * xc[pair[1]]
                    elif pair[1] > lineIndex:
                        sum -= pair[0] * xp[pair[1]]
                    else:
                        mainDiagElementVal = pair[0]

                xc[lineIndex] = (sum * (omegaValue / mainDiagElementVal)) + (xp[lineIndex] * (1 - omegaValue))
                x[lineIndex] = xc[lineIndex] - xp[lineIndex]

            deltaX = np.linalg.norm(x, np.inf)

            k += 1

            if deltaX < eps or k > kmax or deltaX > (10 ** 8):
                break

        if deltaX < eps:
            self.omega[omegaValue] = copy.copy(xc)
        else:
            print("Divergent")
            print(deltaX)

        return k

    def computeNorm(self):
        for key in self.omega.keys():
            AxSOR = self.matrixVectorMultiply(self.omega[key])
            rez = np.subtract(np.array(AxSOR), np.array(self.b))
            print("omega: " + str(key) + " norm: " + str(np.linalg.norm(rez)))


m1 = Matrix(sys.argv[1])
m2 = Matrix(sys.argv[2])
m3 = Matrix(sys.argv[3])
m4 = Matrix(sys.argv[4])
m5 = Matrix(sys.argv[5])
# test = Matrix(sys.argv[6])

print("Check Main Diag: ", m1.checkMainDiag(), m2.checkMainDiag(), m3.checkMainDiag(), m4.checkMainDiag(),
      m5.checkMainDiag())
# print(m1.getXBySOR(0.8))
# print(m1.getXBySOR(1.0))
print("m1")
print(m1.getXBySOR(1.2))
print(m1.getXBySOR(1.0))
print(m1.getXBySOR(0.8))
m1.computeNorm()

print("m2")
print(m2.getXBySOR(1.2))
print(m2.getXBySOR(1.0))
print(m2.getXBySOR(0.8))
m2.computeNorm()

print("m3")
print(m3.getXBySOR(1.2))
print(m3.getXBySOR(1.0))
print(m3.getXBySOR(0.8))
m3.computeNorm()

print("m4")
print(m4.getXBySOR(1.2))
print(m4.getXBySOR(1.0))
print(m4.getXBySOR(0.8))
m4.computeNorm()

# print(test.getXBySOR(1.0))
# print(test.omega)

# print(test.matrixVectorMultiply(test.omega[1.0]))
# print(m5.omega)
