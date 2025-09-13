from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StatesFreeze(Enum):
    OPEN_DOOR = auto()
    CLOSED_DOOR = auto()
    ON = auto()
    OFF = auto()

class Mode(Enum):
    ECO = 'eco'
    TURBO = 'turbo'

class Freeze(Dispositivo):
    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.GELADEIRA)
        self.temperature = 5
        self.mode = Mode.ECO

        self.machine = Machine(model=self, states=StatesFreeze, transitions=[
            {'trigger': 'ligar', 'source': StatesFreeze.OFF, 'dest': StatesFreeze.ON},
            {'trigger': 'desligar', 'source': StatesFreeze.ON, 'dest': StatesFreeze.OFF},
            {'trigger': 'abrir_porta', 'source': [StatesFreeze.CLOSED_DOOR, StatesFreeze.ON], 'dest': StatesFreeze.OPEN_DOOR},
            {'trigger': 'fechar_porta', 'source': StatesFreeze.OPEN_DOOR, 'dest': StatesFreeze.CLOSED_DOOR},
            {'trigger': 'ajustar_temperatura', 'source': StatesFreeze.CLOSED_DOOR, 'dest': None, 'before': 'check_temperature'},
            {'trigger': 'mudar_modo', 'source': StatesFreeze.CLOSED_DOOR, 'dest': None, 'before': 'change_mode'}
        ], initial=StatesFreeze.OFF, auto_transitions=False)

    # -------- Implementações da ABC Dispositivo --------

    def ligar(self):
        self.trigger("ligar")

    def desligar(self):
        self.trigger("desligar")
    
    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Temp: {self.temperature}°C | Modo: {self.mode.value}"
    
    # ------------- Métodos da classe -----------------------
    
    def check_temperature(self, t):
        if 0 <= t <= 10:
            self.temperature = t
            print(f">> Temperatura ajustada: {t}°C")
        else:
            print(">> Temperatura inválida (0–10°C)")

    def change_mode(self, mode):
        try:
            self.mode = Mode[mode.upper()]
            print(f">> Modo alterado: {self.mode.value}")
        except KeyError:
            print(">> Modo inválido (ECO/TURBO)")

    def on_enter_OPEN_DOOR(self): 
        print(">> Geladeira aberta.")
    def on_enter_CLOSED_DOOR(self): 
        print(">> Geladeira fechada.")
    def on_enter_ON(self):
        print(">> Geladeira ligada.")
    def on_enter_OFF(self):
        print(">> Geladeira desligada.")

    
