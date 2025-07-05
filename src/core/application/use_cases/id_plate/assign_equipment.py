#src\core\application\use_cases\id_plate\assign_equipment.py
from core.application.common import Command, UseCase
from core.ports.repositories import IIdPlateRepository, IEquipmentCatalogRepository
from core.domain.equipment import Equipment
from core.domain.exceptions import EquipmentNotInCatalogException
from core.domain.value_objects import TechnicalSpecs

class AssignEquipmentCommand(Command):
    def __init__(self, plate_id: str, brand: str, model: str, variant: str):
        self.plate_id = plate_id
        self.brand = brand
        self.model = model
        self.variant = variant

class AssignEquipmentUseCase(UseCase):
    def __init__(self, 
                 id_plate_repo: IIdPlateRepository, 
                 catalog_repo: IEquipmentCatalogRepository):
        self.id_plate_repo = id_plate_repo
        self.catalog_repo = catalog_repo
    
    def execute(self, command: AssignEquipmentCommand):
        # Obtener la placa
        id_plate = self.id_plate_repo.get(command.plate_id)
        if not id_plate:
            raise ValueError(f"ID Plate {command.plate_id} no encontrada")
        
        # Validar que el modelo existe en el catálogo
        if not self.catalog_repo.model_exists(
            command.brand, 
            command.model, 
            command.variant
        ):
            raise EquipmentNotInCatalogException(
                f"Modelo no encontrado: {command.brand}/{command.model}/{command.variant}"
            )
        
        # Obtener detalles del modelo
        model_details = self.catalog_repo.get_model_details(
            command.brand, 
            command.model, 
            command.variant
        )
        
        # Crear entidad de equipo
        equipment = Equipment(
            brand=command.brand,
            model=command.model,
            variant=command.variant,
            category=model_details["category"],
            subcategory=model_details["subcategory"],
            technical_specs=TechnicalSpecs(model_details["specs"])
        )
        
        # Asignar equipo a la placa
        id_plate.assign_equipment(equipment)
        
        # Actualizar en el repositorio
        self.id_plate_repo.update(id_plate)
        
        return id_plate