from enum import Enum

class PrescriptionStatus(str, Enum):
    DRAFT = "draft"
    FINALIZED = "finalized"
    

    @property
    def label(self) -> str:
        labels = {
            self.DRAFT: "Draft",
            self.FINALIZED: "Finalized",
        }
        return labels.get(self, "Unknown")