from enum import Enum

class LabReferralPriority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"

    @property
    def label(self) -> str:
        labels = {
            self.LOW: "Low",
            self.MEDIUM: "Medium",
            self.HIGH: "High",
            self.EMERGENCY: "Emergency",
        }
        return labels.get(self)
    
