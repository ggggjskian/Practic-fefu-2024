import matplotlib.pyplot as plt
import numpy as np

t = np.linspace(0, 2*np.pi, 500)  # Создаем массив значений t от 0 до 2pi

# Вычисляем значения x и y
x = 4 * np.sqrt(2) * np.cos(t)**3
y = 2 * np.sqrt(2) * np.sin(t)**3

# Строим график
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('График функции x=4√2cos^3(t), y=2√2sin^3(t)')
plt.grid(True)
plt.show()
