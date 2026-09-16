from enum import Enum

class PatientBloodGroup(Enum):
    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

    @property
    def label(self) -> str:
        labels = {
            self.A_POSITIVE: "A+",
            self.A_NEGATIVE: "A-",
            self.B_POSITIVE: "B+",
            self.B_NEGATIVE: "B-",
            self.O_POSITIVE: "O+",
            self.O_NEGATIVE: "O-",
            self.AB_POSITIVE: "AB+",
            self.AB_NEGATIVE: "AB-",
        }
        return labels.get(self, "Unknown")
