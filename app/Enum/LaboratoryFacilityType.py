from enum import Enum

class LaboratoryFacilityType(Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"

    @property
    def label(self) -> str:
        labels = {
            self.INTERNAL: "Internal",
            self.EXTERNAL: "External",
        }
        return labels.get(self)
