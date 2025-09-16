import os
import json
from smart_home.core.dispositivos import TipoDispositivo  
from smart_home.dispositivos.tomada import Smartplug
from smart_home.dispositivos.porta import Port
from smart_home.dispositivos.geladeira import Freeze
from smart_home.dispositivos.luz import Ligth
from smart_home.dispositivos.umidificador import Humidifier
from smart_home.dispositivos.ar_condicionado import AirConditioner


# Função para salvar a configuração do hub em um arquivo JSON
def salvar_config(self, arquivo="data/config.json"):
    # Define diretório base e de dados
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    data_dir = os.path.join(base_dir, "data")
    os.makedirs(data_dir, exist_ok=True) 

    # Ajusta caminho do arquivo se não for absoluto
    if not os.path.isabs(arquivo):
        arquivo = os.path.join(data_dir, os.path.basename(arquivo))
 
    # Monta dicionário com dados do hub
    data = {
        "hub": {
            "nome": self.nome,
            "versao": "1.0" 
        },
        "dispositivos": [],
        "rotinas": self.rotinas
    }

    # Serializa cada dispositivo
    for d in self.dispositivos.values():
        atributos_serializaveis = {}
        for k, v in d.__dict__.items():
            # Ignora atributos que não devem ser salvos
            if k in ("id", "nome", "tipo", '_moment_on'):
                continue
            # Salva apenas tipos simples
            if isinstance(v, (int, float, str, bool, list, dict, type(None))):
                atributos_serializaveis[k] = v

        # Adiciona dispositivo ao JSON
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



# Função para carregar configuração do hub a partir de um arquivo JSON
def carregar_config(self, arquivo="config.json"):

    with open(arquivo, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Atualiza nome e rotinas do hub
    self.nome = data["hub"]["nome"]
    if "rotinas" in data and data["rotinas"]:
        self.rotinas = data["rotinas"]

    # Carrega dispositivos do JSON
    for d in data.get("dispositivos", []):
        id_ = d["id"]
        nome = d["nome"]
        tipo = d["tipo"]  # Tipo do dispositivo
        atributos = d.get("atributos", {})
        estado_salvo = d.get("estado")  # <- pega estado do JSON

        try:
            tipo_enum = TipoDispositivo[tipo]  # Converte string para enum
        except KeyError:
            print(f">> Tipo desconhecido: {tipo}")
            continue

        # Instancia o dispositivo correto conforme o tipo
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

        # Seta atributos extras do dispositivo
        for attr, valor in atributos.items():
            if attr == 'moment_on':
                continue
            setattr(dispositivo, attr, valor)

        # Restaura estado salvo (se existir e o dispositivo usar máquina de estados)
        if estado_salvo and hasattr(dispositivo, "machine"):
            try:
                # Converte string do estado para Enum correto
                if hasattr(dispositivo.state, "name"):  # Se o estado é Enum
                    estado_enum = type(dispositivo.state)[estado_salvo]
                    dispositivo.machine.set_state(estado_enum)
                else:
                    # fallback caso o estado não seja Enum
                    dispositivo.machine.set_state(estado_salvo)
            except Exception as e:
                print(f"[AVISO] Não foi possível restaurar estado '{estado_salvo}' para {id_}: {e}")

        # Adiciona o dispositivo ao hub
        self.adicionar_dispositivo(dispositivo)

    return data
