import pandas as pd
import numpy as np

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
