import os
import json
from smart_home.core.dispositivos import TipoDispositivo  
from smart_home.dispositivos.tomada import Smartplug
from smart_home.dispositivos.porta import Port
from smart_home.dispositivos.geladeira import Freeze
from smart_home.dispositivos.luz import Ligth
from smart_home.dispositivos.umidificador import Humidifier
from smart_home.dispositivos.ar_condicionado import AirConditioner

def salvar_config(self, arquivo="data/config.json"): #     Salva todos os dados do hub (nome, dispositivos, rotinas) em um JSON.
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True)

    if not os.path.isabs(arquivo):
        arquivo = os.path.join(data_dir, os.path.basename(arquivo))

    data = {
        "hub": {
            "nome": self.nome,
            "versao": "1.0" 
        },
        "dispositivos": [],
        "rotinas": self.rotinas
    }

    for d in self.dispositivos.values():
        atributos_serializaveis = {}
        for k, v in d.__dict__.items():
            if k in ("id", "nome", "tipo", '_moment_on'):
                continue
            if isinstance(v, (int, float, str, bool, list, dict, type(None))):
                atributos_serializaveis[k] = v

        data["dispositivos"].append({
            "id": d.id,
            "tipo": d.tipo.name,
            "nome": d.nome,
            "estado": getattr(d, "state", None).name if hasattr(d, "state") else None,
            "atributos": atributos_serializaveis
        })


    with open(arquivo, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f">> Configuração salva em {arquivo}")


def carregar_config(self, arquivo="config.json"): #    Carrega dispositivos e rotinas de um JSON para dentro do hub.
    with open(arquivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    self.nome = data["hub"]["nome"]
    if "rotinas" in data and data["rotinas"]:
        self.rotinas = data["rotinas"]



    for d in data.get("dispositivos", []):
        id_ = d["id"]
        nome = d["nome"]
        tipo = d["tipo"]  
        atributos = d.get("atributos", {})

        try:
            tipo_enum = TipoDispositivo[tipo]  
        except KeyError:
            print(f">> Tipo desconhecido: {tipo}")
            continue

        if tipo_enum == TipoDispositivo.TOMADA:
            
            dispositivo = Smartplug(id_, nome, potencia_w=atributos.get("potencia_w", 0))
        elif tipo_enum == TipoDispositivo.PORTA:
            dispositivo = Port(id_, nome)
        elif tipo_enum == TipoDispositivo.GELADEIRA:
            dispositivo = Freeze(id_, nome)
        elif tipo_enum == TipoDispositivo.LUZ:
            dispositivo = Ligth(id_, nome)
        elif tipo_enum == TipoDispositivo.UMIDIFICADOR:
            dispositivo = Humidifier(id_, nome)
        elif tipo_enum == TipoDispositivo.ARCONDICIONADO:
            dispositivo = AirConditioner(id_, nome)
        else:
            print(f">> Tipo não suportado: {tipo_enum}")
            continue

        for attr, valor in atributos.items():
            if attr == 'moment_on':
                continue
            setattr(dispositivo, attr, valor)

        self.adicionar_dispositivo(dispositivo)

    return data
