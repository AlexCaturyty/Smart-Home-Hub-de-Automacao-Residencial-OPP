from smart_home.core.logger import LoggerCSV
import csv
from smart_home.core.persistencia import salvar_config, carregar_config
from datetime import datetime
from transitions.core import MachineError

class Hub:
        def __init__(self, nome="Minha Casa"):
            self.nome = nome
            self.dispositivos = {}
            self.observers = []
            self.logger = LoggerCSV()
            self.rotinas = {
            "modo_noite": [
                {"id": "luz_sala", "comando": "desligar"},
                {"id": "ar_quarto", "comando": "ligar", "argumentos": {"temperatura": 22}},
                {"id": "porta_entrada", "comando": "fechar"},
            ],
            "acordar": [
                {"id": "luz_sala", "comando": "ligar"},
                {"id": "umidificador", "comando": "ligar"},
                {"id": "ar_quarto", "comando": "desligar"},
            ]
        }

        def adicionar_dispositivo(self, dispositivo):
            self.dispositivos[dispositivo.id] = dispositivo
            self.notificar({
                "evento": "DispositivoAdicionado",
                "id": dispositivo.id,
                "tipo": dispositivo.tipo.value
            })

        def executar_comando(self, id_, comando, *args, **kwargs):
            disp = self.dispositivos.get(id_)
            if not disp:
                print(">> Dispositivo não encontrado.")
                return

            metodo = getattr(disp, comando, None)
            if not callable(metodo):
                print(f">> Comando '{comando}' inválido para o dispositivo {id_}.")
                return

            antes = disp.status()
            try:
                metodo(*args, **kwargs)
            except MachineError as e:
                print(f">> Comando '{comando}' não pôde ser executado no estado atual ({disp.state.name}).")
            except Exception as e:
                print(f">> Erro ao executar comando: {e}")
            finally:
                depois = disp.status()
                evento = {
                    "id": id_,
                    "comando": comando,
                    "antes": antes,
                    "depois": depois
                }
                self.notificar(evento)
                self.logger.registrar(id_, comando, depois)

        def listar_dispositivos(self):
            for d in self.dispositivos.values():
                print(d.status())

        # -------- OBSERVER --------
        def registrar_observer(self, observer):
            self.observers.append(observer)

        def notificar(self, evento):
            for obs in self.observers:
                obs.update(evento)

        # -------- ROTINAS --------
        def executar_rotina(self, nome):
            comandos = self.rotinas.get(nome)
            if not comandos:
                print(f">> Rotina '{nome}' não encontrada.")
                return
            print(f">> Executando rotina '{nome}'...")
            for cmd in comandos:
                id_ = cmd["id"]
                comando = cmd["comando"]
                args = cmd.get("argumentos", {})
                self.executar_comando(id_, comando, **args)

        # ------------ Relatório ---------------
        def gerar_relatorio(self, arquivo="data/eventos.csv", tipo=None):
            campos = ["timestamp", "id", "nome", "tipo", "estado"]

            extra_keys = set()
            for d in self.dispositivos.values():
                if tipo and d.tipo != tipo:
                    continue
                for k, v in d.__dict__.items():
                    if k.startswith("_") or k in ("id", "nome", "tipo"):
                        continue
                    extra_keys.add(k)
            campos += list(extra_keys)

            # criar arquivo CSV
            with open(arquivo, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=campos)
                writer.writeheader()
                timestamp = datetime.now().isoformat()
                for d in self.dispositivos.values():
                    if tipo and d.tipo != tipo:
                        continue
                    linha = {
                        "timestamp": timestamp,
                        "id": d.id,
                        "nome": d.nome,
                        "tipo": d.tipo.name,
                        "estado": getattr(d, "state", None).name if hasattr(d, "state") else None
                    }
                    for k in extra_keys:
                        linha[k] = getattr(d, k, "")
                    writer.writerow(linha)

            print(f">> Relatório salvo em '{arquivo}'")
            

        # -------- PERSISTÊNCIA --------
        def salvar_config(self, arquivo="data/config.json"):
            salvar_config(self, arquivo)

        def carregar_config(self, arquivo="data/config.json"):
            carregar_config(self, arquivo)