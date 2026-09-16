from enum import Enum

class SupplierType(Enum):
    DIRECT_SUPPLIER = "direct_supplier"
    MEDICAL_REPRESENTATIVE = "medical_representative"

    @property
    def label(self) -> str:
        labels = {
            self.DIRECT_SUPPLIER: "Direct Supplier",
            self.MEDICAL_REPRESENTATIVE: "Medical Representative",
        }
        return  labels.get(self)