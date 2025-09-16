from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo
from smart_home.core.erros import ValidacaoAtributo


# ---------- Estados e Enums ----------
class StateLigth(Enum):
    OFF = auto()
    ON = auto()

class Colors(Enum):
    QUENTE = "quente"
    FRIA = "fria"
    NEUTRA = "neutra"


# ---------- Descritores ----------
class BrilhoDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, 0)

    def __set__(self, instance, value):
        try:
            valor = int(value)
        except (ValueError, TypeError):
            raise ValidacaoAtributo("brightness", value, "O brilho deve ser um número entre 0 e 100")
        if not (0 <= valor <= 100):
            raise ValidacaoAtributo("brightness", valor, "O brilho deve estar entre 0 e 100")
        setattr(instance, self.private_name, valor)


class CorDescriptor:
    def __set_name__(self, owner, name):
        self.private_name = '_' + name
    
    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.private_name, Colors.NEUTRA)

    def __set__(self, instance, value):
        if isinstance(value, Colors):
            setattr(instance, self.private_name, value)
        elif isinstance(value, str):
            value_up = value.upper()
            if value_up in Colors.__members__:
                setattr(instance, self.private_name, Colors[value_up])
            else:
                raise ValidacaoAtributo("color", value, "Cor inválida: escolha QUENTE, FRIA ou NEUTRA")
        else:
            raise ValidacaoAtributo("color", value, "Cor inválida")


# ---------- Classe principal ----------
class Ligth(Dispositivo):
    brightness = BrilhoDescriptor()
    color = CorDescriptor()

    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.LUZ)
        self.brightness = 0
        self.color = Colors.NEUTRA

        # Máquina de estados
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
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Brilho: {self.brightness}% | Cor: {self.color.value}"

    # -------- Métodos auxiliares da máquina --------
    def apply_brightness(self, valor=None, **kwargs):
        if valor is not None:
            self.brightness = valor
            print(f">> Brilho definido para {self.brightness}%")

    def apply_color(self, valor=None, **kwargs):
        if valor is not None:
            self.color = valor
            print(f">> Cor definida para {self.color.value}")

    # -------- Callbacks da máquina --------
    def on_enter_ON(self, *args, **kwargs):
        print(">> A luz foi ligada.")

    def on_enter_OFF(self, *args, **kwargs):
        print(">> A luz foi desligada.")
