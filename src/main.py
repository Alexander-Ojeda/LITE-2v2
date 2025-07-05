from infrastructure.system.initializer import initialize_system
from core.application.use_cases.client.create_client import CreateClientCommand
from core.application.use_cases.id_plate.create_id_plate import CreateIdPlateCommand
from core.application.use_cases.id_plate.assign_equipment import AssignEquipmentCommand
from core.application.use_cases.catalog.add_category import AddCategoryCommand
from core.application.use_cases.catalog.add_subcategory import AddSubcategoryCommand
from core.application.use_cases.catalog.add_brand import AddBrandCommand
from core.application.use_cases.catalog.add_model import AddModelCommand
from core.application.use_cases.client.generate_client_report import GenerateClientReportCommand
from core.application.use_cases.id_plate.add_photos import AddPhotosToIdPlateCommand

system = initialize_system()

# 1. Crear categorías
system.add_category_use_case.execute(AddCategoryCommand("Refrigeración"))
system.add_subcategory_use_case.execute(
    AddSubcategoryCommand("Refrigeración", "Refrigerador Horizontal")
)

# 2. Añadir marcas y modelos
system.add_brand_use_case.execute(AddBrandCommand("Infrico"))
system.add_model_use_case.execute(
    AddModelCommand(
        brand="Infrico",
        model="BMPP1500II",
        category="Refrigeración",
        subcategory="Refrigerador Horizontal"
    )
)

# 3. Consultar datos del catálogo
catalog = system.catalog_repository
print("Categorías:", catalog.get_categories())
print("Subcategorías de Refrigeración:", catalog.get_subcategories("Refrigeración"))
print("Marcas:", catalog.get_brands())
print("Modelos de Infrico:", catalog.get_models("Infrico"))

# 4. Luego añadir la variante con especificaciones
catalog.add_variant(
    brand="Infrico",
    model="BMPP1500II",
    variant="R290",
    specs={
        "voltage": "220V",
        "dimensions": {"width": 1468, "depth": 600, "height": 850},
        "gas_refrigerante": "R290"
    }
)

# 5. Crear cliente
client = system.create_client_use_case.execute(
    CreateClientCommand(client_id="RKUK", name="Riu Kukulkan")
)

# 6. Añadir ubicaciones
client.add_main_location("Restaurante Italiano")
client.add_secondary_location("Restaurante Italiano", "Área de cocina")
system.client_repository.update(client)

# 7. Crear ID Plate
id_plate = system.create_id_plate_use_case.execute(
    CreateIdPlateCommand(
        client_id="RKUK",
        plate_number="001",
        main_location="Restaurante Italiano",
        secondary_location="Área de cocina"
    )
)

print(f"ID Plate creada: {id_plate.id}")

# 8. Asignar equipo a la placa
id_plate = system.assign_equipment_use_case.execute(
    AssignEquipmentCommand(
        plate_id=id_plate.id,
        brand="Infrico",
        model="BMPP1500II",
        variant="R290"
    )
)

print(f"Equipo asignado: {id_plate.equipment.full_model}")
print(f"Especificaciones: {id_plate.equipment.technical_specs.values}")
print(f"Última entrada auditoría: {id_plate.audit_log[-1].details}")

# 9. Generar reporte
report = system.generate_client_report_use_case.execute(
    GenerateClientReportCommand(client_id="RKUK")
)

# 10. Mostrar resultados claros
print("\n=== REPORTE FINAL ===")
print(f"Cliente: {report['client_name']}")
print(f"Total placas: {report['total_plates']}")
print(f"Placas activas: {report['active_plates']}")
print(f"Placas inactivas: {report['inactive_plates']}")
print(f"Placas con notas: {report['plates_with_notes']}")

print("\nPlacas por categoría:")
for category, count in report["id_plates_by_category"].items():
    print(f"- {category}: {count} placas")

print("\nPlacas por marca:")
for brand, count in report["id_plates_by_brand"].items():
    print(f"- {brand}: {count} placas")

print("\nPlacas por ubicación:")
for location, count in report["id_plates_by_location"].items():
    print(f"- {location}: {count} placas")

print("\nÚltimas auditorías:")
for audit in report["recent_audits"]:
    print(f"[{audit['timestamp']}] {audit['plate_id']}: {audit['action']} - {audit['details']}")
    
# Crear una foto de prueba
import tempfile
from pathlib import Path

# Crear una imagen de prueba
with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_photo:
    temp_photo.write(b"fake image data")
    temp_photo_path = temp_photo.name

print(f"Ruta temporal de foto: {temp_photo_path}")

# Añadir fotos a la placa
result = system.add_photos_use_case.execute(
    AddPhotosToIdPlateCommand(
        plate_id=id_plate.id,
        client_id="RKUK",
        photo_paths=[temp_photo_path]
    )
)

print(f"Fotos añadidas: {result['saved_photos']}")
print(f"Total fotos ahora: {result['total_photos']}")

# Listar fotos de la placa
photo_service = system.photo_service
photos = photo_service.list_plate_photos("RKUK", id_plate.id)
print(f"Fotos almacenadas: {photos}")

# Obtener ruta de una foto
if photos:
    photo_path = photo_service.get_photo_path("RKUK", id_plate.id, photos[0])
    print(f"Ruta completa de foto: {photo_path}")

# Limpiar archivo temporal
Path(temp_photo_path).unlink()    