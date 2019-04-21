import sys
import numpy as np
from scipy import linalg
import copy

eps = 10 ** -9

kmax = 10000


class MatrixFromFile:
    dimension = 0
    data = []
    b = []
    v = []
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
        
        testV = np.random.uniform(1.0,5.0,self.dimension)
        vNorm = np.linalg.norm(testV,2)
        self.v = ([element/vNorm for element in testV])
        
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


    def powerMethod(self):
        lambdaVector = []
        w = self.matrixVectorMultiply(self.v)
        lambdaVector = np.dot(w,self.v)
        
        k = 0
        
        while True:
            wNorm = np.linalg.norm(w)
            self.v = [element/wNorm for element in w]
     
            w = self.matrixVectorMultiply(self.v)
            lambdaVector = np.dot(w,self.v)
            
            k += 1
            testValueVector = []
            for index in range(0,len(self.v)):
                testValueVector.append(w[index] - lambdaVector * self.v[index])
            if np.linalg.norm(testValueVector) <= self.dimension * eps  or k > 10000:
                break
    
        if k > 10000:
            print("Algoritmul nu a reusit sa calculeze valoarea proprie")
        else:
            print("O aproximare a unei valori proprii de modul maxim a matricei din fisier este " + str(lambdaVector))
         

class MatrixRandom:
    dimension = 0
    data = []
    v = []
 
    def __init__(self, dimension):
        self.dimension = dimension 
        
        self.data = [[] for i in range(self.dimension)]
        randnums= np.random.randint(1, 100, self.dimension)

        for randint in randnums:
            line = np.random.randint(0 , self.dimension)
            column = np.random.randint(0, self.dimension)
            index = self.getElementPosition(line,column)
          
            if  index == -1:
                self.data[line].append([randint,column])
                if line!=column:
                    self.data[column].append([randint,line])
            else:
                self.data[line][index][0] += randint
                if line!=column:
                    index = self.getElementPosition(column,line)
                    self.data[column][index][0] += randint
        
        testV = np.random.uniform(1.0,5.0,self.dimension)
        vNorm = np.linalg.norm(testV,2)
        self.v = ([element/vNorm for element in testV])

        for line in self.data:
            line.sort(key=lambda elem: elem[1])
    
    def matrixVectorMultiply(self, x):
        result = []
        # x = [self.dimension - i for i in range(0, self.dimension)]
        for line in self.data:
            sum = 0
            for pair in line:
                sum += pair[0] * x[pair[1]]

            result.append(sum)

        return result

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

    def getElementPosition(self, line, column):
        if len(self.data[line]) == 0:
            return -1
        for index in range(len(self.data[line])):
            if  self.data[line][index][1] == column:
                return index
        return -1        
    
    def printMatrix(self):
        for line in self.data:
            print(line)
    
    def getTranspose(self):
        result = [[] for i in range(self.dimension)]

        for lineIndex in range(self.dimension):
            for pair in self.data[lineIndex]:
                val, colIndex = pair[0], pair[1]
                result[colIndex].append([val, lineIndex])

        for line in result:
            line.sort(key=lambda elem: elem[1])
        return result


    def powerMethod(self):
        lambdaVector = []
        w = self.matrixVectorMultiply(self.v)
        lambdaVector = np.dot(w,self.v)
        
        k = 0
        
        while True:
            wNorm = np.linalg.norm(w)
            self.v = [element/wNorm for element in w]
     
            w = self.matrixVectorMultiply(self.v)
            lambdaVector = np.dot(w,self.v)
            
            k += 1
            testValueVector = []
            for index in range(0,len(self.v)):
                testValueVector.append(w[index] - lambdaVector * self.v[index])
            if np.linalg.norm(testValueVector) <= self.dimension * eps  or k > 10000:
                break
    
        if k > 10000:
            print("Algoritmul nu a reusit sa calculeze valoarea proprie")
        else:
            print("O aproximare a unei valori proprii de modul maxim a matricei generata aleator este " + str(lambdaVector))
            
            


""" fileMat = MatrixFromFile("input\m_rar_sim_2019_500.txt")
randMat = MatrixRandom(500)
if  randMat.compareMatrix(randMat.getTranspose(),randMat.dimension) == True:
    randMat.powerMethod()
else:
    print("Matricea generata aleator nu este simetrica")
if fileMat.compareMatrix(fileMat.getTranspose(),fileMat.dimension) == True:
    fileMat.powerMethod()
else:
    print("Matricea din fisier nu este simetrica")  """
A = np.array([[1,2,3],[2,3,3],[4,2,1],[2,1,3]])
b = np.array([1,2,3,4])
U,S,V = np.linalg.svd(A)
mooreMatrix = np.linalg.pinv(A)

rangMatrix = 0 
singularValues = []
minSingularValue = -1
maxSingularValue = -1 

for element in S:
    if element >= 0: 
        singularValues.append(element)
        rangMatrix += 1
        if element < minSingularValue or minSingularValue == -1:
            minSingularValue = element
        if element > maxSingularValue:
            maxSingularValue = element

print ("Valorile singulare ale matricii A pentru p > n sunt: " +  str(singularValues))
print ("Rangul matricii A comform calculelor noastre este: " + str(rangMatrix))
print ("Rangul matricii A comform numpy este: " + str(np.linalg.matrix_rank(A)))
print ("Numarul de conditionare al matricii A comform calculelor noastre este: " + str(maxSingularValue/ minSingularValue))
print ("Numarul de conditionare al matricii A comform numpy este: " + str(np.linalg.cond(A)))

print ("Pseudoinversa Moore-Penrose a matricei A este: ")

x = mooreMatrix.dot(b)
print("Solutia sistemului Ax = b: " + str(x ))

Ax = A.dot(x)
equationResult = []

for index in range(len(Ax)):
    equationResult.append(b[index] - Ax[index])

print("Norma ecuatiei b − Ax este: " + str(np.linalg.norm(equationResult)))