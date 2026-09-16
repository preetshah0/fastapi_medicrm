from enum import Enum


class FollowupVisitStatus(str, Enum):
    PENDING = "pending"
    VISITED = "visited"
    CONTACTED = "contacted"
    NOT_VISITED = "not_visited"
    CANCELLED = "cancelled"

    @property
    def label(self) -> str:
        labels = {
            self.PENDING: "Pending",
            self.VISITED: "Visited",
            self.CONTACTED: "Contacted",
            self.NOT_VISITED: "Not Visited",
            self.CANCELLED: "Cancelled",
        }
        return labels.get(self, "Unknown")
