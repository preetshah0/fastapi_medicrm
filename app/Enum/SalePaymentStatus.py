from enum import Enum

class SalePaymentStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    CANCELLED = "cancelled"
    
    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.PAID: "Paid",
            self.CANCELLED: "Cancelled",
        }
        return  labels.get(self)