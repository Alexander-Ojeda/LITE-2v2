#src\core\application\use_cases\catalog\add_subcategory.py
from core.application.common import Command, UseCase
from core.ports.repositories import IEquipmentCatalogRepository

class AddSubcategoryCommand(Command):
    def __init__(self, category: str, subcategory: str):
        self.category = category
        self.subcategory = subcategory

class AddSubcategoryUseCase(UseCase):
    def __init__(self, catalog_repo: IEquipmentCatalogRepository):
        self.catalog_repo = catalog_repo
    
    def execute(self, command: AddSubcategoryCommand):
        self.catalog_repo.add_subcategory(command.category, command.subcategory)
        return {"status": "success", "message": f"Subcategoría {command.subcategory} añadida a {command.category}"}