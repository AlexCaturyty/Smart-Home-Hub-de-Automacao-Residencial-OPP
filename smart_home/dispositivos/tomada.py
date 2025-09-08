from transitions import Machine
from enum import Enum, auto
from datetime import datetime
import time; 

class Statesmartplug(Enum):
    ON = auto()
    OFF = auto()

class Smartplug:
    def __init__(self, potencia_w=100):
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
 
    def on_enter_ON(self):
        self.moment_on = datetime.now()
        print(">> Tomada ligada!")

    def on_enter_OFF(self):
        if self.state == Statesmartplug.OFF and self.moment_on:
            time_seconds = (datetime.now() - self.moment_on).total_seconds()
            time_hours = time_seconds / 3600
            consumption = self.potencia_w * time_hours
            self.consumption_wh += consumption
            print(f">> Consumo acumulado: {self.consumption_wh:.2f} Wh")
        print(">> A tomada desconectou!")



transitions = [
    {'trigger': 'on', 'source': Statesmartplug.OFF, 'dest': Statesmartplug.ON},
    {'trigger': 'off', 'source': Statesmartplug.ON, 'dest': Statesmartplug.OFF}
]

p = Smartplug(potencia_w=60)
machine = Machine(model=p, states=Statesmartplug, transitions=transitions,
                  initial=Statesmartplug.OFF, auto_transitions=False)

if __name__ == '__main__':
    print("Estado inicial:", p.state)
    p.on()
    time.sleep(2)  
    p.off()
