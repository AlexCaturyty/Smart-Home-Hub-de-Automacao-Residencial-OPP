from transitions import Machine
from enum import Enum, auto

class StatesFreeze(Enum):
    OPEN_DOOR = auto()
    CLOSED_DOOR = auto()
    ON = auto()
    OFF = auto()

class Mode(Enum):
    ECO = 'eco'
    TURBO = 'turbo'
    
class Freeze:
    def __init__(self):
        self.temperature = 5
        self.mode = Mode.ECO
        
    def check_temperature(self, temperature):
        if 0 <= temperature <= 10:
            if temperature != self.temperature:
                self.temperature = temperature
                print(f'>> Temperatura foi alterada para {self.temperature}°C')
            else:
                print(f'>> Temperatura já está em {self.temperature}°C')
            return True
        print('>> A geladeira só aceita temperatures entre 0°C e 10°C')
        return False
    
    def change_mode (self, mode):
        if isinstance(mode, str):
            mode = mode.upper()
            if mode in Mode.__members__:
                novo_mode = Mode[mode]
                if novo_mode != self.mode:
                    self.mode = novo_mode
                    print(f'>> O modo de energia foi alterado para {self.mode.value}')
                else:
                    print(f'>> O modo já está em {self.mode.value}')
            else:
                print(f'>> Modo inválido: {mode}')
        else:
            print(">> Tipo inválido de mode")
                
    def on_enter_OPEN_DOOR(self, *args, **kwargs):
        print('>> A geladeira foi aberta')
    
    def on_enter_CLOSED_DOOR(self, *args, **kwargs):
        print(">> Geladeira fechada")
    
    def on_enter_ON(self):
        print('>> Geladeira ligada')
    
    def on_enter_OFF(self):
        print('>> Geladeira desligada')

    

transitions = [
    {'trigger' : 'on' , 'source': StatesFreeze.OFF, 'dest' : StatesFreeze.ON},
    {'trigger': 'close_door', 'source': StatesFreeze.OPEN_DOOR, 'dest': StatesFreeze.CLOSED_DOOR},
    {'trigger': 'open_door', 'source': [StatesFreeze.CLOSED_DOOR, StatesFreeze.ON], 'dest': StatesFreeze.OPEN_DOOR, },
    {'trigger': 'adjust_temperature', 'source': StatesFreeze.CLOSED_DOOR, 'dest': None, 'before': 'check_temperature'},
    {'trigger': 'switch_mode', 'source': StatesFreeze.CLOSED_DOOR, 'dest': None, 'before': 'change_mode'}
]

f = Freeze()
machine = Machine(model=f, states=StatesFreeze, transitions=transitions, initial=StatesFreeze.OFF, auto_transitions=False)


if __name__ == '__main__':
    print("Estado inicial:", f.state)
    f.on()
    f.open_door()
    f.close_door()
    f.adjust_temperature(2)
    f.adjust_temperature(23)   
    f.switch_mode("TURBO")
    f.switch_mode("TURBO")      
    f.switch_mode("ECOu") 
