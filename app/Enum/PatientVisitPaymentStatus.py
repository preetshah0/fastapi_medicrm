from enum import Enum

class PatientVisitPaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.PAID: "Paid",
        }
        return labels.get(self, "Unknown")
