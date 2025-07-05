#src\core\application\use_cases\id_plate\create_id_plate.py
from core.application.common import Command, UseCase
from core.domain.id_plate import IdPlate
from core.domain.value_objects import Location
from core.ports.repositories import IClientRepository, IIdPlateRepository
from core.domain.exceptions import InvalidLocationException, DuplicateIdPlateException

class CreateIdPlateCommand(Command):
    def __init__(self, client_id: str, plate_number: str, main_location: str, secondary_location: str):
        self.client_id = client_id
        self.plate_number = plate_number
        self.main_location = main_location
        self.secondary_location = secondary_location

class CreateIdPlateUseCase(UseCase):
    def __init__(self, 
                 client_repo: IClientRepository, 
                 id_plate_repo: IIdPlateRepository):
        self.client_repo = client_repo
        self.id_plate_repo = id_plate_repo
    
    def execute(self, command: CreateIdPlateCommand):
        # Validar cliente
        client = self.client_repo.get(command.client_id)
        if not client:
            raise ValueError(f"Cliente {command.client_id} no encontrado")
        
        # Crear ID completo
        plate_id = f"{command.client_id}{command.plate_number}"
        
        # Validar unicidad
        if self.id_plate_repo.get(plate_id):
            raise DuplicateIdPlateException(f"ID Plate {plate_id} ya existe")
        
        # Validar ubicación
        location = Location(
            main=command.main_location,
            secondary=command.secondary_location
        )
        
        if not client.validate_location(location):
            raise InvalidLocationException(f"Ubicación inválida: {location}")
        
        # Crear entidad
        id_plate = IdPlate(
            id=plate_id,
            client_id=command.client_id,
            location=location
        )
        
        # Persistir
        self.id_plate_repo.add(id_plate)
        client.add_id_plate(plate_id)
        self.client_repo.update(client)
        
        return id_plate