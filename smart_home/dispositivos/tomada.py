from transitions import Machine
from enum import Enum, auto
from datetime import datetime
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StatesSmartplug(Enum):
    ON = auto()
    OFF = auto()

class Smartplug(Dispositivo):
    def __init__(self, id_: str, nome: str, potencia_w=100):
        super().__init__(id_, nome, TipoDispositivo.TOMADA)
        self._potencia_w = None
        self.potencia_w = potencia_w
        self.consumption_wh = 0.0
        self.moment_on = None

        self.machine = Machine(model=self, states=StatesSmartplug, transitions=[
            {'trigger': 'ligar', 'source': StatesSmartplug.OFF, 'dest': StatesSmartplug.ON},
            {'trigger': 'desligar', 'source': StatesSmartplug.ON, 'dest': StatesSmartplug.OFF}
        ], initial=StatesSmartplug.OFF, auto_transitions=False)

      # -------- Implementações da ABC Dispositivo --------
    def ligar(self):
        self.trigger("ligar")

    def desligar(self):
        self.trigger("desligar")
    # ------------- Métodos da classe Tomada
    @property
    def potencia_w(self): return self._potencia_w

    @potencia_w.setter
    def potencia_w(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Potência deve ser >= 0")
        self._potencia_w = value

    def on_enter_ON(self):
        self.moment_on = datetime.now()
        print(">> Tomada ligada!")

    def on_enter_OFF(self):
        if self.moment_on:
            segundos = (datetime.now() - self.moment_on).total_seconds()
            self.consumption_wh += self.potencia_w * (segundos / 3600)
            print(f">> Consumo acumulado: {self.consumption_wh:.2f} Wh")
        print(">> Tomada desligada!")

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Consumo: {self.consumption_wh:.2f} Wh"
