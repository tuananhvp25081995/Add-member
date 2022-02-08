arr1 = [1,2,3,4,5,6,7,8]
arr2 = [1,1,2,3,4,6,5,8]

for ar1 in arr1:
    for ar2 in arr2:
        if ar1 == ar2:
            print(ar2)
            break
    continue