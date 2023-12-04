import numpy as np
import matplotlib.pyplot as plt

def clothoid(t, a):
    """Hàm tính toán vị trí (x, y) trên đường clothoid với tham số a."""
    x = a * t**2 * np.cos(np.pi * t**2 / 2)
    y = a * t**2 * np.sin(np.pi * t**2 / 2)
    return x, y

def connect_curves(a, b, num_points=100):
    """Nối hai đoạn đường clothoid có tham số lần lượt là a và b."""
    t_a = np.linspace(0, 1, num_points)
    t_b = np.linspace(0, 1, num_points)
    
    x_a, y_a = clothoid(t_a, a)
    x_b, y_b = clothoid(t_b, b)
    
    # Điều chỉnh vị trí của đoạn thứ hai để nối chúng mượt mà
    x_b += x_a[-1] - x_b[0]
    y_b += y_a[-1] - y_b[0]
    
    plt.plot(x_a, y_a, label=f'Clothoid A (a={a:.2f})')
    plt.plot(x_b, y_b, label=f'Clothoid B (b={b:.2f})')
    plt.legend()

# Tham số của đường clothoid cho hai đoạn đường
a = 0.2
b = 0.5

# Vẽ đường clothoid nối giữa hai đoạn đường vuông góc
connect_curves(a, b)

# Hiển thị đồ thị
plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Connecting Clothoids')
plt.grid(True)
plt.show()
