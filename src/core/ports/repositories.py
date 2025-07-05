#src\core\ports\repositories.py
from abc import ABC, abstractmethod
from typing import Optional, List
from core.domain.client import Client
from core.domain.id_plate import IdPlate

class IClientRepository(ABC):
    @abstractmethod
    def add(self, client: Client):
        pass
    
    @abstractmethod
    def get(self, client_id: str) -> Optional[Client]:
        pass
    
    @abstractmethod
    def update(self, client: Client):
        pass

class IIdPlateRepository(ABC):
    @abstractmethod
    def add(self, id_plate: IdPlate):
        pass
    
    @abstractmethod
    def get(self, plate_id: str) -> Optional[IdPlate]:
        pass
    
    @abstractmethod
    def update(self, id_plate: IdPlate):
        pass
    
    @abstractmethod
    def list_by_client(self, client_id: str) -> List[IdPlate]:
        pass

class IEquipmentCatalogRepository(ABC):
    @abstractmethod
    def model_exists(self, brand: str, model: str, variant: str) -> bool:
        pass
    
    @abstractmethod
    def get_model_details(self, brand: str, model: str, variant: str) -> dict:
        pass