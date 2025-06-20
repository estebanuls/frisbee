import pandas as pd
import numpy as np
from pyproj import Transformer
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial.transform import Rotation as R

def cargar_datos_vuelo(archivo):

    tabla = pd.read_csv(archivo)

    # Convertir a arrays 
    tiempo = tabla["tiempo"].values
    lat    = tabla["lat"].values
    lon    = tabla["lon"].values
    alt    = tabla["alt"].values

    acc = tabla[["acc_x", "acc_y", "acc_z"]].values  # se crea matriz de 3x3 para calculos vectoriales futturos
    gyro = tabla[["gyro_x", "gyro_y", "gyro_z"]].values  

    #guardarlo en diccionario para facil acceso
    datos = {
        "tiempo": tiempo,
        "lat": lat,
        "lon": lon,
        "alt": alt,
        "aceleracion": acc,
        "giroscopio": gyro
    }

    return datos

def convertir_a_metros(lat, lon):
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32719", always_xy=True)
    x, y = transformer.transform(lon, lat)
    x = x - x[0]#obtener los metros recorridos desde 0,0
    y = y - y[0]
    return x, y

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
    
def transformar_aceleracion(aceleracion, orientaciones):
    acc_inercial = np.zeros_like(aceleracion)
    for i in range(len(aceleracion)):
        acc_inercial[i] = orientaciones[i].apply(aceleracion[i])
    return acc_inercial

def integrar(tiempo, acc):
    dt = np.gradient(tiempo)
    velocidad = np.zeros_like(acc)
    for i in range(1, len(tiempo)):
        velocidad[i] = velocidad[i-1] + acc[i] * dt[i]
    return velocidad
   
def transformar_aceleracion(aceleracion, orientaciones):
    acc_inercial = np.zeros_like(aceleracion)
    for i in range(len(aceleracion)):
        acc_inercial[i] = orientaciones[i].apply(aceleracion[i])
    return acc_inercial

def animar_trayectoria_2d(x, y, intervalo=50):
    fig, ax = plt.subplots()
    ax.set_xlim(min(x)-5, max(x)+5)
    ax.set_ylim(min(y)-5, max(y)+5)
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_title("Animación 2D del vuelo del frisbi")
    plt.show()
