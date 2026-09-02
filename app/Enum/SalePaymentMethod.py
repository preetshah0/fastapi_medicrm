from enum import Enum

class SalePaymentMethod(str, Enum):
    CASH = "cash"
    CARD = "card"
    BANK = "bank"
    OTHER = "other"
    
    @property
    def label(self) -> str:
        labels = {
            self.CASH: "Cash",
            self.CARD: "Card",
            self.BANK: "Bank",
            self.OTHER: "Other",
        }
        return  labels.get(self)
