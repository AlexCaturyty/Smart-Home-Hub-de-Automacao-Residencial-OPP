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
        self._potencia_w = potencia_w
        self._consumption_wh = 0.0
        self._moment_on = None

        self.machine = Machine(model=self, states=StatesSmartplug, transitions=[
            {'trigger': 'ligar', 'source': StatesSmartplug.OFF, 'dest': StatesSmartplug.ON},
            {'trigger': 'desligar', 'source': StatesSmartplug.ON, 'dest': StatesSmartplug.OFF}
        ], initial=StatesSmartplug.OFF, auto_transitions=False)

      # -------- Implementações da ABC Dispositivo --------
    def turn_on(self):
        self.trigger("ligar")

    def turn_off(self):
        self.trigger("desligar")

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Potência: {self._potencia_w}W | Consumo: {self._consumption_wh:.2f}Wh"
    
    # ------------- Métodos da classe -----------------------
    @property
    def potencia_w(self): 
        return self._potencia_w

    @potencia_w.setter
    def potencia_w(self, value):
        try:
            value = int(value)  
        except (ValueError, TypeError):
            raise ValueError("Potência deve ser um número inteiro >= 0")
        if value < 0:
            raise ValueError("Potência deve ser >= 0")
        self._potencia_w = value


    def on_enter_ON(self):
        self._moment_on = datetime.now()
        print(">> Tomada ligada!")

    def on_enter_OFF(self):
        if self._moment_on:
            segundos = (datetime.now() - self._moment_on).total_seconds()
            self._consumption_wh += self._potencia_w * (segundos / 3600)
            print(f">> Consumo acumulado: {self._consumption_wh:.2f} Wh")
        print(">> Tomada desligada!")

    
