from transitions import Machine
from enum import Enum, auto

class StatePort(Enum):
    LOCKED = auto()
    UNLOCKED = auto()
    OPEN = auto()

class Port:
    def __init__(self):
        self.invalid_attempts = 0  

    def can_lock(self):
        if self.state == StatePort.OPEN:
            print(">> Não é possível trancar a porta pois está aberta.")
            return False
        return True

    def can_open(self):
        if self.state == StatePort.OPEN:
            print(">> A porta já está aberta.")
            return False
        if self.state == StatePort.LOCKED:
            print(">> A porta está trancada, não pode abrir.")
            return False
        return True

    def increment_exception(self):
        if self.state == StatePort.OPEN:
            self.invalid_attempts += 1
        

    def may_close(self):
        if self.state == StatePort.OPEN:
            return True
        print(">> A porta já está fechada.")
        return False

    def on_enter_LOCKED(self):

        print(">> Porta TRANCADA.")

    def on_enter_UNLOCKED(self):

        print(">> Porta DESTRANCADA e FECHADA!")

    def on_enter_OPEN(self):
        if self.state == StatePort.OPEN:
            print(">> Porta ABERTA.")
 
       

transitions = [
    {'trigger': 'destrancar', 'source': StatePort.LOCKED, 'dest': StatePort.UNLOCKED},
    {'trigger': 'trancar',    'source': StatePort.UNLOCKED, 'dest': StatePort.LOCKED, 'conditions': 'can_lock'},
    {'trigger': 'abrir',      'source': StatePort.UNLOCKED, 'dest': StatePort.OPEN},
    {'trigger': 'fechar',     'source': StatePort.OPEN,      'dest': StatePort.UNLOCKED, 'conditions': 'may_close'},

]

p = Port()
machine = Machine(model=p, states=StatePort, transitions=transitions, initial=StatePort.LOCKED, auto_transitions=False, on_exception= 'increment_exception')

if __name__ == '__main__':
    print("Estado inicial:", p.state)
    p.destrancar()
    p.destrancar()
    p.abrir()
    print(f'1{p.state}')      
    p.trancar()   
    print(f'2{p.state}')     
    p.fechar()
    print(f'3{p.state}')     
    p.trancar()   
    print("Tentativas inválidas:", p.invalid_attempts)
