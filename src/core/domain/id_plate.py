#src\core\domain\id_plate.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from .value_objects import Location, TechnicalSpecs, AuditEntry
from .equipment import Equipment

class IdPlateStatus:
    ACTIVE = "ACTIVO"
    INACTIVE = "INACTIVO"

@dataclass
class IdPlate:
    id: str
    client_id: str
    status: str = IdPlateStatus.ACTIVE
    location: Optional[Location] = None
    equipment: Optional[Equipment] = None
    photos: List[str] = field(default_factory=list)
    notes: str = ""
    audit_log: List[AuditEntry] = field(default_factory=list)
    
    def __post_init__(self):
        self.add_audit_entry("CREATED", "Placa creada")
    
    def add_audit_entry(self, action: str, details: str):
        entry = AuditEntry(
            timestamp=datetime.now(),
            action=action,
            details=details
        )
        self.audit_log.append(entry)
    
    def change_location(self, new_location: Location):
        if self.location == new_location:
            return
            
        old_location = str(self.location) if self.location else "Ninguna"
        self.location = new_location
        self.add_audit_entry(
            "LOCATION_CHANGE",
            f"De: {old_location} → A: {new_location}"
        )
    
    def change_status(self, new_status: str):
        if self.status == new_status:
            return
            
        old_status = self.status
        self.status = new_status
        self.add_audit_entry(
            "STATUS_CHANGE",
            f"De: {old_status} → A: {new_status}"
        )
    
    def assign_equipment(self, equipment: 'Equipment'):
        self.equipment = equipment
        self.add_audit_entry(
            "EQUIPMENT_ASSIGNED",
            f"Equipo asignado: {equipment.brand} {equipment.model}"
        )
    
    def add_photo(self, photo_path: str):
        self.photos.append(photo_path)
        self.add_audit_entry(
            "PHOTO_ADDED",
            f"Foto añadida: {photo_path}"
        )
    
    def update_notes(self, notes: str):
        self.notes = notes
        self.add_audit_entry(
            "NOTES_UPDATED",
            "Notas actualizadas"
        )