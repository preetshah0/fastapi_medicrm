from enum import Enum

class SubscriptionStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    @property
    def label(self) -> str:
        labels = {
            self.ACTIVE: "Active",
            self.INACTIVE: "Inactive",
            self.CANCELLED: "Cancelled",
            self.EXPIRED: "Expired",
        }
        return labels.get(self)