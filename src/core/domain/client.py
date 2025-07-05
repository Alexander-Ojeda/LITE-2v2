#src\core\domain\client.py
from dataclasses import dataclass, field
from typing import Dict, List, Set
from .value_objects import Location
from .exceptions import InvalidLocationException, DuplicateIdPlateException

@dataclass
class Client:
    id: str
    name: str
    main_locations: Set[str] = field(default_factory=set)
    secondary_locations: Dict[str, Set[str]] = field(default_factory=dict)
    id_plates: Set[str] = field(default_factory=set)  # IDs de placas
    
    def add_main_location(self, location: str):
        if location in self.main_locations:
            raise ValueError(f"Ubicación principal '{location}' ya existe")
        self.main_locations.add(location)
        self.secondary_locations[location] = set()
    
    def add_secondary_location(self, main_location: str, secondary_location: str):
        if main_location not in self.main_locations:
            raise ValueError(f"Ubicación principal '{main_location}' no existe")
        
        if secondary_location in self.secondary_locations[main_location]:
            raise ValueError(f"Ubicación secundaria '{secondary_location}' ya existe en '{main_location}'")
        
        self.secondary_locations[main_location].add(secondary_location)
    
    def validate_location(self, location: Location) -> bool:
        """Valida si una ubicación es válida para este cliente"""
        if location.main not in self.main_locations:
            return False
        if location.secondary not in self.secondary_locations[location.main]:
            return False
        return True
    
    def add_id_plate(self, plate_id: str):
        if plate_id in self.id_plates:
            raise DuplicateIdPlateException(f"ID Plate {plate_id} ya existe")
        self.id_plates.add(plate_id)
    
    def remove_id_plate(self, plate_id: str):
        if plate_id in self.id_plates:
            self.id_plates.remove(plate_id)