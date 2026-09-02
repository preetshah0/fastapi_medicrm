from enum import Enum

class OrganizationStatus(Enum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    
    @property
    def label(self) -> str:
        labels = {
            self.ACTIVE: "Active",
            self.SUSPENDED: "Suspended",
        }
        return  labels.get(self)