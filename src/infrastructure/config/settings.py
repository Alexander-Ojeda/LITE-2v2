from pathlib import Path

class AppConfig:
    def __init__(self, storage_dir: str = "storage"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        # Directorios de datos
        self.data_dir = self.storage_dir / "data"
        self.data_dir.mkdir(exist_ok=True)
        
        # Directorio de fotos
        self.photos_base_dir = self.storage_dir / "photos"
        self.photos_base_dir.mkdir(exist_ok=True)
        
        # Archivos de datos
        self.clients_file = self.data_dir / "clients.json"
        self.id_plates_file = self.data_dir / "id_plates.json"
        self.catalog_file = self.data_dir / "equipment_catalog.json"
    
    def get_client_photos_dir(self, client_id: str) -> Path:
        """Obtiene el directorio de fotos para un cliente específico"""
        client_dir = self.photos_base_dir / "client" / client_id
        client_dir.mkdir(parents=True, exist_ok=True)
        return client_dir
    
    def get_plate_photos_dir(self, client_id: str, plate_id: str) -> Path:
        """Obtiene el directorio de fotos para una placa específica"""
        plate_dir = self.get_client_photos_dir(client_id) / plate_id
        plate_dir.mkdir(parents=True, exist_ok=True)
        return plate_dir