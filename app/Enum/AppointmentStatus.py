from enum import Enum

class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    OVERDUE = "overdue"

    @property
    def label(self) -> str:
        labels = {
            self.SCHEDULED: "Scheduled",
            self.CANCELLED: "Cancelled",
            self.COMPLETED: "Completed",
            self.OVERDUE: "Overdue",
        }
        return labels.get(self, "Unknown")
