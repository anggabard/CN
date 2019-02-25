import math
import random
import time
import matplotlib.pyplot as plt


def ex1():
    u = 1
    m = 0

    while 1 + u != 1:
        m += 1
        u = 10 ** -m

    return 10 ** -(m - 1)


def ex2():
    preciziaMasina = ex1()
    x = 1.0
    y = preciziaMasina
    z = preciziaMasina

    if (x + y) + z == x + (y + z):
        print("Adunarea este asociativa.")
    else:
        print("Adunarea nu este asociativa.")

    x = 1.5

    if (x * y) * z == x * (y * z):
        print("Inmultirea este asociativa.")
    else:
        print("Inmultirea nu este asociativa.")


c = [None, 1 / (math.factorial(3)), 1 / (math.factorial(5)), 1 / (math.factorial(7)), 1 / (math.factorial(9)),
     1 / (math.factorial(11)), 1 / (math.factorial(13))]

Time = dict()
Time["P1"], Time["P2"], Time["P3"], Time["P4"], Time["P5"], Time["P6"] = 0, 0, 0, 0, 0, 0


def P1(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (c[1] - c[2] * x2))
    Time["P1"] += time.time() - now
    return rez


def P2(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (c[1] - x2 * (c[2] - c[3] * x2)))
    Time["P2"] += time.time() - now
    return rez


def P3(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (c[1] - x2 * (c[2] - x2 * (c[3] - c[4] * x2))))
    Time["P3"] += time.time() - now
    return rez


def P4(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (0.166 - x2 * (0.00833 - x2 * (c[3] - c[4] * x2))))
    Time["P4"] += time.time() - now
    return rez


def P5(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (c[1] - x2 * (c[2] - x2 * (c[3] - x2 * (c[4] - c[5] * x2)))))
    Time["P5"] += time.time() - now
    return rez


def P6(x):
    now = time.time()
    x2 = x ** 2
    rez = x * (1 - x2 * (c[1] - x2 * (c[2] - x2 * (c[3] - x2 * (c[4] - x2 * (c[5] - c[6] * x2))))))
    Time["P6"] += time.time() - now
    return rez


s = dict()
s['1'], s['2'], s['3'], s['4'], s['5'], s['6'] = 0, 0, 0, 0, 0, 0


def eroarea(x, i):
    if i == 1:
        return abs(P1(x) - math.sin(x))
    elif i == 2:
        return abs(P2(x) - math.sin(x))
    elif i == 3:
        return abs(P3(x) - math.sin(x))
    elif i == 4:
        return abs(P4(x) - math.sin(x))
    elif i == 5:
        return abs(P5(x) - math.sin(x))
    else:
        return abs(P6(x) - math.sin(x))


randVals = []


def ex3():
    for i in range(0, 10000):
        rand = random.uniform(0, 5)

        randVals.append(rand)

        for j in range(1, 7):
            s[str(j)] = s[str(j)] + eroarea(rand, j)

    final = sorted(s, key=s.__getitem__)

    for indexP in final:
        print("P" + indexP)

    print()

    timeSorted = sorted(Time, key=Time.__getitem__)

    for indexTime in timeSorted:
        print(indexTime + " : " + str(Time[indexTime]))


def drawGrafic():
    y1, y2, y3, y4, y5, y6, sinUs = [], [], [], [], [], [], []
    randVals.sort()

    for val in randVals:
        y1.append(P1(val))
        y2.append(P2(val))
        y3.append(P3(val))
        y4.append(P4(val))
        y5.append(P5(val))
        y6.append(P6(val))
        sinUs.append(math.sin(val))

    plt.plot(randVals, y1, color='green')
    plt.plot(randVals, y2, color='red')
    plt.plot(randVals, y3, color='blue')
    plt.plot(randVals, y4, color='orange')
    plt.plot(randVals, y5, color='black')
    plt.plot(randVals, y6, color='pink')
    plt.plot(randVals, sinUs)
    plt.show()


print("0 - Exit")
print("n - ex no")

option = input("Chose option: ")
while (0 != int(option)):
    option = int(option)
    if option == 1:
        print(ex1())
    elif option == 2:
        ex2()
    elif option == 3:
        ex3()
        drawGrafic()
    else:
        print("Invalid option")
    print("0 - Exit")
    print("n - ex no")
    option = input("Chose option: ")
