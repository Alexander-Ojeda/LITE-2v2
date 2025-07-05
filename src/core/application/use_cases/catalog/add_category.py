#src\core\application\use_cases\catalog\add_category.py
from core.application.common import Command, UseCase
from core.ports.repositories import IEquipmentCatalogRepository

class AddCategoryCommand(Command):
    def __init__(self, category: str):
        self.category = category

class AddCategoryUseCase(UseCase):
    def __init__(self, catalog_repo: IEquipmentCatalogRepository):
        self.catalog_repo = catalog_repo
    
    def execute(self, command: AddCategoryCommand):
        self.catalog_repo.add_category(command.category)
        return {"status": "success", "message": f"Categoría {command.category} añadida"}