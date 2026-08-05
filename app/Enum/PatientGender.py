from enum import Enum

class PatientGender(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    @property
    def label(self) -> str:
        labels = {
            self.MALE: "Male",
            self.FEMALE: "Female",
            self.OTHER: "Other",
        }
        return labels.get(self, "Unknown")
