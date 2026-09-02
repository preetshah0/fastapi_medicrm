import uuid
from datetime import time
from app.model.Inventory import Inventory
from app.model.Product import Product
from typing import Optional, List
from app.Enum.PrescriptionStatus import PrescriptionStatus
from app.Enum.FollowupDuration import FollowupDuration
from app.model.User import User
from app.model.Branch import Branch
from app.model.Patient import Patient
from app.db.schemas import PrescriptionMedicationUpdate
from app.db.schemas import PrescriptionUpdate
from app.db.schemas import PrescriptionMedicationCreate
from app.db.schemas import PrescriptionCreate
from app.db.schemas import (
    BranchDropdownResponse,
    DoctorDropdownResponse,
    PatientDropdownResponse,
    MedicationDropdownResponse,
    FollowupDurationOptionResponse,
)
from sqlalchemy.orm import Session
from app.model.Prescription import Prescription
from app.model.Prescription import PrescriptionMedication


from app.model.FollowUp import PrescriptionFollowUp, FollowUp
from app.Enum.FollowupStatus import FollowupStatus
from app.Enum.FollowupVisitStatus import FollowupVisitStatus
from app.services.followup_service import (
    mark_overdue_followups,
    update_followup_on_edit,
    calculate_followup_end_time,
)


def refrence_code_generator(id: str = None) -> str:
    val = id or str(uuid.uuid4())
    return val.split("-")[0].upper()[:8]


def create_prescription(
    db: Session,
    prescription_data: PrescriptionCreate
):

    duration_val = (
        prescription_data.followup_duration.value 
        if prescription_data.followup_duration 
        else None
    )

    db_prescription = Prescription(
        branch_id=prescription_data.branch_id,
        patient_id=prescription_data.patient_id,
        doctor_id=prescription_data.doctor_id,
        ref=refrence_code_generator(),
        diagnosis=prescription_data.diagnosis,
        notes=prescription_data.notes,
        status=PrescriptionStatus.DRAFT.value,
        follow_up_required=prescription_data.follow_up_required,
        follow_up_date=prescription_data.follow_up_date,
        follow_up_time=prescription_data.follow_up_time,
        follow_up_note=prescription_data.follow_up_note,
        followup_duration=duration_val,
    )
    db.add(db_prescription)
    db.flush()

    if prescription_data.medications:
        medications_to_add = []
        for medication in prescription_data.medications:
            medications_to_add.append(
                PrescriptionMedication(
                    prescription_id=db_prescription.id,
                    inventory_id=medication.inventory_id,
                    inventory_batch_id=medication.inventory_batch_id,
                    drug_name=medication.drug_name,
                    quantity=medication.quantity,
                    dosage=medication.dosage,
                    frequency=medication.frequency,
                    meal_timing=medication.meal_timing,
                    duration=medication.duration,
                    notes=medication.notes,
                )
            )
        db.add_all(medications_to_add)

   
    if prescription_data.follow_up_required == True:
        branch = db.query(Branch).filter(Branch.id == prescription_data.branch_id).first()
        org_id = branch.organization_id if branch else None

        db_followup = PrescriptionFollowUp(
            organization_id=org_id,
            branch_id=prescription_data.branch_id,
            patient_id=prescription_data.patient_id,
            doctor_id=prescription_data.doctor_id,
            prescription_id=db_prescription.id,
            followable_type="prescription",
            followable_id=db_prescription.id,
            followup_date=prescription_data.follow_up_date,
            followup_time=prescription_data.follow_up_time,
            followup_duration=duration_val or 30,
            status=FollowupStatus.SCHEDULED.value,
            visited_status=FollowupVisitStatus.PENDING.value,
        )
        db.add(db_followup)

    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def create_medication(
    db: Session,
    prescription_id: str,
    medication_data: PrescriptionMedicationCreate,
    organization_id: str
):
    # db_prescription = (
    #     db.query(Prescription)
    #     .join(Branch, Prescription.branch_id == Branch.id)
    #     .filter(
    #         Prescription.id == prescription_id,
    #         Branch.organization_id == organization_id
    #     )
    #     .first()
    # )

    db_medication = PrescriptionMedication(
        prescription_id=prescription_id,
        inventory_id=medication_data.inventory_id,
        inventory_batch_id=medication_data.inventory_batch_id,
        drug_name=medication_data.drug_name,
        quantity=medication_data.quantity,
        dosage=medication_data.dosage,
        frequency=medication_data.frequency,
        meal_timing=medication_data.meal_timing,
        duration=medication_data.duration,
        notes=medication_data.notes,
    )
    db.add(db_medication)
    db.commit()
    db.refresh(db_medication)
    return db_medication


