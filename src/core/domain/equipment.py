#src\core\domain\equipment.py
from dataclasses import dataclass
from .value_objects import TechnicalSpecs

@dataclass
class Equipment:
    brand: str
    model: str
    variant: str  # Identificador de variante (ej: "R290")
    category: str
    subcategory: str
    technical_specs: TechnicalSpecs
    
    @property
    def full_model(self):
        return f"{self.brand} {self.model} ({self.variant})"
    
    def update_specs(self, new_specs: dict):
        self.technical_specs = TechnicalSpecs(values=new_specs)