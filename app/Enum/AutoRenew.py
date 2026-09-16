from enum import Enum


class AutoRenew(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"

    @property
    def label(self) -> str:
        labels = {
            self.ACTIVE: "Active",
            self.INACTIVE: "Inactive",
        }
        return labels[self]
