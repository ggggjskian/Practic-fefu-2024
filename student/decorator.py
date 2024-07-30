import math
def decorator (func,dx=0,001):
    def wrapped(x,*args,**kwargs):
        res= func(x+dx,*args,**kwargs)-func(x,*args,**kwargs)
        return res
    return wrapped

@decorator
def tg(x):
    return math.tan(x)
dtg=tg(math.pi/4)
print(math.tan(math.pi/4))
print(dtg)