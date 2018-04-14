import random

def crand(seed):
    r=[]
    r.append(seed)
    for i in range(30):
        r.append((16807*r[-1]) % 2147483647)
        if r[-1] < 0:
            r[-1] += 2147483647
    for i in range(31, 34):
        r.append(r[len(r)-31])
    for i in range(34, 344):
        r.append((r[len(r)-31] + r[len(r)-3]) % 2**32)
    while True:
        next = r[len(r)-31]+r[len(r)-3] % 2**32
        r.append(next)
        yield (next >> 1 if next < 2**32 else (next % 2**32) >> 1)

def initUnknown(lis):
    unknown = [-1]*93
    mutated = True
    while mutated:
        mutated = False
        for n in range(31, 93):
            mutated = checkUnknown(lis, unknown, n, mutated)
    return unknown

def checkUnknown(lis, unknown, n, mutated):
    d = (2*(lis[n] - lis[n-3] - lis[n-31])) % 2**32
    if d == 2:
        a = fill(unknown, n, 0)
        b = fill(unknown, n-3, 1)
        c = fill(unknown, n-31, 1)
        mutated = mutated or a or b or c
    else:
        if unknown[n] == 0:
            a = fill(unknown, n-3, 0)
            b = fill(unknown, n-31, 0)
            mutated = mutated or a or b
        if n - 3 >= 0 and unknown[n-3] == 1:
            a = fill(unknown, n-31, 0)
            b = fill(unknown, n, 1)
            mutated = mutated or a or b
        if n - 31 >= 0 and unknown[n-31] == 1:
            a = fill(unknown, n-3, 0)
            b = fill(unknown, n, 1)
            mutated = mutated or a or b
    return mutated

def reCheckUnknown(lis, r, un):
    for n in range(93):
        if un[n] == -1:
            if not(r[n] == -1):
                un[n] = r[n] - 2 * lis[n]

def initRValue(lis, un):
    r = [-1]*93
    for n in range(31,93):
        if un[n] == -1:
            if not (un[n-3] == -1 or un[n-31] == -1):
                r[n] = (lis[n-3] * 2 + lis[n-31] * 2 + un[n-3] + un[n-31]) % 2 ** 32
        else:
            r[n] = lis[n] * 2 + un[n]
    for n in range(31, 93):
        validate(r, n)
    #print r[92], (r[92-3] + r[92-31]) % 2**32
    for n in range(31, 93):
        validate(r, n)
    return r

def init32r(lis, un, r):
    for n in range(32):
        if not(un[n] == -1):
            r[n] = lis[n]*2 + un[n]

def checkRValue(lis, un, r):
    reCheckUnknown(lis, r, un)
    for n in range(62,93):
        checkUnknown(lis, un, n, mutated=False)
    for n in range(31, 93):
        validate(r, n)

def calcNext(r, i):
    i += 93
    calc =(r[i-3] + r[i-31]) % 2**32
    r.append(calc)
    return calc >> 1

def calc93(r):
    output = []
    for n in range(93):
        output.append(calcNext(r,n))
    return output

def validate(r, n):
    if not (r[n-3] == -1 or r[n-31] == -1):
        calc = (r[n-3] + r[n-31]) % 2**32
        r[n] = calc
    if n + 3 < len(r) and not(r[n+3] == -1 or r[n-28] == -1):
        calc = (r[n+3] - r[n-28]) % 2**32
        r[n] = calc
    if n + 31 < len(r) and not(r[n+31] == -1 or r[n+28] == -1):
        calc = (r[n+31] - r[n+28]) % 2**32
        r[n] = calc

def trueValidate(r, un, inp, a):

    if a < 0 or a+28 > 93:
        return True

    if (r[a] == (r[a-3] + r[a-31]) % 2**32):
        if (not(un[a] == -1) and (2 * inp[a] + un[a]) % 2** 32 == r[a]):
            return True
        else:
            return False

    return trueValidate(r,un,inp, a+3) and trueValidate(r,un,inp, a+28)

def etTuBrute(r, un, inp):
    for n in range(31, 93):
        if r[n] == -1:
            for a in range(2):
                un[n] = a
                if trueValidate(r, un, inp, n):
                    break
                else:
                    un[a] = -1

def fill(lis, index, val):
    if lis[index] == -1:
        lis[index] = val
        return True
    else:
        return False

def rFill(r, un, inp):
    for n in range(62, 93):
        if r[n] == -1:
            if not(un[n] == -1):
                r[n] = (inp[n] * 2 + un[n]) % 2**32

def your_code(theinput):
    unknown = initUnknown(theinput)
    r = initRValue(theinput, unknown)
    init32r(theinput,unknown, r)
    checkRValue(theinput, unknown, r) #there is definitely some redundant code in here

    etTuBrute(r, unknown, theinput)

    rFill(r, unknown, theinput)
    output = calc93(r)

    #for a in range(93):
    #   print a,r[a], theinput[a], unknown[a]


    return output


def testMulti(l):
    c = 0
    for n in range(l):
        theseed = random.randint(1, 2**30)
        skip = random.randint(10000, 200000)

        my_generator = crand(theseed)
        for i in range(skip):
            temp = my_generator.next()

        the_input = [my_generator.next() for i in range(93)]
        the_output = [my_generator.next() for i in range(93)]

        test = your_code(the_input)
        if test == the_output:
            c += 1
    return c, l

results = testMulti(200)
print str(results[0]) + " out of " + str(results[1]) + " trials correct"


