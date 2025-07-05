#src\infrastructure\services\photo_service.py
from pathlib import Path
import shutil
import uuid
from infrastructure.config.settings import AppConfig

class PhotoService:
    def __init__(self, config: AppConfig):
        self.config = config
    
    def save_photo(self, client_id: str, plate_id: str, photo_path: str) -> str:
        """
        Guarda una foto en el sistema de almacenamiento
        Retorna el nombre del archivo guardado
        """
        # Obtener directorio destino
        plate_dir = self.config.get_plate_photos_dir(client_id, plate_id)
        
        # Generar nombre único para el archivo
        extension = Path(photo_path).suffix
        filename = f"{uuid.uuid4().hex}{extension}"
        dest_path = plate_dir / filename
        
        # Copiar la foto
        shutil.copy(photo_path, dest_path)
        
        return filename
    
    def get_photo_path(self, client_id: str, plate_id: str, filename: str) -> Path:
        """Obtiene la ruta completa de una foto"""
        return self.config.get_plate_photos_dir(client_id, plate_id) / filename
    
    def list_plate_photos(self, client_id: str, plate_id: str) -> list:
        """Lista todas las fotos asociadas a una placa"""
        plate_dir = self.config.get_plate_photos_dir(client_id, plate_id)
        return [f.name for f in plate_dir.iterdir() if f.is_file()]
    
    def delete_photo(self, client_id: str, plate_id: str, filename: str):
        """Elimina una foto específica"""
        photo_path = self.get_photo_path(client_id, plate_id, filename)
        if photo_path.exists():
            photo_path.unlink()