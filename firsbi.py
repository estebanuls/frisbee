import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.spatial.transform import Rotation as R

# Función para crear el disco como una malla circular (tipo frisbee)
def crear_disco(n_puntos=50, radio=0.5):
    theta = np.linspace(0, 2 * np.pi, n_puntos)
    x = radio * np.cos(theta)
    y = radio * np.sin(theta)
    z = np.zeros_like(x)
    disco = np.stack((x, y, z), axis=-1)
    return disco

# Cargar datos
file_path = "datos_20250630_1710_mpu.csv"
data = pd.read_csv(file_path)

euler_angles = data[['roll', 'pitch', 'yaw']].values
gyro_data = data[['GyX', 'GyY', 'GyZ']].values
times = data['tiempo_ms'].values

# Crear figura 3D
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim([-1.0, 1.0])
ax.set_ylim([-1.0, 1.0])
ax.set_zlim([-0.5, 0.5])
ax.set_box_aspect([1, 1, 0.5])
ax.set_title("Rotación del Frisbee")

# Crear disco
disco = crear_disco()
frisbee_patch = Poly3DCollection([disco], facecolor='skyblue', alpha=0.8)
ax.add_collection3d(frisbee_patch)

# Punto rojo para mostrar rotación
punto_rojo, = ax.plot([], [], [], 'ro', markersize=6)

# Texto para mostrar valores giroscópicos
text_gyro = ax.text2D(0.02, 0.95, '', transform=ax.transAxes, fontsize=10, color='red')

# Función de actualización
def update(frame):
    global frisbee_patch, punto_rojo, text_gyro

    roll, pitch, yaw = np.radians(euler_angles[frame])
    rot = R.from_euler('xyz', [roll, pitch, yaw])

    # Aplicar rotación al disco
    disco_rotado = rot.apply(disco)

    # Actualizar frisbee como superficie
    frisbee_patch.set_verts([disco_rotado])

    # Actualizar punto rojo (usamos el primer punto del borde del disco)
    punto = disco_rotado[0]
    punto_rojo.set_data([punto[0]], [punto[1]])
    punto_rojo.set_3d_properties([punto[2]])

    # Actualizar texto del giroscopio
    gx, gy, gz = gyro_data[frame]
    text_gyro.set_text(f"Gyro: X={gx:.2f}, Y={gy:.2f}, Z={gz:.2f} °/s")

    return frisbee_patch, punto_rojo, text_gyro

# Crear animación
ani = FuncAnimation(fig, update, frames=len(times), interval=50, blit=False)

plt.tight_layout()
plt.show()