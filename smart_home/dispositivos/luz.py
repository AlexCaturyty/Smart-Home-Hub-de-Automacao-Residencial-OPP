from transitions import Machine
from enum import Enum, auto

class StateLight(Enum):
    OFF = auto()
    ON = auto()

class Colors(Enum):
    QUENTE = "quente"
    FRIA = "fria"
    NEUTRA = "neutra"

class Ligth():
    def __init__(self):
        self.on = False
        self.off = True
        self.brightness = 0
        self.color = Colors.NEUTRA

    def turn_on_light(self):
        if self.on:
            return False
        return True

    def turn_off_light(self):
        if self.off:
            return False
        return True

    def validate_brightness(self, valor):
        if valor <= 100 and valor >= 0:
            return True
        print(f">> Brilho inválido: {valor}. Deve estar entre 0 e 100.")
        return False
    
    def apply_color(self, color):
        if isinstance(color, str):
            color = color.upper()
            if color in Colors.__members__:
                self.color = Colors[color]
                print(f">> Cor definida para {self.color.value.upper()}")
            else:
                print(f">> Cor inválida: {color}")
        elif isinstance(color, Colors):
            self.color = color
            print(f">> Cor definida para {self.color.value.upper()}")
        else:
            print(">> Tipo inválido de cor")
    
    def set_brightness(self, valor):
        if self.validate_brightness(valor):
            self.brightness = valor
            print(f">> Brilho definido para {self.brightness}%.")

    def on_enter_ON(self, *args, **kwargs):
        if not self.on: 
            print(">> A luz acendeu")
        self.on = True
        self.off = False

    def on_enter_OFF(self):
        self.on = False
        self.off = True
        print('>> A luz apagou')

transitions = [
    {'trigger' : 'ligar', 'source' : StateLight.OFF, 'dest': StateLight.ON, 'conditions' : 'turn_on_light'},
    {'trigger' : 'desligar', 'source' : StateLight.ON, 'dest': StateLight.OFF},
    {'trigger' : 'definir_brightness', 'source' : StateLight.ON, 'dest' : StateLight.ON, 'before': 'set_brightness'},
    {"trigger": "definir_color", "source": StateLight.ON, 'dest' : StateLight.ON, "before": "apply_color"},

] 


l = Ligth()
machine = Machine(model=l, states=StateLight,transitions=transitions, initial=StateLight.OFF, auto_transitions=False)
if __name__ == '__main__':
    print("Estado inicial:", l.state)
    l.ligar() 
    l.definir_brightness(50)   
    l.definir_color("fria")
    l.desligar()