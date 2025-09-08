from transitions import Machine
from enum import Enum, auto

class StatePort(Enum):
    LOCKED = auto()
    UNLOCKED = auto()
    OPEN = auto()

class Port:
    def __init__(self):
        self.open = False
        self.closed = True
        self.locked = True
        self.unlocked = False
        self.invalid_attempts = 0  

    def can_lock(self):
        if self.open:
            print(">> Não é possível trancar a porta pois está aberta.")
            self.invalid_attempts += 1
            return False
        return True

    def can_open(self):
        if self.open:
            print(">> A porta já está aberta.")
            return False
        if self.locked:
            print(">> A porta está trancada, não pode abrir.")
            return False
        return True

    def open_door_does_not_lock(self):
        print(">> Não é possível trancar a porta pois ela está aberta.")
        self.invalid_attempts += 1


    def may_close(self):
        if self.open:
            return True
        print(">> A porta já está fechada.")
        return False

    def on_enter_LOCKED(self):
        self.locked = True
        self.unlocked = False
        self.open = False
        self.closed = True
        print(">> Port TRANCADA.")

    def on_enter_UNLOCKED(self):
        self.locked = False
        self.unlocked = True
        self.open = False
        self.closed = True
        print(">> Port DESTRANCADA e FECHADA!")

    def on_enter_OPEN(self):
        if not self.open:
            print(">> Port ABERTA.")
        self.open = True
        self.closed = False
       

transitions = [
    {'trigger': 'destrancar', 'source': StatePort.LOCKED, 'dest': StatePort.UNLOCKED},
    {'trigger': 'trancar',    'source': StatePort.UNLOCKED, 'dest': StatePort.LOCKED, 'conditions': 'can_lock'},
    {'trigger': 'abrir',      'source': StatePort.UNLOCKED, 'dest': StatePort.OPEN, 'conditions': 'can_open'},
    {'trigger': 'fechar',     'source': StatePort.OPEN,      'dest': StatePort.UNLOCKED, 'conditions': 'may_close'},
    {'trigger': 'trancar', 'source': StatePort.OPEN, 'dest': StatePort.OPEN, 'after': 'open_door_does_not_lock'}

]

p = Port()
machine = Machine(model=p, states=StatePort, transitions=transitions, initial=StatePort.LOCKED, auto_transitions=False)

if __name__ == '__main__':
    print("Estado inicial:", p.state)
    p.destrancar()  
    p.abrir()                     
    p.trancar()   
    p.fechar()
    p.trancar()   
    print("Tentativas inválidas:", p.invalid_attempts)
