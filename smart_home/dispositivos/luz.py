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
        self._pending_brightness = None
        self._pending_color = None

        # Máquina de estados com transições
        self.machine = Machine(
            model=self,
            states=StateLigth,
            transitions=[
                {'trigger': 'ligar', 'source': StateLigth.OFF, 'dest': StateLigth.ON},
                {'trigger': 'desligar', 'source': StateLigth.ON, 'dest': StateLigth.OFF},
                {'trigger': 'definir_brilho', 'source': StateLigth.ON, 'dest': None, 'after': 'apply_brightness'},
                {'trigger': 'definir_cor', 'source': StateLigth.ON, 'dest': None, 'after': 'apply_color'},
            ],
            initial=StateLigth.OFF,
            auto_transitions=False
        )

    # -------- Implementações da ABC Dispositivo --------
    def turn_on(self):
        self.ligar()

    def turn_off(self):
        self.desligar()

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Brilho: {self._brightness}% | Cor: {self._color.value}"

    # ------------- Propriedades -----------------------
    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, valor):
        try:
            valor_int = int(valor)
            if 0 <= valor_int <= 100:
                self._brightness = valor_int
                print(f">> Brilho definido para {self._brightness}%.")
            else:
                print(f">> Brilho inválido: {valor}. Deve estar entre 0 e 100.")
        except (ValueError, TypeError):
            print(f">> Brilho inválido: {valor}. Informe um número entre 0 e 100.")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        try:
            if isinstance(value, Colors):
                self._color = value
            elif isinstance(value, str) and value.upper() in Colors.__members__:
                self._color = Colors[value.upper()]
            else:
                raise ValueError(f">> Cor inválida: {value}")
            print(f">> Cor definida para {self._color.value.upper()}")
        except Exception as e:
            print(e)

    # -------- Métodos auxiliares para a máquina --------
    def apply_brightness(self, valor=None, **kwargs):
        if valor is not None:
            self.brightness = valor

    def apply_color(self, valor=None, **kwargs):
        if valor is not None:
            self.color = valor

    # -------- Callbacks da máquina --------
    def on_enter_ON(self, *args, **kwargs):
        print(">> A luz foi ligada.")

    def on_enter_OFF(self, *args, **kwargs):
        print(">> A luz foi desligada.")
