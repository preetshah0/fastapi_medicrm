from enum import Enum

class SupplierVisitPurpose(Enum):
    Meeting = 'meeting'
    Payment = 'payment'
    SampleDrop = 'sample_drop'
    Delivery = 'delivery'
    Other = 'other'

    @property
    def label(self) -> str:
        labels = {
            self.Meeting: "Meeting",
            self.Payment: "Payment",
            self.SampleDrop: "Sample Drop",
            self.Delivery: "Delivery",
            self.Other: "Other",
        }
        return  labels.get(self)
