from database.database import DataBase
import pandas as pd

def main():
    database = DataBase()
    df = pd.read_csv("static/csv/data_extractor.csv")
    database.guardar_df(df)
    # df_db = database.obtener_datos(nombre_tabla="mercadolibre")
    # df_db.to_csv("static/csv/data_db.csv", index=False)

if __name__ == "__main__":
    main()