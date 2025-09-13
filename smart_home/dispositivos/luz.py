from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StateLigth(Enum):
    OFF = auto()
    ON = auto()

class Colors(Enum):
    QUENTE = "quente"
    FRIA = "fria"
    NEUTRA = "neutra"

class Ligth(Dispositivo):
    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.LUZ)
        self._brightness = 0
        self._color = Colors.NEUTRA

        # Definição da máquina de estados
        self.machine = Machine(model=self, states=StateLigth, transitions=[
            {'trigger': 'ligar', 'source': StateLigth.OFF, 'dest': StateLigth.ON},
            {'trigger': 'desligar', 'source': StateLigth.ON, 'dest': StateLigth.OFF}
        ], initial=StateLigth.OFF, auto_transitions=False)

    # -------- Implementações da ABC Dispositivo --------
    def ligar(self):
        self.trigger("ligar")

    def desligar(self):
        self.trigger("desligar")

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Brilho: {self._brightness}% | Cor: {self._color.value}"
    # ------------- Métodos da classe -----------------------
    
    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, valor):
        if 0 <= valor <= 100:
            self._brightness = valor
            print(f">> Brilho definido para {self._brightness}%.")
        else:
            print(f">> Brilho inválido: {valor}. Deve estar entre 0 e 100.")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if isinstance(value, Colors):
            self._color = value
            print(f">> Cor definida para {self._color.value.upper()}")
        elif isinstance(value, str) and value.upper() in Colors.__members__:
            self._color = Colors[value.upper()]
            print(f">> Cor definida para {self._color.value.upper()}")
        else:
            print(f">> Cor inválida: {value}")

    def on_enter_ON(self):
        print(">> A luz foi ligada.")

    def on_enter_OFF(self):
        print(">> A luz foi desligada.")

    
    


