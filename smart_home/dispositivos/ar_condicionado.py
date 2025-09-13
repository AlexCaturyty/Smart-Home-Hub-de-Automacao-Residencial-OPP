from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StatesAirConditioner(Enum):
    ON = auto()
    OFF = auto()

class AirConditionerMODE(Enum):
    QUENTE = 'quente'
    FRIO = 'frio'

class AirConditioner(Dispositivo):
    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.ARCONDICIONADO)
        self.temperature = 16
        self.mode = AirConditionerMODE.FRIO

        self.machine = Machine(model=self, states=StatesAirConditioner, transitions=[
            {'trigger': 'ligar', 'source': StatesAirConditioner.OFF, 'dest': StatesAirConditioner.ON},
            {'trigger': 'desligar', 'source': StatesAirConditioner.ON, 'dest': StatesAirConditioner.OFF},
            {'trigger': 'ajustar_temperatura', 'source': StatesAirConditioner.ON, 'dest': None, 'before': 'check_temperature'},
            {'trigger': 'mudar_modo', 'source': StatesAirConditioner.ON, 'dest': None, 'before': 'change_mode'}
        ], initial=StatesAirConditioner.OFF, auto_transitions=False)
        
    # -------- Implementações da ABC Dispositivo --------

    def ligar(self):
        self.trigger("ligar")

    def desligar(self):
        self.trigger("desligar")

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Temp: {self.temperature}°C | Modo: {self.mode.value}"
    # ------------- Métodos da classe -----------------------    
    def check_temperature(self, new_temp):
        try:
            new_temp = int(new_temp)  
        except (ValueError, TypeError):
            print(">> Valor inválido para temperatura. Use um número inteiro entre 16 e 30°C.")
            return

        if 16 <= new_temp <= 30:
            self.temperature = new_temp
            print(f">> Temperatura ajustada: {new_temp}°C")
        else:
            print(">> Temperatura inválida (16–30°C)")


    def change_mode(self, mode):
        try:
            self.mode = AirConditionerMODE[mode.upper()]
            print(f">> Modo alterado: {self.mode.value}")
        except KeyError:
            print(">> Modo inválido (FRIO/QUENTE)")

    def on_enter_ON(self):
        print(">> Ar-condicionado ligado.")
    def on_enter_OFF(self): 
        print(">> Ar-condicionado desligado.")

    
