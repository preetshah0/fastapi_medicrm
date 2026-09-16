from enum import Enum

class SalesStatus(str, Enum):
    PENDING = "pending"
    DISPENSED = "dispensed"
    CANCELLED = "cancelled"

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.DISPENSED: "Dispensed",
            self.CANCELLED: "Cancelled",
        }
        return  labels.get(self)