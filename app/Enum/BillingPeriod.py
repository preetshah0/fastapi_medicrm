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

    @property
    def stripe_interval(self) -> str:
        return "month" if self == self.MONTHLY else "year"
