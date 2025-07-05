#src\infrastructure\di\container.py
from core.ports.repositories import IClientRepository, IIdPlateRepository, IEquipmentCatalogRepository
from infrastructure.persistence.json.json_client_repository import JsonClientRepository
from infrastructure.persistence.json.json_id_plate_repository import JsonIdPlateRepository
from core.application.use_cases.client.create_client import CreateClientUseCase
from core.application.use_cases.id_plate.create_id_plate import CreateIdPlateUseCase
from infrastructure.persistence.json.json_equipment_catalog_repository import JsonEquipmentCatalogRepository
from core.application.use_cases.id_plate.assign_equipment import AssignEquipmentUseCase
from core.application.use_cases.catalog.add_category import AddCategoryUseCase
from core.application.use_cases.catalog.add_subcategory import AddSubcategoryUseCase
from core.application.use_cases.catalog.add_brand import AddBrandUseCase
from core.application.use_cases.catalog.add_model import AddModelUseCase
from core.application.use_cases.client.generate_client_report import GenerateClientReportUseCase
from infrastructure.config.settings import AppConfig
from infrastructure.services.photo_service import PhotoService
from core.application.use_cases.id_plate.add_photos import AddPhotosToIdPlateUseCase

class Container:
    def __init__(self):
        self.config = AppConfig()
        
        # Servicios
        self.photo_service = PhotoService(self.config)
        
        # Initialize repositories
        self.client_repository: IClientRepository = JsonClientRepository(self.config)
        self.id_plate_repository: IIdPlateRepository = JsonIdPlateRepository(self.config)
        self.catalog_repository: IEquipmentCatalogRepository = JsonEquipmentCatalogRepository(self.config)
        
        # Initialize use cases
        self.create_client_use_case = CreateClientUseCase(
            client_repo=self.client_repository
        )
        
        self.create_id_plate_use_case = CreateIdPlateUseCase(
            client_repo=self.client_repository,
            id_plate_repo=self.id_plate_repository
        )
        
        # Nuevo caso de uso para asignar equipos
        self.assign_equipment_use_case = AssignEquipmentUseCase(
            id_plate_repo=self.id_plate_repository,
            catalog_repo=self.catalog_repository
        )
        
        # Casos de uso de catálogo
        self.add_category_use_case = AddCategoryUseCase(
            catalog_repo=self.catalog_repository
        )
        self.add_subcategory_use_case = AddSubcategoryUseCase(
            catalog_repo=self.catalog_repository
        )
        self.add_brand_use_case = AddBrandUseCase(
            catalog_repo=self.catalog_repository
        )
        self.add_model_use_case = AddModelUseCase(
            catalog_repo=self.catalog_repository
        )
        
        # Reportes
        self.generate_client_report_use_case = GenerateClientReportUseCase(
            client_repo=self.client_repository,
            id_plate_repo=self.id_plate_repository
        )
        
        # Nuevo caso de uso para fotos
        self.add_photos_use_case = AddPhotosToIdPlateUseCase(
            id_plate_repo=self.id_plate_repository,
            photo_service=self.photo_service
        )