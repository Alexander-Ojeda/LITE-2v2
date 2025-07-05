#src/infrastructure/persistence/json/json_equipment_catalog_repository.py
import json
from typing import List
from core.ports.repositories import IEquipmentCatalogRepository
from infrastructure.config.settings import AppConfig

class JsonEquipmentCatalogRepository(IEquipmentCatalogRepository):
    def __init__(self, config: AppConfig):
        self.config = config
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        try:
            with open(self.config.catalog_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {
                "brands": {},
                "categories": {}
            }
    
    def _save_data(self):
        with open(self.config.catalog_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    # Métodos para categorías
    def add_category(self, category: str):
        if category not in self.data["categories"]:
            self.data["categories"][category] = {"subcategories": {}}
            self._save_data()
    
    def add_subcategory(self, category: str, subcategory: str):
        # Validar que la categoría exista primero
        if category not in self.data["categories"]:
            raise ValueError(f"Categoría '{category}' no existe")
        
        # Validar que la subcategoría no exista
        if subcategory in self.data["categories"][category]["subcategories"]:
            raise ValueError(f"Subcategoría '{subcategory}' ya existe en '{category}'")
        
        self.data["categories"][category]["subcategories"][subcategory] = {}
        self._save_data()
    
    # Métodos para marcas y modelos
    def add_brand(self, brand: str):
        if brand not in self.data["brands"]:
            self.data["brands"][brand] = {"models": {}}
            self._save_data()
    
    def add_model(self, brand: str, model: str, category: str, subcategory: str):
        self.add_brand(brand)
        
        if model not in self.data["brands"][brand]["models"]:
            self.data["brands"][brand]["models"][model] = {
                "category": category,
                "subcategory": subcategory,
                "variants": {}
            }
            self._save_data()
        else:
            # Actualizar categoría si es necesario
            model_data = self.data["brands"][brand]["models"][model]
            if category:
                model_data["category"] = category
            if subcategory:
                model_data["subcategory"] = subcategory
            self._save_data()
    
    def add_variant(self, brand: str, model: str, variant: str, specs: dict):
        if brand not in self.data["brands"] or model not in self.data["brands"][brand]["models"]:
            raise ValueError(f"Modelo {brand}/{model} no existe en el catálogo")
        
        model_data = self.data["brands"][brand]["models"][model]
        model_data["variants"][variant] = specs
        self._save_data()
    
    # Métodos de validación y consulta
    def model_exists(self, brand: str, model: str, variant: str) -> bool:
        return (
            brand in self.data["brands"] and
            model in self.data["brands"][brand]["models"] and
            variant in self.data["brands"][brand]["models"][model]["variants"]
        )
    
    def get_model_details(self, brand: str, model: str, variant: str) -> dict:
        if not self.model_exists(brand, model, variant):
            return None
        
        model_data = self.data["brands"][brand]["models"][model]
        return {
            "category": model_data["category"],
            "subcategory": model_data["subcategory"],
            "specs": model_data["variants"][variant]
        }
    
    def get_categories(self) -> List[str]:
        return list(self.data["categories"].keys())
    
    def get_subcategories(self, category: str) -> List[str]:
        if category in self.data["categories"]:
            return list(self.data["categories"][category]["subcategories"].keys())
        return []
    
    def get_brands(self) -> List[str]:
        return list(self.data["brands"].keys())
    
    def get_models(self, brand: str) -> List[str]:
        if brand in self.data["brands"]:
            return list(self.data["brands"][brand]["models"].keys())
        return []
    
    def get_variants(self, brand: str, model: str) -> List[str]:
        if brand in self.data["brands"] and model in self.data["brands"][brand]["models"]:
            return list(self.data["brands"][brand]["models"][model]["variants"].keys())
        return []