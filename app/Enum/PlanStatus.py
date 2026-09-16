from enum import Enum

class PlanStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    INACTIVE = "inactive"

    @property
    def label(self) -> str:
        labels = {
            self.DRAFT: "Draft",
            self.ACTIVE: "Active",
            self.INACTIVE: "Inactive",
        }
        return labels.get(self, "Unknown")