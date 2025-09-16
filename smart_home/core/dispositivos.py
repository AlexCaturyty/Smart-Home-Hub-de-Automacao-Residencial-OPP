# smart_home/core/dispositivos.py
from abc import ABC, abstractmethod
from enum import Enum, auto

# -------- TIPOS DE DISPOSITIVOS --------
class TipoDispositivo(Enum):
    PORTA = "Porta"
    TOMADA = "Tomada"
    UMIDIFICADOR = "Umidificador"
    GELADEIRA = "Geladeira"
    ARCONDICIONADO = "Ar Condicionado"
    LUZ = "Luz"

# -------- classe base --------
class Dispositivo(ABC):
    def __init__(self, id_: str, nome: str, tipo: TipoDispositivo):
        self.id = id_
        self.nome = nome
        self.tipo = tipo
        
# -------- Status sobre os dispositios -----------------------------
    @abstractmethod
    def status(self):
        pass

# -------- classe intermediária para os dispositivos ligáveis --------
class Ligavel(Dispositivo):
    @abstractmethod
    def turn_on(self):
        pass

    @abstractmethod
    def turn_off(self):
        pass