import time
def decorator_time(func):
    def wrapped(*args,**kwargs):
        start_time=time.time()
        res=func(*args,**kwargs)
        complete_time=time.time()
        doing_time=complete_time-start_time
        print(f"Время выполнения функции:\n {doing_time}")
        return res
    return wrapped
@decorator_time
def evklid(a,b):
    while a!=b:
        if a>b:
            a-=b
        else:
            b-=a
    return a

print(evklid(2, 100000))
print(2//4)

