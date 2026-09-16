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
        }
        return  labels.get(self)