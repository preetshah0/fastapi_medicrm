from enum import Enum

class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    PAID = "paid"
    FAILED = "failed"

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.PROCESSING: "Processing",
            self.PAID: "Paid",
            self.FAILED: "Failed",
        }
        return labels.get(self, self.value)
