from transitions import Machine
from enum import Enum, auto

class StatesAirConditioner(Enum):
    ON = auto()
    OFF = auto()
    COOL = auto()
    WARM = auto()

class AirConditionerMODE(Enum):
    QUENTE = 'quente'
    FRIO = 'frio'

class AirConditioner:
    def __init__(self):
        self.temperature = 16
        self.mode = AirConditionerMODE.FRIO
        
    def check_temperature(self, temperature):
        if 16 <= temperature <= 30:
            if temperature != self.temperature:
                self.temperature = temperature
                print(f'>> Temperatura foi alterada para {self.temperature}°C')
            else:
                print(f'>> Temperatura já está em {self.temperature}°C')
            return True
        print('>> O Ar condicionado só aceita temperatures entre 16°C e 30°C')
        return False
    
    def change_mode (self, mode):
        if isinstance(mode, str):
            mode = mode.upper()
            if mode in AirConditionerMODE.__members__:
                novo_mode = AirConditionerMODE[mode]
                if novo_mode != self.mode:
                    self.mode = novo_mode
                    print(f'>> O modo foi alterado para {self.mode.value}')
                else:
                    print(f'>> O modo já está em {self.mode.value}')
            else:
                print(f'>> Modo inválido: {mode}')
        else:
            print(">> Tipo inválido de modo")
                
    def on_enter_WARM(self, *args, **kwargs):
        print('>> Modo frio ativado!')
    
    def on_enter_ON(self):
        print('>> Ar-Condicionado ligado')
    
    def on_enter_OFF(self):
        print('>> Ar-Condicionado desligado')

transitions = [
    {'trigger' : 'on' , 'source': StatesAirConditioner.OFF, 'dest' : StatesAirConditioner.ON},
    {'trigger' : 'off' , 'source': StatesAirConditioner.ON, 'dest' : StatesAirConditioner.OFF},
    {'trigger': 'adjust_temperature', 'source': StatesAirConditioner.ON, 'dest': None, 'before': 'check_temperature'},
    {'trigger': 'switch_mode', 'source': StatesAirConditioner.ON, 'dest': None, 'before': 'change_mode'}
]

a = AirConditioner()
machine = Machine(model=a, states=StatesAirConditioner, transitions=transitions, initial=StatesAirConditioner.OFF, auto_transitions=False)

if __name__ == '__main__':
    print("Estado inicial:", a.state)
    a.on()
    a.adjust_temperature(2)
    a.adjust_temperature(23)
    a.switch_mode("TURBO")  
    a.switch_mode("FRIO")
    a.switch_mode('QUENTE')
    a.off() 
