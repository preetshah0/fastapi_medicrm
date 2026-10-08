from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    SUCCESS = "success"
    FAILED = "failed"
    REFUNDED = "refunded"

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.SUCCESS: "Success",
            self.FAILED: "Failed",
            self.REFUNDED: "Refunded",
        }
        return labels.get(self, self.value)