def get_prescriptions(db: Session, organization_id: str):
    return (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(Branch.organization_id == organization_id)
        .all()
    )


def get_prescription_by_id(db: Session, prescription_id: str, organization_id: str):
    return (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            Prescription.id == prescription_id,
            Branch.organization_id == organization_id
        )
        .first()
    )


def update_prescription(
    db: Session, 
    prescription_id: str, 
    prescription_data: PrescriptionUpdate, 
    organization_id: str
):
    db_prescription = (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            Prescription.id == prescription_id,
            Branch.organization_id == organization_id
        )
        .first()
    )

    if not db_prescription:
        return None

    update_data = prescription_data.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        if hasattr(db_prescription, key):
            setattr(db_prescription, key, value)

    mark_overdue_followups(db)

    existing_followup = (
        db.query(PrescriptionFollowUp)
        .filter(PrescriptionFollowUp.prescription_id == prescription_id)
        .order_by(PrescriptionFollowUp.created_at.desc())
        .first()
    )

    if db_prescription.follow_up_required == True:
        duration_val = db_prescription.followup_duration or 30
        if existing_followup:
            update_followup_on_edit(
                db=db,
                followup=existing_followup,
                new_date=db_prescription.follow_up_date,
                new_time=db_prescription.follow_up_time,
                new_duration=duration_val,
                patient_id=db_prescription.patient_id,
                doctor_id=db_prescription.doctor_id,
                branch_id=db_prescription.branch_id,
            )
        else:
            db_followup = PrescriptionFollowUp(
                organization_id=organization_id,
                branch_id=db_prescription.branch_id,
                patient_id=db_prescription.patient_id,
                doctor_id=db_prescription.doctor_id,
                prescription_id=db_prescription.id,
                followable_type="prescription",
                followable_id=db_prescription.id,
                followup_date=db_prescription.follow_up_date,
                followup_time=db_prescription.follow_up_time,
                followup_duration=duration_val,
                status=FollowupStatus.SCHEDULED.value,
                visited_status=FollowupVisitStatus.PENDING.value,
            )
            db.add(db_followup)

    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def update_medications(
    db: Session, 
    medication_id: str, 
    medication_data: PrescriptionMedicationUpdate, 
    organization_id: str
):
    db_medication = (
        db.query(PrescriptionMedication)
        .join(Prescription, PrescriptionMedication.prescription_id == Prescription.id)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            PrescriptionMedication.id == medication_id,
            Branch.organization_id == organization_id
        )
        .first()
    )



    update_data = medication_data.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        if hasattr(db_medication, key):
            setattr(db_medication, key, value)

    db.commit()
    db.refresh(db_medication)
    return db_medication


def delete_prescription(db: Session, prescription_id: str, organization_id: str):
    db_prescription = (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            Prescription.id == prescription_id,
            Branch.organization_id == organization_id
        )
        .first()
    )
    if not db_prescription:
        return False

    db.delete(db_prescription)
    db.commit()
    return True

def delete_medication(db: Session, medication_id: str, organization_id: str):
    db_medication = (
        db.query(PrescriptionMedication)
        .join(Prescription, PrescriptionMedication.prescription_id == Prescription.id)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            PrescriptionMedication.id == medication_id,
            Branch.organization_id == organization_id
        )
        .first()
    )
    db.delete(db_medication)
    db.commit()
    return True

