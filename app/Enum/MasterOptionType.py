from enum import Enum


class MasterOptionType(str, Enum):
    # INVENTORY_CATEGORY = "inventory_category"
    # MR_VISIT_PURPOSE = "mr_visit_purpose"
    # SUPPLIER_VISIT_PURPOSE = "supplier_visit_purpose"
    # PATIENT_REPORT_TYPE = "patient_report_type"
    LAB_TYPE = "lab_type"
    PRODUCT_FORM = "product_form"
    PRODUCT_SIZE = "product_size"
    BASE_UNIT = "base_unit"

    @property
    def label(self) -> str:
        labels = {
            # self.INVENTORY_CATEGORY: "Inventory Category",
            # self.MR_VISIT_PURPOSE: "MR Visit Purpose",
            # self.SUPPLIER_VISIT_PURPOSE: "Supplier Visit Purpose",
            # self.PATIENT_REPORT_TYPE: "Patient Report Type",
            self.LAB_TYPE: "Lab Type",
            self.PRODUCT_FORM: "Product Form (Tablet, Syrup, etc.)",
            self.PRODUCT_SIZE: "Product Size (Box, Strip, Pack)",
            self.BASE_UNIT: "Base Unit (mg, ml, Tablet)",
        }
        return labels.get(self, self.value)
