from enum import Enum

class MRVisitPurpose(Enum):
    SampleTesting = 'sample_testing'
    Meeting = 'meeting'
    ProductDemo = 'product_demo'
    OrderCollection = 'order_collection'
    CampOrganaization = 'camp_orgnization'
    Other = 'other'

    @property
    def label(self) -> str:
        labels = {
            self.SampleTesting: "Sample Testing",
            self.Meeting: "Meeting",
            self.ProductDemo: "Product Demo",
            self.OrderCollection: "Order Collection",
            self.CampOrganaization: "Camp Organization",
            self.Other: "Other",
        }
        return  labels.get(self)