def get_branch_dropdown(
    db: Session, 
    organization_id: str
):
    results = (
        db.query(Branch.id, Branch.branch_name)
        .filter(Branch.organization_id == organization_id)
        .all()
    )
    return [
        BranchDropdownResponse(id=row.id, branch_name=row.branch_name)
        for row in results
    ]


def get_doctor_dropdown(
    db: Session, 
    organization_id: str
):
    results = (
        db.query(User.id, User.name)
        .filter(
            User.organization_id == organization_id,
            User.role == "doctor"
        )
        .all()
    )
    return [
        DoctorDropdownResponse(id=row.id, name=row.name)
        for row in results
    ]


def get_patient_dropdown(
    db: Session, 
    organization_id: str
):
    results = (
        db.query(Patient.id, Patient.name)
        .filter(Patient.organization_id == organization_id)
        .all()
    )
    return [
        PatientDropdownResponse(id=row.id, name=row.name)
        for row in results
    ]

def update_prescription_status(db: Session, prescription_id: str, organization_id: str) -> bool:
    db_prescription = (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            Prescription.id == prescription_id,
            Branch.organization_id == organization_id,
            Prescription.status == PrescriptionStatus.DRAFT.value
        )
        .first()
    )



    db_prescription.status = PrescriptionStatus.FINALIZED.value
    db.commit()
    db.refresh(db_prescription)
    return True


def toggle_followup(db: Session, prescription_id: str, organization_id: str):
    db_prescription = (
        db.query(Prescription)
        .join(Branch, Prescription.branch_id == Branch.id)
        .filter(
            Prescription.id == prescription_id,
            Branch.organization_id == organization_id
        )
        .first()
    )

    if not db_prescription:
        return None

    db_prescription.follow_up_required = not db_prescription.follow_up_required

    existing_followup = (
        db.query(PrescriptionFollowUp)
        .filter(PrescriptionFollowUp.prescription_id == prescription_id)
        .first()
    )

    if db_prescription.follow_up_required:
        if not existing_followup:
            db_followup = PrescriptionFollowUp(
                organization_id=organization_id,
                branch_id=db_prescription.branch_id,
                patient_id=db_prescription.patient_id,
                doctor_id=db_prescription.doctor_id,
                prescription_id=db_prescription.id,
                followable_type="prescription",
                followable_id=db_prescription.id,
                followup_date=db_prescription.follow_up_date,
                followup_time=db_prescription.follow_up_time,
                followup_duration=db_prescription.followup_duration or 30,
                status=FollowupStatus.SCHEDULED.value,
                visited_status=FollowupVisitStatus.PENDING.value,
            )
            db.add(db_followup)

    db.commit()
    db.refresh(db_prescription)
    return db_prescription


def format_medicine_name(name: str, variant: Optional[str] = None, dosage_strength: Optional[str] = None) -> str:
    parts = [name]
    if variant:
        parts.append(f"({variant})")
    if dosage_strength:
        parts.append(f"({dosage_strength})")
    return " ".join(parts)


def get_medication_names(
    db: Session, 
    organization_id: str,
    branch_id: str
):
    results = (
        db.query(
            Inventory.id, 
            Product.name, 
            Product.variant, 
            Product.dosage_strength
        )
        .join(Product, Inventory.product_id == Product.id)
        .filter(
            Inventory.organization_id == organization_id,
            Inventory.branch_id == branch_id,
            Product.is_available == True
        )
        .all()
    )
    return [
        MedicationDropdownResponse(
            id=row.id,
            name=format_medicine_name(row.name, row.variant, row.dosage_strength)
        )
        for row in results
    ]


def get_followup_duration_types():
    return [
        FollowupDurationOptionResponse(
            value=duration.value,
            label=duration.label
        )
        for duration in FollowupDuration
    ]


def calculate_followup_end_time_controller(
    followup_time: Optional[time],
    followup_duration: Optional[int]
) -> Optional[time]:
    return calculate_followup_end_time(followup_time, followup_duration)