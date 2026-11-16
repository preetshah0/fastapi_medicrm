from enum import Enum

class AppointmentType(Enum):
    GENERAL_CONSULTATION = "general_consultation"
    FOLLOW_UP = "follow_up"
    EMERGENCY = "emergency"
    WALK_IN = "walk_in"
    PROCEDURE = "procedure"
    OTHER = "other"

    @property
    def label(self) -> str:
        labels = {
            self.GENERAL_CONSULTATION: "General Consultation",
            self.FOLLOW_UP: "Follow Up",
            self.EMERGENCY: "Emergency",
            self.WALK_IN: "Walk-in",
            self.PROCEDURE: "Procedure",
            self.OTHER: "Other",
        }
        return labels.get(self, "Unknown")

