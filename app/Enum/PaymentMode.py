from enum import Enum


class PaymentMode(str, Enum):
    GATEWAY = "gateway"
    MANUAL = "manual"
    BANK_TRANSFER = "bank_transfer"
    CASH = "cash"

    @property
    def label(self) -> str:
        labels = {
            self.GATEWAY: "Payment Gateway",
            self.MANUAL: "Manual",
            self.BANK_TRANSFER: "Bank Transfer",
            self.CASH: "Cash",
        }
        return labels.get(self, self.value)
