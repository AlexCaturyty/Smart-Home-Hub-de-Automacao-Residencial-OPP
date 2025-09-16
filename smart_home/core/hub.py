from smart_home.core.erros import ConfigInvalida, TransicaoInvalida
from smart_home.core.logger import LoggerCSV
import csv
from smart_home.core.persistencia import salvar_config, carregar_config
from datetime import datetime
from transitions.core import MachineError
from smart_home.core.relatorios import Relatorios
from smart_home.dispositivos.tomada import Smartplug
from smart_home.dispositivos.tomada import Smartplug  
from smart_home.core.eventos import EventoHub, EventoDispositivo


# Classe principal do sistema, representa o Hub central da casa
class Hub:
    def __init__(self, nome="Minha Casa"):
        self.nome = nome  
        self.dispositivos = {} 
        self.observers = []  # Lista de observadores para eventos
        self.logger = LoggerCSV()  # Logger para registrar eventos em CSV
        self.rotinas = {
            "modo_frio": [
                {"id": "umidicador", "comando": "ligar"},
                {"id": "ar_quarto", "comando": "ligar", "argumentos": {"temperatura": 16}},
                {"id": "luz_id", "comando": "desligar"},
            ],
            "acordar": [
                {"id": "luz_sala", "comando": "ligar"},
                {"id": "umidificador", "comando": "ligar"},
                {"id": "ar_quarto", "comando": "desligar"},
            ]
        }


    # Adiciona um novo dispositivo ao hub
    def adicionar_dispositivo(self, dispositivo):
        self.dispositivos[dispositivo.id] = dispositivo
        # Notifica observadores sobre o novo dispositivo
        self.notificar({
            "evento": EventoHub.DISPOSITIVO_ADICIONADO,
            "id": dispositivo.id,
            "tipo": dispositivo.tipo.value
        })


    # Executa um comando em um dispositivo específico
    def executar_comando(self, id_, comando, *args, **kwargs):
        disp = self.dispositivos.get(id_)
        if not disp:
            print(">> Dispositivo não encontrado.")
            return

        # Obtém o método do dispositivo pelo nome do comando
        metodo = getattr(disp, comando, None)
        if not callable(metodo):
            print(f">> Comando '{comando}' inválido para o dispositivo {id_}.")
            return

        antes = disp.status()  # Status antes do comando
        try:
            metodo(*args, **kwargs)  
        except MachineError as e:
            raise TransicaoInvalida(disp.nome, comando, disp.state.name) from e
        except Exception as e:
            print(f">> Erro ao executar comando: {e}")
        finally:
            depois = disp.status()  # Status depois do comando
            # Obtém consumo do dispositivo (Smartplug ou outros)
            consumo = getattr(disp, "_consumption_wh", 0) if isinstance(disp, Smartplug) else getattr(disp, "consumo_wh", 0)
            # Monta dicionário de estado para registrar no logger
            estado_para_logger = {
                "estado": depois.get("estado") if isinstance(depois, dict) else str(depois),
                "potencia_w": getattr(disp, "potencia_w", ""),
                "consumo_wh": round(consumo, 2),
                "temperatura": getattr(disp, "temperatura", ""),
                "brilho": getattr(disp, "brightness", "")
            }

            # Registra o evento no logger
            self.logger.registrar(
                id_,
                comando,
                estado_para_logger,
                nome_dispositivo=getattr(disp, "nome", ""),
                tipo_dispositivo=getattr(disp, "tipo", "")
            )


    # Lista todos os dispositivos cadastrados no hub
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
        rel = Relatorios()
        if tipo == "consumo":
            rel.consumo_por_tomada(arquivo)  
        elif tipo == "comandos":
            rel.comandos_por_tipo(arquivo)
        elif tipo == "ar_semana":
            rel.ar_condicionado_ligado_semana(arquivo)
        elif tipo == "tempo_luz":
            rel.tempo_luz_ligada(arquivo)
        elif tipo == "mais_usados":
            rel.dispositivos_mais_usados(arquivo)
        else:
            print(">> Tipo de relatório inválido.")

            

    # -------- PERSISTÊNCIA --------
    def salvar_config(self, arquivo="data/config.json"):
        salvar_config(self, arquivo)

    def carregar_config(self, arquivo="data/config.json"):
        try:
            carregar_config(self, arquivo)
        except Exception as e:
            raise ConfigInvalida(arquivo, str(e))