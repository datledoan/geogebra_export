import numpy as np
import matplotlib.pyplot as plt

def reflect_over_line(points, m, c):
    reflected_points = []
    for x, y in points:
        x_reflected = (x + (y - c) * m) / (1 + m**2)
        y_reflected = m * x_reflected + c
        reflected_points.append((x_reflected, y_reflected))
    return reflected_points

# Định nghĩa phương trình đường thẳng: y = mx + c
m = 0.5  # Hệ số góc
c = 2    # Hệ số giao điểm với trục y

# Tạo một dãy điểm
original_points = np.array([(1, 2), (2, 3), (3, 4), (4, 5)])

# Lấy đối xứng các điểm qua đường thẳng
reflected_points = reflect_over_line(original_points, m, c)

# Vẽ đồ thị
original_points = np.array(original_points).T
reflected_points = np.array(reflected_points).T

plt.scatter(original_points[0], original_points[1], label='Original Points')
plt.scatter(reflected_points[0], reflected_points[1], label='Reflected Points')

# Vẽ đường thẳng
x_values = np.linspace(min(original_points[0]), max(original_points[0]), 100)
y_values = m * x_values + c
plt.plot(x_values, y_values, label='Line: y = {}x + {}'.format(m, c), linestyle='--')

plt.title('Đối xứng qua đường thẳng')
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.legend()
plt.grid(True)
plt.show()
