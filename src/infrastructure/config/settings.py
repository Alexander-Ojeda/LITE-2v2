#src\infrastructure\config\settings.py
from pathlib import Path

class AppConfig:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        self.clients_file = self.data_dir / "clients.json"
        self.id_plates_file = self.data_dir / "id_plates.json"
        self.catalog_file = self.data_dir / "equipment_catalog.json"