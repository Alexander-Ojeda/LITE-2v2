#src\infrastructure\persistence\json\json_client_repository.py
import json
from typing import Optional
from core.domain.client import Client
from core.ports.repositories import IClientRepository
from infrastructure.config.settings import AppConfig

class JsonClientRepository(IClientRepository):
    def __init__(self, config: AppConfig):
        self.config = config
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        try:
            with open(self.config.clients_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"clients": {}}
    
    def _save_data(self):
        with open(self.config.clients_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def add(self, client: Client):
        self.data["clients"][client.id] = {
            "id": client.id,
            "name": client.name,
            "main_locations": list(client.main_locations),
            "secondary_locations": {
                main: list(secondaries) 
                for main, secondaries in client.secondary_locations.items()
            },
            "id_plates": list(client.id_plates)
        }
        self._save_data()
    
    def get(self, client_id: str) -> Optional[Client]:
        client_data = self.data["clients"].get(client_id)
        if not client_data:
            return None
        
        client = Client(
            id=client_data["id"],
            name=client_data["name"]
        )
        
        # Restaurar ubicaciones
        for loc in client_data["main_locations"]:
            client.main_locations.add(loc)
            client.secondary_locations[loc] = set()
        
        for main, secondaries in client_data["secondary_locations"].items():
            for sec in secondaries:
                client.secondary_locations[main].add(sec)
        
        # Restaurar placas
        for plate_id in client_data["id_plates"]:
            client.id_plates.add(plate_id)
        
        return client
    
    def update(self, client: Client):
        self.add(client)  # Sobrescribe los datos existentes