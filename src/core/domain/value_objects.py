#src\core\domain\value_objects.py
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, List

@dataclass(frozen=True)
class Location:
    main: str
    secondary: str

    def __str__(self):
        return f"{self.main}/{self.secondary}"

@dataclass(frozen=True)
class TechnicalSpecs:
    values: Dict[str, Any]
    
    def get(self, key: str, default=None):
        return self.values.get(key, default)

@dataclass
class AuditEntry:
    timestamp: datetime
    action: str  # 'CREATED', 'LOCATION_CHANGE', 'STATUS_CHANGE', etc.
    details: str
    
    def to_dict(self):
        return {
            "timestamp": self.timestamp.isoformat(),
            "action": self.action,
            "details": self.details
        }