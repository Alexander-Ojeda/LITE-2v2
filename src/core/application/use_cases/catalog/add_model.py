#src\core\application\use_cases\catalog\add_model.py
from core.application.common import Command, UseCase
from core.ports.repositories import IEquipmentCatalogRepository

class AddModelCommand(Command):
    def __init__(self, brand: str, model: str, category: str, subcategory: str):
        self.brand = brand
        self.model = model
        self.category = category
        self.subcategory = subcategory

class AddModelUseCase(UseCase):
    def __init__(self, catalog_repo: IEquipmentCatalogRepository):
        self.catalog_repo = catalog_repo
    
    def execute(self, command: AddModelCommand):
        self.catalog_repo.add_model(
            command.brand, 
            command.model, 
            command.category, 
            command.subcategory
        )
        return {"status": "success", "message": f"Modelo {command.model} añadido a {command.brand}"}