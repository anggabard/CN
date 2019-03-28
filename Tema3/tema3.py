import sys


class Matrix:
    dimension = 0
    data = []
    b = []

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
                    if pairSelf[0] == pairOther[0] and pairSelf[1] == pairOther[1]:
                        exists = True
                        break

                if not exists:
                    return False

        return True

    def compareVector(self, vector):
        if self.dimension != len(vector):
            return False

        for index in range(self.dimension):
            if self.b[index] != vector[index]:
                return False

        return True

    def printMatrix(self):
        for line in self.data:
            print(line)

    def matrixVectorMultiply(self):
        result = []
        x = [self.dimension - i for i in range(0, self.dimension)]
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

def verify12elementsPerLine(mat):
    for line in mat.data:
        if len(line) > 12:
            return False
    return True

def addMatrix(a, b):
    if a.dimension != b.dimension:
        return False

    result = []
    dimension = a.dimension

    for lineNo in range(dimension):
        lineResult = []
        lineResult.extend(a.data[lineNo])
        lineResult.extend(b.data[lineNo])

        strippedLine = []

        for pairIndex1 in range(len(lineResult)):
            exists = False
            newElement = [0, -1]

            for pairIndex2 in range(pairIndex1 + 1, len(lineResult)):
                if lineResult[pairIndex1][1] == lineResult[pairIndex2][1]:
                    newElement[0] = lineResult[pairIndex1][0] + lineResult[pairIndex2][0]
                    newElement[1] = lineResult[pairIndex1][1]

                    lineResult.pop(pairIndex2)

                    exists = True
                    break

            if exists:
                strippedLine.append(newElement)
            else:
                try:
                    strippedLine.append(lineResult[pairIndex1])
                except IndexError:
                    break

        result.append(strippedLine)

    return result

def mulLines(line1, line2):
    if len(line1) == 0:
        return 0

    sum = 0

    for pairF in line1:
        col = pairF[1]

        for pairS in line2:
            if col < pairS[1]:
                break

            if col == pairS[1]:
                sum += (pairF[0] * pairS[0])

    return sum

def mulMatrix(a, b):
    first = a.data
    second = b.getTranspose()

    result = [[] for i in range(a.dimension)]
    for line1Index in range(a.dimension):
        for line2Index in range(b.dimension):
            if first[line1Index] and second[line2Index]:
                sum = mulLines(first[line1Index], second[line2Index])
                if sum != 0:
                    result[line1Index].append([sum, line2Index])

    for line in result:
        line.sort(key=lambda elem: elem[1])

    return result


a = Matrix(sys.argv[1])

b = Matrix(sys.argv[2])

aplusb = Matrix(sys.argv[3])

aorib = Matrix(sys.argv[4])

print("Validate a: " + str(verify12elementsPerLine(a)))
print("Validate b: " + str(verify12elementsPerLine(b)))

aplusbtest = addMatrix(a, b)
aplusbtestDimension = a.dimension

print("Validate a + b: " + str(aplusb.compareMatrix(aplusbtest, aplusbtestDimension)))

Ax = a.matrixVectorMultiply()
Bx = b.matrixVectorMultiply()
aplusbX = aplusb.matrixVectorMultiply()
aoribX = aorib.matrixVectorMultiply()

print("Validate a * x: " + str(a.compareVector(Ax)))
print("Validate b * x: " + str(b.compareVector(Bx)))
print("Validate (a + b) * x: " + str(aplusb.compareVector(aplusbX)))
print("Validate (a * b) * x: " + str(aorib.compareVector(aoribX)))

print("Calculating a * b")
aoribtest = mulMatrix(a, b)
aoribtestD = a.dimension

#aoribtest[23].append([23.5, 14])
#aorib.data[23].append([23.5, 14])
print("Validate a * b: " + str(aorib.compareMatrix(aoribtest, aoribtestD)))

# test1 = Matrix(sys.argv[5])
# test2 = Matrix(sys.argv[6])