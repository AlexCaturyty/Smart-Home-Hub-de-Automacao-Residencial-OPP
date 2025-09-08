from transitions import Machine
from enum import Enum, auto
from datetime import datetime
import time; 

class Statesmartplug(Enum):
    ON = auto()
    OFF = auto()

class Smartplug:
    def __init__(self, potencia_w=100):
        self.on = False
        self.off = True
        self._potencia_w = None
        self.potencia_w = potencia_w  
        self.consumption_wh = 0.0
        self.moment_on = None


    @property
    def potencia_w(self):
        return self._potencia_w

    @potencia_w.setter
    def potencia_w(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Potência deve ser um inteiro >= 0")
        self._potencia_w = value


    def turn_on(self):
        return not self.on
    
    def turn_off(self):
        return not self.off
    
 
    def on_enter_ON(self):
        self.on = True
        self.off = False
        self.moment_on = datetime.now()
        print(">> Tomada conectada!")

    def on_enter_OFF(self):
        if self.on and self.moment_on:
            time_seconds = (datetime.now() - self.moment_on).total_seconds()
            time_hours = time_seconds / 3600
            consumption = self.potencia_w * time_hours
            self.consumption_wh += consumption
            print(f">> Consumo acumulado: {self.consumption_wh:.2f} Wh")
        self.on = False
        self.off = True
        print(">> A tomada desconectou!")



transitions = [
    {'trigger': 'ligar', 'source': Statesmartplug.OFF, 'dest': Statesmartplug.ON, 'conditions': 'turn_on'},
    {'trigger': 'desligar', 'source': Statesmartplug.ON, 'dest': Statesmartplug.OFF, 'conditions': 'turn_off'},
]

p = Smartplug(potencia_w=60)
machine = Machine(model=p, states=Statesmartplug, transitions=transitions,
                  initial=Statesmartplug.OFF, auto_transitions=False)

if __name__ == '__main__':
    print("Estado inicial:", p.state)
    p.ligar()
    time.sleep(10)  
    p.desligar()
