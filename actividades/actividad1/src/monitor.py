import pandas as pd
import sqlite3
import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

class DatabaseMonitor:
    def __init__(self):
        self.rutadb = "actividades/actividad1/src/static/mercadolibre.db"
        self.tabla = "mercadolibre"
        self.ruta_log = "actividades/actividad1/src/static/logs/monitor_log.json"
        
    def verificar_base_datos(self):
        if not os.path.exists(self.rutadb):
            print(f"ERROR: Base de datos no encontrada en {self.rutadb}")
            return False
        try:
            conn = sqlite3.connect(self.rutadb)
            conn.close()
            print("Base de datos verificada correctamente")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo conectar a la base de datos: {str(e)}")
            return False

    def contar_registros(self):
        try:
            conn = sqlite3.connect(self.rutadb)
            cursor = conn.cursor()
            # Contar registros
            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla}")
            total_registros = cursor.fetchone()[0]
            # Contar registros con valores nulos en campos clave
            cursor.execute(f"SELECT COUNT(*) FROM {self.tabla} WHERE precio IS NULL OR titulo IS NULL")
            registros_nulos = cursor.fetchone()[0]
            # Última actualización
            cursor.execute(f"SELECT MAX(fecha_update) FROM {self.tabla}")
            ultima_actualizacion = cursor.fetchone()[0]
            conn.close()
            print(f"Total de registros: {total_registros}")
            print(f"Registros con valores nulos: {registros_nulos}")
            print(f"Última actualización: {ultima_actualizacion}")
            return {
                "total_registros": total_registros,
                "registros_nulos": registros_nulos,
                "ultima_actualizacion": ultima_actualizacion,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        except Exception as e:
            print(f"ERROR: No se pudo contar registros: {str(e)}")
            return None

    def guardar_log(self, metricas):
        try:
            os.makedirs(os.path.dirname(self.ruta_log), exist_ok=True)
            if os.path.exists(self.ruta_log):
                with open(self.ruta_log, 'r') as f:
                    try:
                        logs = json.load(f)
                    except:
                        logs = {"registros": []}
            else:
                logs = {"registros": []}
            logs["registros"].append(metricas)
            if len(logs["registros"]) > 30:
                logs["registros"] = logs["registros"][-30:]
            with open(self.ruta_log, 'w') as f:
                json.dump(logs, f, indent=2)
            print(f"Log guardado correctamente en {self.ruta_log}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo guardar el log: {str(e)}")
            return False

    def enviar_alerta(self, asunto, mensaje):
        try:
            email_emisor = os.environ.get('EMAIL_SENDER')
            email_receptor = os.environ.get('EMAIL_RECEIVER')
            email_password = os.environ.get('EMAIL_PASSWORD')
            smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
            smtp_port = int(os.environ.get('SMTP_PORT', 587))
            if not all([email_emisor, email_receptor, email_password]):
                print("ADVERTENCIA: No se enviará alerta por correo. Faltan credenciales.")
                return False
            msg = MIMEMultipart()
            msg['From'] = email_emisor
            msg['To'] = email_receptor
            msg['Subject'] = asunto
            msg.attach(MIMEText(mensaje, 'plain'))
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(email_emisor, email_password)
            server.send_message(msg)
            server.quit()
            print(f"Alerta enviada correctamente a {email_receptor}")
            return True
        except Exception as e:
            print(f"ERROR: No se pudo enviar la alerta: {str(e)}")
            return False

    def ejecutar_monitoreo(self):
        print("*******************************************************************")
        print(f"Inicio de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")
        if not self.verificar_base_datos():
            self.enviar_alerta(
                "ALERTA: Base de datos no accesible", 
                f"La base de datos no se encuentra o no es accesible. Fecha: {datetime.now()}"
            )
            return False
        metricas = self.contar_registros()
        if not metricas:
            self.enviar_alerta(
                "ALERTA: Error en monitoreo de DB", 
                f"No se pudo obtener métricas de la tabla {self.tabla}. Fecha: {datetime.now()}"
            )
            return False
        self.guardar_log(metricas)
        if metricas.get("registros_nulos", 0) > 0:
            self.enviar_alerta(
                "ALERTA: Registros con valores nulos", 
                f"Se detectaron {metricas['registros_nulos']} registros con valores nulos en la tabla {self.tabla}."
            )
        print("*******************************************************************")
        print(f"Fin de monitoreo: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("*******************************************************************")
        return True

if __name__ == "__main__":
    monitor = DatabaseMonitor()
    monitor.ejecutar_monitoreo()