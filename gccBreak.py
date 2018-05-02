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

def initUnknownValue(lis):
    unknown = [-1]*93
    mutated = True
    while mutated:
        mutated = False
        for n in range(31, 93):
            mutated = checkUnknownValue(lis, unknown, n, mutated)
    return unknown

def checkUnknownValue(lis, unknown, n, mutated):
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

def fill(lis, index, val):
    if lis[index] == -1:
        lis[index] = val
        return True
    else:
        return False

def initRValue(lis, un):
    r = [-1]*93
    for n in range(93):
        if not (un[n] == -1):
            calcRfromUnknown(lis, un, r, n)
    return r

def calcRfromUnknown(obs, unk, r, n):
    r[n] = (obs[n] * 2 + unk[n]) % 2**32

def calcRFromPrev(r, n):
    if not (r[n-3] == -1 or r[n-31] == -1):
        calc = (r[n-3] + r[n-31]) % 2**32
        r[n] = calc
    if n + 3 < len(r) and not(r[n+3] == -1 or r[n-28] == -1):
        calc = (r[n+3] - r[n-28]) % 2**32
        r[n] = calc
    if n + 31 < len(r) and not(r[n+31] == -1 or r[n+28] == -1):
        calc = (r[n+31] - r[n+28]) % 2**32
        r[n] = calc

def etTuBrute(r, un, inp):
    for n in range(31, 93):
        if r[n] == -1:
            for a in range(2):
                un[n] = a
                if re_validateGuess(r, un, inp, n):
                    break
                else:
                    un[a] = -1

def re_validateGuess(r, unk, obs, a):
    if a < 0 or a+28 > 93:
        return True

    if (r[a] == (r[a-3] + r[a-31]) % 2**32):
        if (not(unk[a] == -1) and (2 * obs[a] + unk[a]) % 2** 32 == r[a]):
            return True
        else:
            return False

    return re_validateGuess(r,unk,obs, a+3) and re_validateGuess(r,unk,obs, a+28)

def finalizeLast32(r, un, inp):
    for n in range(62, 93):
        if r[n] == -1:
            if not(un[n] == -1):
                calcRfromUnknown(inp,un,r,n)

def calcNextNumber(r, i):
    i += 93
    calc =(r[i-3] + r[i-31]) % 2**32
    r.append(calc)
    return calc >> 1

def calcNext93(r):
    output = []
    for n in range(93):
        output.append(calcNextNumber(r,n))
    return output

def your_code(theinput):
    unknown = initUnknownValue(theinput)
    r = initRValue(theinput, unknown)

    for n in range(31,93):
        calcRFromPrev(r,n)

    etTuBrute(r, unknown, theinput)

    finalizeLast32(r, unknown, theinput)
    output = calcNext93(r)

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
