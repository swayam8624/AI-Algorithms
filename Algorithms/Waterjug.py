def gcd(a, b):
    if b == 0:
        return a
    else:
        return gcd(b, a % b)


def minsteps(maxm, maxn, d):
    currm = maxm
    currn = 0
    steps = 1
    print(currn, currm ,steps)
    while currm != d or currn != d:
        temp = min(currm, maxn - currn)
        currn = currn + temp
        currm = currm - temp

        steps += 1
        print(currn, currm, steps)
        if currn == d or currm == d or currm + currn == d:
            print(currn , currm , steps)
            break
        elif currm == 0:
            currm = maxm
            steps += 1
        elif currn == maxn:
            currn = 0
            steps += 1
        else:
            continue
    return steps


def waterjug(m, n, d):
    if m > n:
        m = m + n
        n = m - n
        m = m - n
    if d % gcd(m, n) != 0:
        return -1
    else:
        steps = minsteps(m, n, d)
    return steps


m = eval(input("enter smaller capacity \n"))
n = eval(input("enter bigger capacity \n"))
d = eval(input("enter the finding \n"))
steps = waterjug(m, n, d)
if steps == -1:
    print("not possible")
else:
    print("no of steps required was : ", steps)
