import pandas as pd
import sqlite3
import os
from datetime import datetime

class DataBase:
    def __init__(self, tabla="mercadolibre"):
        self.rutadb = "actividades/actividad1/src/static/mercadolibre.db"
        self.tabla = tabla

    def guardar_df(self, df=pd.DataFrame(), tabla=None):
        df = df.copy()
        tabla = tabla or self.tabla
        try:
            fecha_actual = datetime.now().strftime("%Y-%m-%d")
            df["fecha_create"] = fecha_actual
            df["fecha_update"] = fecha_actual
            with sqlite3.connect(self.rutadb) as conn:
                df.to_sql(tabla, conn, if_exists='replace', index=False)
            print("*******************************************************************")
            print("Datos guardados")
            print("*******************************************************************")
            print(f"Se guardó el df en base de datos. Cantidad de registros: {df.shape}")
        except Exception as errores:
            print(f"Error al guardar el df en base de datos: {errores}")

    def obtener_datos(self, nombre_tabla=None):
        tabla = nombre_tabla or self.tabla
        try:
            with sqlite3.connect(self.rutadb) as conn:
                consulta = f"SELECT * FROM {tabla}"
                df = pd.read_sql_query(consulta, conn)
            print("*******************************************************************")
            print("Se obtuvieron los datos de la base de datos")
            print("*******************************************************************")
            print(f"Base de datos cantidad de registros: {df.shape}")
            return df
        except Exception as errores:
            print(f"Error al obtener los datos de la tabla {tabla} en base de datos: {errores}")
            return pd.DataFrame()