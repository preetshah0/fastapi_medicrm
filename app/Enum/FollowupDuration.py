from enum import IntEnum


class FollowupDuration(IntEnum):
    FIFTEEN = 15
    THIRTY = 30
    FORTY_FIVE = 45
    SIXTY = 60

    @property
    def label(self) -> str:
        labels = {
            self.FIFTEEN: "15 Mins",
            self.THIRTY: "30 Mins",
            self.FORTY_FIVE: "45 Mins",
            self.SIXTY: "1 Hour",
        }
        return labels.get(self, "Unknown")