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
        self._temperature = 5
        self._mode = Mode.ECO

        self.machine = Machine(model=self, states=StatesFreeze, transitions=[
            {'trigger': 'ligar', 'source': StatesFreeze.OFF, 'dest': StatesFreeze.ON},
            {'trigger': 'desligar', 'source': StatesFreeze.ON, 'dest': StatesFreeze.OFF},
            {'trigger': 'abrir_porta', 'source': [StatesFreeze.CLOSED_DOOR, StatesFreeze.ON], 'dest': StatesFreeze.OPEN_DOOR},
            {'trigger': 'fechar_porta', 'source': StatesFreeze.OPEN_DOOR, 'dest': StatesFreeze.CLOSED_DOOR},
            {'trigger': 'ajustar_temperatura', 'source': [StatesFreeze.CLOSED_DOOR, StatesFreeze.OPEN_DOOR, StatesFreeze.ON] , 'dest': None, 'before': 'check_temperature'},
            {'trigger': 'mudar_modo', 'source': [StatesFreeze.CLOSED_DOOR, StatesFreeze.OPEN_DOOR, StatesFreeze.ON], 'dest': None, 'before': 'change_mode'}
        ], initial=StatesFreeze.OFF, auto_transitions=False)

    # -------- Implementações da ABC Dispositivo --------

    def turn_on(self):
        self.trigger("ligar")

    def turn_off(self):
        self.trigger("desligar")
    
    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Temp: {self._temperature}°C | Modo: {self._mode.value}"
    
    # ------------- Métodos da classe -----------------------
    
    def check_temperature(self, t):
        try:
            t_int = int(t)
            if 0 <= t_int <= 10:
                self._temperature = t_int
                print(f">> Temperatura ajustada: {t_int}°C")
            else:
                print(">> Temperatura inválida (0–10°C)")
        except (ValueError, TypeError):
            print(f">> Valor inválido para temperatura: {t}. Informe um número entre 0 e 10.")

    def change_mode(self, mode):
        try:
            self._mode = Mode[mode.upper()]
            print(f">> Modo alterado: {self._mode.value}")
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

    
