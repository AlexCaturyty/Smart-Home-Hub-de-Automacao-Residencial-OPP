from transitions import Machine
from enum import Enum, auto

class StatesFreeze(Enum):
    Open_Door = auto()
    Closed_Door = auto()

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
                    print(f'>> O mode de energia foi alterado para {self.mode.value}')
                else:
                    print(f'>> O mode já está em {self.mode.value}')
            else:
                print(f'>> Modo inválido: {mode}')
        else:
            print(">> Tipo inválido de mode")
                
    def on_enter_Open_Door(self, *args, **kwargs):
        print('>> A geladeira foi aberta')
    
    def on_enter_Closed_Door(self, *args, **kwargs):
        print(">> Geladeira fechada")
    

transitions = [
    {'trigger': 'close_door', 'source': StatesFreeze.Open_Door, 'dest': StatesFreeze.Closed_Door},
    {'trigger': 'open_door', 'source': StatesFreeze.Closed_Door, 'dest': StatesFreeze.Open_Door},
    {'trigger': 'adjust_temperature', 'source': StatesFreeze.Closed_Door, 'dest': StatesFreeze.Closed_Door, 'before': 'check_temperature'},
    {'trigger': 'switch_mode', 'source': StatesFreeze.Closed_Door, 'dest': StatesFreeze.Closed_Door, 'before': 'change_mode'}
]

f = Freeze()
machine = Machine(model=f, states=StatesFreeze, transitions=transitions, initial=StatesFreeze.Closed_Door, auto_transitions=False)


if __name__ == '__main__':
    print("Estado inicial:", f.state)
    f.open_door()
    f.close_door()
    f.adjust_temperature(2)
    f.adjust_temperature(23)   
    f.switch_mode("TURBO")
    f.switch_mode("TURBO")      
    f.switch_mode("ECOu") 
