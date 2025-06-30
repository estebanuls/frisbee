import pandas as pd
import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.signal import medfilt

def cargar_datos_gps(archivo_gps):
    tabla = pd.read_csv(archivo_gps)
    tabla = tabla[(tabla['lat'] != 0) & (tabla['lon'] != 0)]
    tabla = tabla.drop_duplicates()

    tiempo = tabla["tiempo"].values / 1000#convertir a seg
    fecha = tabla["fecha"].values
    lat = tabla["lat"].values
    lon = tabla["lon"].values
    alt = tabla["alt"].astype(float).values

    # Limpiar ruido GPS
    lat, lon = limpiar_ruido_gps(lat, lon, tamano_ventana=5)

    return tiempo, fecha, lat, lon, alt


def convertir_a_metros(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32719", always_xy=True)
    x, y = transformer.transform(lon, lat)
    x -= x[0]
    y -= y[0]
    return x, y


def limpiar_ruido_gps(lat, lon, tamano_ventana=5):
    if tamano_ventana % 2 == 0:
        raise ValueError("El tamaño de la ventana debe ser impar.")
    lat_limpia = medfilt(lat, kernel_size=tamano_ventana)
    lon_limpia = medfilt(lon, kernel_size=tamano_ventana)
    return lat_limpia, lon_limpia


def calcular_velocidad(x, y, z, tiempo):
    dx = np.gradient(x, tiempo)
    dy = np.gradient(y, tiempo)
    dz = np.gradient(z, tiempo)
    return np.sqrt(dx**2 + dy**2 + dz**2)


def animar_trayectoria_2d_lateral(x, z, tiempo, velocidad, cd, cl, intervalo=100):
    fig, ax = plt.subplots(figsize=(8, 6))
    
    ax.set_xlim(np.min(x)-5, np.max(x)+5)
    ax.set_ylim(np.min(z)-5, np.max(z)+5)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Altitud (m)")
    ax.set_title(f"Trayectoria Lateral (X-Z)\nCd={cd:.4f}, Cl={cl:.4f}")
    ax.grid(True)

    linea, = ax.plot([], [], 'b-', lw=2)
    punto, = ax.plot([], [], 'ro', markersize=6)
    texto = ax.text(0.02, 0.95, '', transform=ax.transAxes, fontsize=12)

    def init():
        linea.set_data([], [])
        punto.set_data([], [])
        texto.set_text('')
        return linea, punto, texto

    def update(frame):
        linea.set_data(x[:frame+1], z[:frame+1])
        punto.set_data([x[frame]], [z[frame]])
        texto.set_text(f't = {tiempo[frame]:.1f} s | v = {velocidad[frame]:.2f} m/s')
        return linea, punto, texto

    ani = FuncAnimation(fig, update, frames=len(tiempo),
                        init_func=init, blit=False, interval=intervalo, repeat=False)
    plt.tight_layout()
    plt.show()


def estimar_coeficientes(tiempo, vx, vy):
    dvx_dt = np.gradient(vx, tiempo)
    dvy_dt = np.gradient(vy, tiempo) + 9.81  # g pasa al otro lado

    A1 = np.stack([-vx, vy], axis=1)
    B1 = dvx_dt

    A2 = np.stack([vx, -vy], axis=1)
    B2 = dvy_dt

    A_total = np.concatenate([A1, A2], axis=0)
    B_total = np.concatenate([B1, B2], axis=0)

    validos = ~np.isnan(A_total).any(axis=1) & ~np.isinf(A_total).any(axis=1)
    A_total = A_total[validos]
    B_total = B_total[validos]

    try:
        coef, _, _, _ = np.linalg.lstsq(A_total, B_total, rcond=1e-6)
        cd, cl = coef
        return cd, cl
    except np.linalg.LinAlgError:
        print("Error: No se pudo resolver el sistema. Datos posiblemente sin variación.")
        return float('nan'), float('nan')


def main():
    archivo_gps = "datos_gps_corregido.csv"
    tiempo, fecha, lat, lon, alt = cargar_datos_gps(archivo_gps)

    x, y = convertir_a_metros(lat, lon)
    z = alt - alt[0]

    # Velocidades en cada eje
    vx = np.gradient(x, tiempo)
    vy = np.gradient(y, tiempo)
    vz = np.gradient(z, tiempo)  # cambio de altitud

    # Velocidad total
    velocidad = calcular_velocidad(x, y, z, tiempo)

    cd, cl = estimar_coeficientes(tiempo, vx, vz)


    # Estimación de coeficientes aerodinámicos
    #cd, cl = estimar_coeficientes(tiempo, vx, vy)
    print(f"Coeficiente de arrastre (cd): {cd:.4f}")
    print(f"Coeficiente de sustentación (cl): {cl:.4f}")

    duracion_total = tiempo[-1] - tiempo[0]
    num_frames = len(tiempo)
    intervalo = (duracion_total / num_frames) * 1000  # intervalo en ms

    # Animación 2D lateral (X-Z)
    animar_trayectoria_2d_lateral(x, z, tiempo, velocidad, cd, cl, intervalo=intervalo)


if __name__ == "__main__":
    main()
