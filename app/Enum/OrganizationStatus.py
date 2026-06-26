from enum import Enum

class OrganizationStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @property
    def label(self) -> str:
        labels = {
            self.ACTIVE: "Active",
            self.INACTIVE: "Inactive",
        }
        return  labels.get(self)