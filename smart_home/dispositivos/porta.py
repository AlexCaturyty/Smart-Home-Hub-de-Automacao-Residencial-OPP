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
        self._invalid_attempts = 0

        self.machine = Machine(model=self, states=StatePort, transitions=[
            {'trigger': 'destrancar', 'source': StatePort.LOCKED, 'dest': StatePort.UNLOCKED},
            {'trigger': 'trancar', 'source': [StatePort.UNLOCKED, StatePort.OPEN], 'dest': StatePort.LOCKED, 'conditions': 'can_lock'},
            {'trigger': 'abrir', 'source': StatePort.UNLOCKED, 'dest': StatePort.OPEN},
            {'trigger': 'fechar', 'source': StatePort.OPEN, 'dest': StatePort.UNLOCKED, 'conditions': 'may_close'}
        ], initial=StatePort.LOCKED, auto_transitions=False)

    # -------- Métodos auxiliares para a máquina --------


    def can_lock(self):
        if self.state == StatePort.OPEN:
            self._invalid_attempts += 1
            print(">> Não pode trancar porta aberta!")
            return False
        return True 

    def may_close(self): return self.state == StatePort.OPEN

    # -------- Callbacks da máquina --------
    def on_enter_LOCKED(self): print(">> Porta trancada.")
    def on_enter_UNLOCKED(self): print(">> Porta destrancada e fechada.")
    def on_enter_OPEN(self): print(">> Porta aberta.")

    # -------- Implementações da ABC Dispositivo --------

    def status(self):
        return f"{self.id} | {self.nome} | {self.tipo.value} | Estado: {self.state.name} | Tentativas inválidas: {self._invalid_attempts}"

    
    def turn_on(self): 
        self.abrir()
    
    def turn_off(self): 
        self.fechar()

