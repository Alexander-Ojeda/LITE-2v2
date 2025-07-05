#src\core\application\use_cases\client\create_client.py
from core.application.common import Command, UseCase
from core.domain.client import Client
from core.ports.repositories import IClientRepository

class CreateClientCommand(Command):
    def __init__(self, client_id: str, name: str):
        self.client_id = client_id
        self.name = name

class CreateClientUseCase(UseCase):
    def __init__(self, client_repo: IClientRepository):
        self.client_repo = client_repo
    
    def execute(self, command: CreateClientCommand):
        # Validar si cliente ya existe
        if self.client_repo.get(command.client_id):
            raise ValueError(f"Cliente con ID {command.client_id} ya existe")
        
        client = Client(
            id=command.client_id,
            name=command.name
        )
        
        self.client_repo.add(client)
        return client