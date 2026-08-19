from enum import Enum


class FollowupStatus(str, Enum):
    SCHEDULED = "scheduled"
    RESCHEDULED = "rescheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    OVERDUE = "overdue"

    @property
    def label(self) -> str:
        labels = {
            self.SCHEDULED: "Scheduled",
            self.RESCHEDULED: "Rescheduled",
            self.COMPLETED: "Completed",
            self.CANCELLED: "Cancelled",
            self.OVERDUE: "Overdue",
        }
        return labels.get(self, "Unknown")
