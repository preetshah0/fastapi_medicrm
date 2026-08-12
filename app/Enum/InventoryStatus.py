from enum import Enum


class InventoryStatus(str, Enum):
    IN_STOCK = "in_stock"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"

    @property
    def label(self) -> str:
        labels = {
            self.IN_STOCK: "In Stock",
            self.LOW_STOCK: "Low Stock",
            self.OUT_OF_STOCK: "Out of Stock",
        }
        return labels.get(self, self.value)
