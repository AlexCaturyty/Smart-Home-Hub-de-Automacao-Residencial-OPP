from transitions import Machine
from enum import Enum, auto


class StatesHumidifier(Enum):
    OFF = auto()
    ON = auto()

class Humidifier:
    def __init__(self):
        self._intensity = 3       
        self._water_level = 50     
    

    @property
    def intensity(self):
        return self._intensity
    
    @intensity.setter
    def intensity(self, value):
        if isinstance(value, int) and 1 <= value <= 5:
            self._intensity = value
            print(f">> Intensidade ajustada para {value}")
        else:
            print("!! Intensidade inválida (deve ser entre 1 e 5).")

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
            print("!! Sem água no reservatório! Não é possível ligar.")
            self.off()  
    
    def on_enter_OFF(self):
        print(">> Umidificador desligado")

    def adjust_intensity(self, value):
        self.intensity = value  

    def refuel(self, qtd):
        if isinstance(qtd, int) and qtd > 0:
            new_level = self._water_level + qtd
            if new_level > 100:
                self._water_level = 100
                print(f">> Reservatório cheio! (tentou reabastecer até {new_level}%)")
            else:
                self._water_level = new_level
                print(f">> Água reabastecida. Nível atual: {self._water_level}%")
        else:
            print("!! Quantidade inválida para refuel.")


transitions = [
    {'trigger': 'on', 'source': StatesHumidifier.OFF, 'dest': StatesHumidifier.ON},
    {'trigger': 'off', 'source': StatesHumidifier.ON, 'dest': StatesHumidifier.OFF},
    {'trigger': 'adjust_intensity', 'source': StatesHumidifier.ON, 'dest': None},
    {'trigger': 'refuel', 'source': '*', 'dest': None},
]

u = Humidifier()
machine = Machine(model=u, states=StatesHumidifier, transitions=transitions,
                  initial=StatesHumidifier.OFF, auto_transitions=False)

if __name__ == "__main__":
    print("Estado inicial:", u.state)
    u.on()                     
    u.adjust_intensity(3)   
    u.refuel(90)          
    u.off()                    
