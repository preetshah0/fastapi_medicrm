from enum import Enum

class LaboratoryLabType(Enum):
    CLINIC = "clinic"
    POLYCLINIC = "polyclinic"
    DIAGNOSTIC_CENTER = "diagnostic_center"
    NURSING_HOME = "nursing_home"
    GENERAL_HOSPITAL = "general_hospital"
    MULTI_SPECIALTY_HOSPITAL = "multi_specialty_hospital"
    SUPER_SPECIALTY_HOSPITAL = "super_specialty_hospital"
    MULTINATIONAL_HOSPITAL = "multinational_hospital"
    INDEPENDENT_REFERENCE = "independent_reference"
    RESEARCH = "research"
    PUBLIC_HEALTH = "public_health"
    MOBILE_CAMP = "mobile_camp"
    POCT = "point_of_care_testing"
    SPECIALIZED_PATHOLOGY = "specialized_pathology"
    MOLECULAR_BIOLOGY = "molecular_biology"
    MICROBIOLOGY = "microbiology"
    BIOCHEMISTRY = "biochemistry"
    GENETICS = "genetics"
    HEMATOLOGY = "hematology"
    IMMUNOLOGY = "immunology"
    OTHER = "other"

    @property
    def label(self) -> str:
        labels = {
            self.CLINIC: "Clinic Laboratory",
            self.POLYCLINIC: "Polyclinic Laboratory",
            self.DIAGNOSTIC_CENTER: "Diagnostic Center",
            self.NURSING_HOME: "Nursing Home Laboratory",
            self.GENERAL_HOSPITAL: "General Hospital Laboratory",
            self.MULTI_SPECIALTY_HOSPITAL: "Multi-specialty Hospital Laboratory",
            self.SUPER_SPECIALTY_HOSPITAL: "Super-specialty Hospital Laboratory",
            self.MULTINATIONAL_HOSPITAL: "Multinational Hospital Laboratory",
            self.INDEPENDENT_REFERENCE: "Independent/Reference Laboratory",
            self.RESEARCH: "Research Laboratory",
            self.PUBLIC_HEALTH: "Public Health Laboratory",
            self.MOBILE_CAMP: "Mobile/Camp Laboratory",
            self.POCT: "Point-of-Care Testing (POCT) Laboratory",
            self.SPECIALIZED_PATHOLOGY: "Specialized Pathology Laboratory",
            self.MOLECULAR_BIOLOGY: "Molecular Biology Laboratory",
            self.MICROBIOLOGY: "Microbiology Laboratory",
            self.BIOCHEMISTRY: "Biochemistry Laboratory",
            self.GENETICS: "Genetics Laboratory",
            self.HEMATOLOGY: "Hematology Laboratory",
            self.IMMUNOLOGY: "Immunology Laboratory",
            self.OTHER: "Other",
        }
        return labels.get(self)
