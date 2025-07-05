# src/infrastructure/system/initializer.py
from infrastructure.di.container import Container

def initialize_system():
    container = Container()
    return container