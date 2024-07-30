import matplotlib.pyplot as plt
import math
def lin(x):
    if x>0:
        return math.log(x,math.e)
def func(x):
    return 1/(1-x)


y=[i for i in range(2,100)]
y=list(map(func,y))
# </editor-fold>
x=[i for i in range(2,10)]
x=list(map(lin,x))
print(x)
print(y)
plt.plot(x,y)
plt.show()






