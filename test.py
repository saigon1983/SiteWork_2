a = [1,2,3,4,3,7,3,2,7,9,5,3,2,5,6,7,8,9]
for i in range(len(a)):
    print(i)
    if a[i] == 4:
        a.remove(a[i])
print(a)