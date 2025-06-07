from database.database import DataBase
import pandas as pd
import os

def main():
    # Definir rutas absolutas
    csv_dir = "/app/actividades/actividad1/static/csv"
    csv_file = os.path.join(csv_dir, "data_extractor.csv")
    
    # Verificar si existe el archivo
    print(f"Verificando archivo CSV en: {csv_file}")
    print(f"¿El directorio existe? {os.path.isdir(csv_dir)}")
    if os.path.exists(csv_file):
        print(f"✅ El archivo CSV existe! Tamaño: {os.path.getsize(csv_file)} bytes")
        print(f"Contenido del directorio: {os.listdir(csv_dir)}")
    else:
        print(f"❌ ERROR: El archivo CSV NO existe")
        print(f"Contenido del directorio (si existe): {os.listdir(csv_dir) if os.path.isdir(csv_dir) else 'directorio no existe'}")
        return
    
    # Continuar con la ingesta si existe el archivo
    database = DataBase()
    df = pd.read_csv(csv_file)
    print(f"CSV leído correctamente. Shape: {df.shape}")
    database.guardar_df(df)

if __name__ == "__main__":
    main()