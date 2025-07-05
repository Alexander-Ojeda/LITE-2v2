#src\infrastructure\di\container.py
from core.ports.repositories import IClientRepository, IIdPlateRepository
from infrastructure.persistence.json.json_client_repository import JsonClientRepository
from infrastructure.persistence.json.json_id_plate_repository import JsonIdPlateRepository
from core.application.use_cases.client.create_client import CreateClientUseCase
from core.application.use_cases.id_plate.create_id_plate import CreateIdPlateUseCase
from infrastructure.config.settings import AppConfig

class Container:
    def __init__(self):
        self.config = AppConfig()
        
        # Initialize repositories
        self.client_repository: IClientRepository = JsonClientRepository(self.config)
        self.id_plate_repository: IIdPlateRepository = JsonIdPlateRepository(self.config)
        
        # Initialize use cases
        self.create_client_use_case = CreateClientUseCase(
            client_repo=self.client_repository
        )
        
        self.create_id_plate_use_case = CreateIdPlateUseCase(
            client_repo=self.client_repository,
            id_plate_repo=self.id_plate_repository
        )