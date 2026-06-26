from enum import Enum

class OrganizationPlanType(str, Enum):
    MONTHLY = "monthly"
    YEARLY = "yearly"

    @property
    def label(self) -> str:
        labels = {
            self.MONTHLY: "Monthly",
            self.YEARLY: "Yearly",
        }
        return  labels.get(self)