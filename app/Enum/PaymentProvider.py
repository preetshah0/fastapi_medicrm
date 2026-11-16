from enum import Enum


class PaymentProvider(str, Enum):
    STRIPE = "stripe"
    MAMOPAY = "mamopay"
    RAZORPAY = "razorpay"
    SYSTEM = "system"

    @property
    def label(self) -> str:
        labels = {
            self.STRIPE: "Stripe",
            self.MAMOPAY: "Mamo Pay",
            self.RAZORPAY: "Razorpay",
            self.SYSTEM: "System",
        }
        return labels.get(self, self.value)
