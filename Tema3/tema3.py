import sys


class Matrix:
    dimension = 0
    data = []
    b = []
    name = ''
    valid = True

    def __init__(self, path, name):
        self.name = name

        with open(path) as fp:
            line = fp.readline()
            self.dimension = int(line)

            self.data = [[] for i in range(self.dimension)]

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
                    self.b.append(values[0])

                else:
                    print("Caz netratat: *" + line + '*')

        for line in self.data:
            if len(line) > 12:
                self.valid = False


a = Matrix(sys.argv[1], 'a')
b = Matrix(sys.argv[2], 'b')
aplusb = Matrix(sys.argv[3], 'aplusb')
aorib = Matrix(sys.argv[4], 'aorib')

print(a.valid, b.valid, aplusb.valid, aorib.valid)
