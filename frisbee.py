import pandas as pd
import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation as R

def cargar_datos_gps(archivo_gps):
    tabla = pd.read_csv(archivo_gps)
    tiempo = tabla["tiempo"].values
    lat = tabla["lat"].values
    lon = tabla["lon"].values
    alt = tabla["alt"].values
    return tiempo, lat, lon, alt
    

def convertir_a_metros(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32719", always_xy=True)
    x, y = transformer.transform(lon, lat)
    x = x - x[0]#obtener los metros recorridos desde 0,0
    y = y - y[0]
    return x, y
"""
def estimar_orientacion(tiempo, giroscopio):
    dt = np.gradient(tiempo)
    orientaciones = [R.identity()]
    q = R.identity()
    for i in range(1, len(tiempo)):
        omega = giroscopio[i]
        angulo = np.linalg.norm(omega * dt[i])
        if angulo > 0:
            eje = omega / np.linalg.norm(omega)
            rot = R.from_rotvec(eje * angulo)
            q = q * rot
        orientaciones.append(q)
    return orientaciones

def crear_disco():
    theta = np.linspace(0, 2*np.pi, 32)
    r = 0.15
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    z = np.zeros_like(x)
    return np.stack((x, y, z), axis=-1)
    
def transformar_aceleracion(aceleracion, orientaciones):
    acc_inercial = np.zeros_like(aceleracion)
    for i in range(len(aceleracion)):
        acc_inercial[i] = orientaciones[i].apply(aceleracion[i])
    return acc_inercial
    """

def integrar(tiempo, acc):
    dt = np.gradient(tiempo)
    velocidad = np.zeros_like(acc)
    for i in range(1, len(tiempo)):
        velocidad[i] = velocidad[i-1] + acc[i] * dt[i]
    return velocidad

def calcular_velocidad_GPS(x, y, z, tiempo):
    dx = np.gradient(x, tiempo)
    dy = np.gradient(y, tiempo)
    dz = np.gradient(z, tiempo)
    v = np.sqrt(dx**2 + dy**2 + dz**2)
    return v

def animar_trayectoria(x, y, z, tiempo, velocidad, intervalo=100):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    ax.set_xlim(np.min(x)-5, np.max(x)+5)
    ax.set_ylim(np.min(y)-5, np.max(y)+5)
    ax.set_zlim(np.min(z)-5, np.max(z)+5)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Altitud (m)")
    ax.set_title("Trayectoria 3D del frisbee (GPS)")

    linea, = ax.plot([], [], [], 'b-', lw=2)
    punto, = ax.plot([], [], [], 'ro', markersize=6)
    texto = ax.text2D(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)

    def init():
        linea.set_data([], [])
        linea.set_3d_properties([])
        punto.set_data([], [])
        punto.set_3d_properties([])
        texto.set_text('')
        return linea, punto, texto

    def update(frame):
        linea.set_data(x[:frame+1], y[:frame+1])
        linea.set_3d_properties(z[:frame+1])
        punto.set_data(x[frame], y[frame])
        punto.set_3d_properties(z[frame])
        texto.set_text(f't = {tiempo[frame]:.1f} s | v = {velocidad[frame]:.2f} m/s')
        return linea, punto, texto

    ani = FuncAnimation(fig, update, frames=len(tiempo),
                        init_func=init, blit=False, interval=intervalo, repeat=False)
    plt.tight_layout()
    plt.show()

def main():
    archivo_gps = "gps_simuladoo.csv"
    tiempo, lat, lon, alt = cargar_datos_gps(archivo_gps)
    x, y = convertir_a_metros(lat, lon)
    z = alt - alt[0]
    velocidad = calcular_velocidad(x, y, z, tiempo)
    animar_trayectoria_3d(x, y, z, tiempo, velocidad, intervalo=100)

if __name__ == "__main__":
    main()

