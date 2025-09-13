from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StatesHumidifier(Enum):
    OFF = auto()
    ON = auto()

class Humidifier(Dispositivo):
    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.UMIDIFICADOR)
        self._intensity = 3
        self._water_level = 50

        self.machine = Machine(model=self, states=StatesHumidifier, transitions=[
            {'trigger': 'ligar', 'source': StatesHumidifier.OFF, 'dest': StatesHumidifier.ON},
            {'trigger': 'desligar', 'source': StatesHumidifier.ON, 'dest': StatesHumidifier.OFF},
            {'trigger': 'ajustar_intensidade', 'source': StatesHumidifier.ON, 'dest': None},
            {'trigger': 'reabastecer', 'source': '*', 'dest': None},
        ], initial=StatesHumidifier.OFF, auto_transitions=False)

    def ligar(self):
        self.trigger("ligar")

    def desligar(self):
        self.trigger("desligar")
        
    @property
    def intensidade(self): return self._intensity

    @intensidade.setter
    def intensidade(self, value):
        if isinstance(value, int) and 1 <= value <= 5:
            self._intensity = value
            print(f">> Intensidade ajustada para {value}")
        else:
            print("!! Intensidade inválida (1–5).")

    @property
    def nivel_agua(self): 
        return self._water_level

    @nivel_agua.setter
    def nivel_agua(self, value):
        if isinstance(value, int) and 0 <= value <= 100:
            self._water_level = value
        else:
            print("!! Nível de água inválido (0–100).")

    def on_enter_ON(self):
        if self._water_level > 0:
            print(">> Umidificador ligado")
        else:
            print("!! Sem água, não é possível ligar.")
            self.desligar()

    def on_enter_OFF(self): print(">> Umidificador desligado")

    def ajustar_intensidade(self, value): self.intensidade = value

    def reabastecer(self, qtd):
        if isinstance(qtd, int) and qtd > 0:
            self._water_level = min(100, self._water_level + qtd)
            print(f">> Nível de água: {self._water_level}%")
        else:
            print("!! Quantidade inválida para reabastecer.")

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Água: {self._water_level}%"
