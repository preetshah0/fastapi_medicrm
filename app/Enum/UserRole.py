from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    OWNER = "owner"
    STAFF = "staff"

    @property
    def label(self) -> str:
        labels = {
            self.ADMIN: "Admin",
            self.OWNER: "Owner",
            self.STAFF: "Staff",
        }
        return  labels.get(self)