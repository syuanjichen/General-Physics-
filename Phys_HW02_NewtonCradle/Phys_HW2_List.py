a = [1, 2, 'x', 4, 5]
b = a

print(a)
print(b)
print(a[-1])
print(a[2:4])

a[2] = 'y'
print(a)
print(b)

a[3:5] = {-1, -2}
print(a)
print(b)

a.append(12)
for i in a:
    print(i)