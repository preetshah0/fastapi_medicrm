from enum import Enum


class SaleType(str, Enum):
    INTERNAL = "internal"
    EXTERNAL = "external"

    @property
    def label(self) -> str:
        labels = {
            self.INTERNAL: "Internal Patient",
            self.EXTERNAL: "External Customer",
        }
        return  labels.get(self)