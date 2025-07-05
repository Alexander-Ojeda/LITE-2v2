#src\core\application\use_cases\catalog\add_brand.py
from core.application.common import Command, UseCase
from core.ports.repositories import IEquipmentCatalogRepository

class AddBrandCommand(Command):
    def __init__(self, brand: str):
        self.brand = brand

class AddBrandUseCase(UseCase):
    def __init__(self, catalog_repo: IEquipmentCatalogRepository):
        self.catalog_repo = catalog_repo
    
    def execute(self, command: AddBrandCommand):
        self.catalog_repo.add_brand(command.brand)
        return {"status": "success", "message": f"Marca {command.brand} añadida"}