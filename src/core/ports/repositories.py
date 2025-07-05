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
    def add_category(self, category: str):
        pass
    
    @abstractmethod
    def add_subcategory(self, category: str, subcategory: str):
        pass
    
    @abstractmethod
    def add_brand(self, brand: str):
        pass
    
    @abstractmethod
    def add_model(self, brand: str, model: str, category: str, subcategory: str):
        pass
    
    @abstractmethod
    def add_variant(self, brand: str, model: str, variant: str, specs: dict):
        pass
    
    @abstractmethod
    def model_exists(self, brand: str, model: str, variant: str) -> bool:
        pass
    
    @abstractmethod
    def get_model_details(self, brand: str, model: str, variant: str) -> dict:
        pass
    
    @abstractmethod
    def get_categories(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_subcategories(self, category: str) -> List[str]:
        pass
    
    @abstractmethod
    def get_brands(self) -> List[str]:
        pass
    
    @abstractmethod
    def get_models(self, brand: str) -> List[str]:
        pass
    
    @abstractmethod
    def get_variants(self, brand: str, model: str) -> List[str]:
        pass