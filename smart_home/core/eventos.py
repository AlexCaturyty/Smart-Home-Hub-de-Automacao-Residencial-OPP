from enum import Enum, auto

class EventoHub(Enum):
    # Eventos gerais do Hub
    DISPOSITIVO_ADICIONADO = auto()
    DISPOSITIVO_REMOVIDO = auto()
    COMANDO_EXECUTADO = auto()
    ROTINA_EXECUTADA = auto()
    CONFIGURACAO_SALVA = auto()
    CONFIGURACAO_CARREGADA = auto()

class EventoDispositivo(Enum):
    # Eventos relacionados a dispositivos individuais
    LIGADO = auto()
    DESLIGADO = auto()
    ABERTO = auto()
    FECHADO = auto()
    TRANCADO = auto()
    DESTRANCADO = auto()
    BRILHO_ALTERADO = auto()
    COR_ALTERADA = auto()
    TEMPERATURA_ALTERADA = auto()
    INTENSIDADE_ALTERADA = auto()
    CONSUMO_ATUALIZADO = auto()
