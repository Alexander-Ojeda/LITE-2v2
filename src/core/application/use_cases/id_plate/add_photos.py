#src\core\application\use_cases\id_plate\add_photos.py
from core.application.common import Command, UseCase
from core.ports.repositories import IIdPlateRepository
from infrastructure.services.photo_service import PhotoService

class AddPhotosToIdPlateCommand(Command):
    def __init__(self, plate_id: str, client_id: str, photo_paths: list):
        self.plate_id = plate_id
        self.client_id = client_id
        self.photo_paths = photo_paths

class AddPhotosToIdPlateUseCase(UseCase):
    def __init__(self, 
                 id_plate_repo: IIdPlateRepository,
                 photo_service: PhotoService):
        self.id_plate_repo = id_plate_repo
        self.photo_service = photo_service
    
    def execute(self, command: AddPhotosToIdPlateCommand):
        # Obtener la placa
        id_plate = self.id_plate_repo.get(command.plate_id)
        if not id_plate:
            raise ValueError(f"ID Plate {command.plate_id} no encontrada")
        
        saved_filenames = []
        
        # Procesar cada foto
        for photo_path in command.photo_paths:
            filename = self.photo_service.save_photo(
                command.client_id,
                command.plate_id,
                photo_path
            )
            id_plate.add_photo(filename)
            saved_filenames.append(filename)
        
        # Actualizar en el repositorio
        self.id_plate_repo.update(id_plate)
        
        return {
            "plate_id": command.plate_id,
            "saved_photos": saved_filenames,
            "total_photos": len(id_plate.photos)
        }