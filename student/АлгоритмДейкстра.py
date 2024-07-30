import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import math

# Пример таблицы смежности графа



adjacency_matrix = np.array([
[0,10,0,3,0,0,0,21,0,0],#0
[0,0,0,0,0,0,0,8,0,43],#1
[0,0,0,0,0,0,0,0,0,3],#2
[0,0,0,0,14,0,0,7,0,0],#3
[0,0,0,0,0,0,0,0,0,0],#4
[0,0,0,0,6,0,2,0,0,0],#5
[0,0,17,0,0,0,0,0,0,0],#6
[0,0,0,0,0,18,0,0,0,33],#7
[0,0,0,0,0,5,0,0,0,0],#8
[0,0,0,0,0,0,0,0,26,0],#9
])

# Создание графа из таблицы смежности
G = nx.from_numpy_array(adjacency_matrix)

# Расположение узлов на графе
pos = nx.circular_layout(G)

# Рисование графа
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_color='black', edge_color='gray')



def get_link_v(v,D):
    for i,weight in enumerate(D[v]):
        if weight>0:
            yield i



def arg_min(T,S):
    amin=-1
    m=max(T)
    for i,t in enumerate(T):
        if t<m and i not in S:
            m=t
            amin=i
    return amin


D=(
(0,3,0,4,0,0,0,0), #x1
(3,0,2,0,0,1,0,0), #x2
(0,2,0,2,0,0,4,4), #x3
(4,0,2,0,0,3,5,0),#x4
(0,0,0,0,0,7,0,7), #x5
(0,1,0,3,7,0,3,0), #x6
(0,0,4,5,0,3,0,7), #x7
(0,0,4,0,0,7,7,0)) #x8
N=len(D)
T=[math.inf]*N
v=0
S={v}
T[v]=0
while v != -1:
    for j in get_link_v(v,D):
        if j not in S:
            w=T[v]+D[v][j]
            if w<T[j]:
                T[j]= w
    v=arg_min(T,S)
    if v>0:
        S.add(v)

print(T)

# Отображение графа
plt.show()





