from transitions import Machine
from enum import Enum, auto
from smart_home.core.dispositivos import Dispositivo, TipoDispositivo

class StatePort(Enum):
    LOCKED = auto()
    UNLOCKED = auto()
    OPEN = auto()

class Port(Dispositivo):
    def __init__(self, id_: str, nome: str):
        super().__init__(id_, nome, TipoDispositivo.PORTA)
        self.invalid_attempts = 0

        self.machine = Machine(model=self, states=StatePort, transitions=[
            {'trigger': 'destrancar', 'source': StatePort.LOCKED, 'dest': StatePort.UNLOCKED},
            {'trigger': 'trancar', 'source': StatePort.UNLOCKED, 'dest': StatePort.LOCKED, 'conditions': 'can_lock'},
            {'trigger': 'abrir', 'source': StatePort.UNLOCKED, 'dest': StatePort.OPEN},
            {'trigger': 'fechar', 'source': StatePort.OPEN, 'dest': StatePort.UNLOCKED, 'conditions': 'may_close'}
        ], initial=StatePort.LOCKED, auto_transitions=False)

    def can_lock(self):
        if self.state == StatePort.OPEN:
            print(">> Não pode trancar porta aberta!")
            self.invalid_attempts += 1
            return False
        return True

    def may_close(self): return self.state == StatePort.OPEN

    def on_enter_LOCKED(self): print(">> Porta trancada.")
    def on_enter_UNLOCKED(self): print(">> Porta destrancada e fechada.")
    def on_enter_OPEN(self): print(">> Porta aberta.")

    def ligar(self): 
        self.abrir()
    
    def desligar(self): 
        self.fechar()

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Tentativas inválidas: {self.invalid_attempts}"


