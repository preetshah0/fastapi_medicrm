from enum import Enum


class BillingPeriod(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @property
    def label(self) -> str:
        labels = {
            self.MONTHLY: "Monthly",
            self.YEARLY: "Yearly",
        }
        return labels[self]
