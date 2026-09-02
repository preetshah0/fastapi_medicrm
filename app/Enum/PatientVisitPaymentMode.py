from enum import Enum

class PatientVisitPaymentMode(str, Enum):
    CASH = "cash"
    DIGITAL_PAYMENT = "digital_payment"

    @property
    def label(self) -> str:
        labels = {
            self.CASH: "Cash",
            self.DIGITAL_PAYMENT: "Digital Payment",
        }
        return labels.get(self, "Unknown")
