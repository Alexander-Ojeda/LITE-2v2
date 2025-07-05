#src\infrastructure\persistence\json\json_id_plate_repository.py
import json
from datetime import datetime
from typing import Optional, List
from core.domain.id_plate import IdPlate
from core.domain.value_objects import AuditEntry, Location, TechnicalSpecs
from core.domain.equipment import Equipment  # Importar Equipment
from core.ports.repositories import IIdPlateRepository
from infrastructure.config.settings import AppConfig

class JsonIdPlateRepository(IIdPlateRepository):
    def __init__(self, config: AppConfig):
        self.config = config
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        try:
            with open(self.config.id_plates_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"id_plates": {}}
    
    def _save_data(self):
        with open(self.config.id_plates_file, 'w') as f:
            json.dump(self.data, f, indent=2, default=str)
    
    def add(self, id_plate: IdPlate):
        plate_data = self._entity_to_dict(id_plate)
        self.data["id_plates"][id_plate.id] = plate_data
        self._save_data()
    
    def get(self, plate_id: str) -> Optional[IdPlate]:
        plate_data = self.data["id_plates"].get(plate_id)
        if not plate_data:
            return None
        return self._dict_to_entity(plate_data)
    
    def update(self, id_plate: IdPlate):
        self.add(id_plate)  # Sobrescribe los datos existentes
    
    def list_by_client(self, client_id: str) -> List[IdPlate]:
        return [
            self._dict_to_entity(plate_data)
            for plate_id, plate_data in self.data["id_plates"].items()
            if plate_data["client_id"] == client_id
        ]
    
    def _entity_to_dict(self, id_plate: IdPlate) -> dict:
        data = {
            "id": id_plate.id,
            "client_id": id_plate.client_id,
            "status": id_plate.status,
            "location": {
                "main": id_plate.location.main if id_plate.location else None,
                "secondary": id_plate.location.secondary if id_plate.location else None
            },
            "photos": id_plate.photos,
            "notes": id_plate.notes,
            "audit_log": [entry.to_dict() for entry in id_plate.audit_log]
        }
        
        # Añadir información del equipo si existe
        if id_plate.equipment:
            data["equipment"] = {
                "brand": id_plate.equipment.brand,
                "model": id_plate.equipment.model,
                "variant": id_plate.equipment.variant,
                "category": id_plate.equipment.category,
                "subcategory": id_plate.equipment.subcategory,
                "technical_specs": id_plate.equipment.technical_specs.values
            }
        else:
            data["equipment"] = None
            
        return data
    
    def _dict_to_entity(self, data: dict) -> IdPlate:
        location = None
        if data["location"]["main"] and data["location"]["secondary"]:
            location = Location(
                main=data["location"]["main"],
                secondary=data["location"]["secondary"]
            )
        
        id_plate = IdPlate(
            id=data["id"],
            client_id=data["client_id"],
            status=data["status"],
            location=location,
            photos=data["photos"],
            notes=data["notes"]
        )
        
        # Restaurar audit log
        id_plate.audit_log = [
            AuditEntry(
                timestamp=datetime.fromisoformat(entry["timestamp"]),
                action=entry["action"],
                details=entry["details"]
            )
            for entry in data["audit_log"]
        ]
        
        # Restaurar equipo si existe
        if data.get("equipment") and data["equipment"] is not None:
            eq_data = data["equipment"]
            equipment = Equipment(
                brand=eq_data["brand"],
                model=eq_data["model"],
                variant=eq_data["variant"],
                category=eq_data["category"],
                subcategory=eq_data["subcategory"],
                technical_specs=TechnicalSpecs(eq_data["technical_specs"])
            )
            id_plate.equipment = equipment
        
        return id_plate