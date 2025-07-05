# core/application/use_cases/client/generate_client_report.py
from core.application.common import Command, UseCase
from core.ports.repositories import IClientRepository, IIdPlateRepository
from collections import defaultdict

class GenerateClientReportCommand(Command):
    def __init__(self, client_id: str):
        self.client_id = client_id

class GenerateClientReportUseCase(UseCase):
    def __init__(self, 
                 client_repo: IClientRepository, 
                 id_plate_repo: IIdPlateRepository):
        self.client_repo = client_repo
        self.id_plate_repo = id_plate_repo
    
    def execute(self, command: GenerateClientReportCommand):
        client = self.client_repo.get(command.client_id)
        if not client:
            raise ValueError(f"Cliente {command.client_id} no encontrado")
        
        id_plates = self.id_plate_repo.list_by_client(command.client_id)
        
        # Estadísticas básicas
        stats = {
            "client_name": client.name,
            "total_plates": len(id_plates),
            "active_plates": sum(1 for p in id_plates if p.status == "ACTIVO"),
            "inactive_plates": sum(1 for p in id_plates if p.status == "INACTIVO"),
            "plates_with_notes": sum(1 for p in id_plates if p.notes),
            "id_plates_by_category": defaultdict(int),
            "id_plates_by_location": defaultdict(int),
            "id_plates_by_brand": defaultdict(int),
            "recent_audits": []
        }
        
        # Recopilar datos detallados
        for plate in id_plates:
            # Solo contar placas con equipo asignado
            if plate.equipment:
                stats["id_plates_by_category"][plate.equipment.category] += 1
                stats["id_plates_by_brand"][plate.equipment.brand] += 1
            
            if plate.location:
                loc_str = f"{plate.location.main}/{plate.location.secondary}"
                stats["id_plates_by_location"][loc_str] += 1
            
            if plate.audit_log:
                # Ordenar por timestamp para obtener la más reciente
                sorted_audit = sorted(plate.audit_log, key=lambda a: a.timestamp, reverse=True)
                latest_audit = sorted_audit[0]
                
                stats["recent_audits"].append({
                    "plate_id": plate.id,
                    "action": latest_audit.action,
                    "timestamp": latest_audit.timestamp.isoformat(),
                    "details": latest_audit.details
                })
        
        # Ordenar auditorías recientes
        stats["recent_audits"].sort(key=lambda x: x["timestamp"], reverse=True)
        
        return stats