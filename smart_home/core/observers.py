from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, evento: dict):
        pass

# Observador que imprime eventos no console
class ConsoleObserver(Observer):
    def update(self, evento: dict):
        print(f"[EVENTO] {evento}")  # Exibe o evento no terminal

# Observador que salva eventos em arquivo texto
class FileObserver(Observer):
    def __init__(self, path="data/observador.txt"):
        self.path = path  # Caminho do arquivo para registrar eventos

    def update(self, evento: dict):
        # Adiciona o evento ao final do arquivo
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(str(evento) + "\n")
