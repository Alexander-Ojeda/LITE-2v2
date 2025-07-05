from infrastructure.system.initializer import initialize_system
from core.application.use_cases.client.create_client import CreateClientCommand
from core.application.use_cases.id_plate.create_id_plate import CreateIdPlateCommand
from core.domain.client import Client  # Importar la entidad Client

system = initialize_system()

# Crear cliente
client = system.create_client_use_case.execute(
    CreateClientCommand(client_id="RKUK", name="Riu Kukulkan")
)

# Añadir ubicación principal y secundaria al cliente
# ¡Esto es necesario ANTES de crear la ID Plate!
client.add_main_location("Restaurante Italiano")
client.add_secondary_location("Restaurante Italiano", "Área de cocina")

# Actualizar el cliente en el repositorio
system.client_repository.update(client)

# Crear ID Plate
id_plate = system.create_id_plate_use_case.execute(
    CreateIdPlateCommand(
        client_id="RKUK",
        plate_number="001",
        main_location="Restaurante Italiano",
        secondary_location="Área de cocina"
    )
)

print(f"ID Plate creada: {id_plate.id}")
print(f"Log de auditoría: {id_plate.audit_log[0].details}")