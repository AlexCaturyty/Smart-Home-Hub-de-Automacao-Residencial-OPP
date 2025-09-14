# smart_home/core/logger.py
import csv
from datetime import datetime

class LoggerCSV:
    _instance = None

    def __new__(cls, arquivo="data/eventos.csv"):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.arquivo = arquivo
            with open(arquivo, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["timestamp", "id_dispositivo", "evento", "estado"])
        return cls._instance

    def registrar(self, id_dispositivo: str, evento: str, estado: str):
        with open(self.arquivo, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now().isoformat(), id_dispositivo, evento, estado])
