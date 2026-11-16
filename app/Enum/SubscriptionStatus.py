from enum import Enum

class SubscriptionStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    CANCELLED = "cancelled"
    EXPIRED = "expired"

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.ACTIVE: "Active",
            self.INACTIVE: "Inactive",
            self.CANCELLED: "Cancelled",
            self.EXPIRED: "Expired",
        }
        return labels.get(self)