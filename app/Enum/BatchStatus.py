from enum import Enum


class BatchStatus(str, Enum):
    IN_STOCK = "in_stock"
    EXPIRED = "expired"
    COMPLETED = "completed"  # All stock sold/dispensed

    @property
    def label(self) -> str:
        labels = {
            self.IN_STOCK: "In Stock",
            self.EXPIRED: "Expired",
            self.COMPLETED: "Completed",
        }
        return labels.get(self, self.value)
