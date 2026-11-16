from enum import Enum


class UploadCategory(str, Enum):
    PROFILES = "profiles"
    DOCUMENTS = "documents"
    GENERAL = "general"

