k=7
p=[]

for i in range(k):
    row=[1]*(i+1)
    for j in range(i+1):
        if j != 0 and j != i :
            row[j]=p[i-1][j-1]+p[i-1][j]
    p.append(row)

for r in p:
    print(r)






