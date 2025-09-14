# smart_home/core/observers.py
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, evento: dict):
        pass

class ConsoleObserver(Observer):
    def update(self, evento: dict):
        print(f"[EVENTO] {evento}")

class FileObserver(Observer):
    def __init__(self, path="data/observador.txt"):
        self.path = path

    def update(self, evento: dict):
        with open(self.path, "a", encoding="utf-8") as f:
            f.write(str(evento) + "\n")
