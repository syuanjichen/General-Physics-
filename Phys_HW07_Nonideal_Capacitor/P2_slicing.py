from numpy import *
List = ["A", "B"]
print(List[0:-1])
print(List[1:-1])
print(List[1:-1:2])
print(List[:-2])
print(List[2:])
print(0.004/1E-4/2.0)

A = zeros([3,3])
B = array(A)
print(A)
A[2, 0:-1] = 1
for i in range(3):
    for j in range(3):
        print(A[i, j])