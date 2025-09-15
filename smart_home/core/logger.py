
import csv
from datetime import datetime

class LoggerCSV:
    _instance = None

    def __new__(cls, arquivo="data/eventos.csv"):
        # Implementação Singleton: garante que só existe uma instância
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        cls._instance.arquivo = arquivo
        # Cria o arquivo CSV e escreve o cabeçalho
        with open(arquivo, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                "timestamp",          
                "id_dispositivo",     
                "nome_dispositivo",   
                "tipo_dispositivo",  
                "evento",             
                "estado",             
                "potencia_w",         
                "consumo_wh",         
            ])
        return cls._instance

    def registrar(self, id_dispositivo, evento, estado: dict, nome_dispositivo=None, tipo_dispositivo=None):
        # Obtém o nome do tipo do dispositivo, se existir
        tipo_val = tipo_dispositivo.name if hasattr(tipo_dispositivo, "name") else tipo_dispositivo

        # Abre o arquivo CSV para adicionar uma nova linha com os dados do evento
        with open(self.arquivo, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().isoformat(),      
                id_dispositivo,                  
                nome_dispositivo or "",        
                tipo_val or "",                 # Tipo do dispositivo
                evento,                          
                estado.get("estado", ""),      
                estado.get("potencia_w", ""), 
                estado.get("consumo_wh", ""),  
            ])