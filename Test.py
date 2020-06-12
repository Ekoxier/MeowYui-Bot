import random

total = 0

for k in range(10):
    count2 = 0;
    for j in range(1000):
        s = ''
        for i in range(80):
            a = random.randint(0, 99)
            if a < 36:
                s = s + '1'
            else:
                s = s + '0'
        count = 0;
        for i in range(50):
            d = {'0': 0, '1': 0}
            for x in s[i:i+4]:
                if x not in d.keys():
                    d[x] = 1
                else:
                    d[x] = d[x] + 1
            if d['1'] > 3:
                count = count + 1
        if count > 0:
            total = total + 1
            count2 = count2 + 1
    print(count2)
print(total)