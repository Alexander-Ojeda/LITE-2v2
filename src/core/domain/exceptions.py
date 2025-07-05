#src\core\domain\exceptions.py
class DomainException(Exception):
    """Excepción base para errores de dominio"""

class InvalidLocationException(DomainException):
    """Ubicación no válida"""

class DuplicateIdPlateException(DomainException):
    """ID Plate duplicado"""

class EquipmentNotInCatalogException(DomainException):
    """Equipo no existe en catálogo"""