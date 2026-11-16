from fastapi.params import Depends
from sqlalchemy.orm import Session
from app.model.Patient import Patient, Note, Report, PatientLabReferral, TestRequired
from app.model.Organization import Organization
from app.model.User import User
from app.model.Branch import Branch
from app.model.Laboratory import Laboratory
from app.Enum.LabReferralPriority import LabReferralPriority
from app.Enum.LaboratoryFacilityType import LaboratoryFacilityType
from app.db.schemas.patient import (
    NoteCreate, NoteUpdate, ReportCreate, ReportUpdate, PatientCreate, PatientUpdate,
    PatientLabReferralCreate, PatientLabReferralUpdate, ReportDropdownResponse, LabReferralPriorityOptionResponse
)
from app.db.schemas.branch import BranchDropdownResponse
from app.db.schemas.user import UserDropdownResponse
from app.db.schemas.labs import LabDropdownResponse
from app.utils.auth_utils import get_current_user_id


def generate_patient_ref(db: Session, organization_id: str, organization_name: str, patient_name: str) -> str:
    count = db.query(Patient).filter(Patient.organization_id == organization_id).count()
    next_number = count + 1

    org_prefix = organization_name[:3].upper().ljust(3, 'X') if organization_name else "ORG"

    words = patient_name.strip().split()
    if len(words) >= 2:
        name_initials = (words[0][0] + words[1][0]).upper()
    elif len(words) == 1 and len(words[0]) >= 2:
        name_initials = words[0][:2].upper()
    elif len(words) == 1:
        name_initials = (words[0][0] + "X").upper()
    else:
        name_initials = "XX"

    return f"PAT-{org_prefix}-{name_initials}-{next_number}"


def create_patient(db: Session, patient: PatientCreate):
    org = db.query(Organization).filter(Organization.id == patient.organization_id).first()
    if not org:
        return None

    ref_code = generate_patient_ref(
        db=db,
        organization_id=org.id,
        organization_name=org.organization_name,
        patient_name=patient.name
    )

    db_patient = Patient(
        organization_id=patient.organization_id,
        name=patient.name,
        ref_code=ref_code,
        email=patient.email,
        phone=patient.phone,
        age=patient.age,
        gender=patient.gender,
        blood_group=patient.blood_group,
        address=patient.address,
        description=patient.description,
        profile_photo=patient.profile_photo,
    )

    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)

    return db_patient


def get_patient_by_id(db: Session, patient_id: str):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_patients_by_organization(db: Session, organization_id: str):
    org = db.query(Organization).filter(Organization.id == organization_id).first()
    if not org:
        return None
    return db.query(Patient).filter(Patient.organization_id == organization_id).all()


def get_patient(db: Session, ref_code: str):
    return db.query(Patient).filter(Patient.ref_code == ref_code).first()


def get_all_patients(db: Session):
    return db.query(Patient).all()


def update_patient(db: Session, patient_id: str, patient: PatientUpdate):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        return None

    update_data = patient.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        setattr(db_patient, key, value)

    db.commit()
    db.refresh(db_patient)
    return db_patient


def delete_patient(db: Session, patient_id: str):
    db_patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not db_patient:
        return None
    db.delete(db_patient)
    db.commit()
    return db_patient


def create_report(db: Session, report: ReportCreate):
    patient = db.query(Patient).filter(Patient.id == report.patient_id).first()
    if not patient:
        return None

    db_report = Report(
        patient_id=report.patient_id,
        report_type=report.report_type,
        attachment=report.attachment,
        notes=report.notes,
        report_date=report.report_date,
    )
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report


def get_report(db: Session, report_id: str):
    return db.query(Report).filter(Report.id == report_id).first()


def get_reports_by_patient(db: Session, patient_id: str):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None
    return db.query(Report).filter(Report.patient_id == patient_id).all()


def get_all_reports(db: Session):
    return db.query(Report).all()


def update_report(db: Session, report_id: str, report: ReportUpdate):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        return None

    update_data = report.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        setattr(db_report, key, value)

    db.commit()
    db.refresh(db_report)
    return db_report


def delete_report(db: Session, report_id: str):
    db_report = db.query(Report).filter(Report.id == report_id).first()
    if not db_report:
        return None
    db.delete(db_report)
    db.commit()
    return db_report


def create_note(db: Session, note: NoteCreate, user_id: str = Depends(get_current_user_id)):
    patient = db.query(Patient).filter(Patient.id == note.patient_id).first()
    if not patient:
        return None

    user = db.query(User).filter(User.id == user_id).first()
    written_by = user.name if user else None

    db_note = Note(
        patient_id=note.patient_id,
        user_id=user_id,
        notes=note.notes,
        note_date=note.note_date,
        written_by=written_by,
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_note(db: Session, note_id: str):
    return db.query(Note).filter(Note.id == note_id).first()


def get_all_notes(db: Session, user_id: str):
    return db.query(Note).filter(Note.user_id == user_id).all()


def get_notes_by_patient(db: Session, patient_id: str):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        return None
    return db.query(Note).filter(Note.patient_id == patient_id).all()


def update_note(db: Session, note_id: str, note: NoteUpdate):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None

    update_data = note.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        setattr(db_note, key, value)

    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: str):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        return None
    db.delete(db_note)
    db.commit()
    return db_note


def get_branch_dropdown(db: Session, organization_id: str):
    results = (
        db.query(Branch.id, Branch.branch_name)
        .filter(Branch.organization_id == organization_id)
        .all()
    )
    return [
        BranchDropdownResponse(id=row.id, branch_name=row.branch_name)
        for row in results
    ]


def get_priority_enum():
    return [
        LabReferralPriorityOptionResponse(value=item.value, label=item.label)
        for item in LabReferralPriority
    ]


def get_report_dropdown(db: Session, patient_id: str):
    results = (
        db.query(Report.id, Report.report_type)
        .filter(Report.patient_id == patient_id)
        .all()
    )
    return [
        ReportDropdownResponse(id=row.id, report_type=row.report_type)
        for row in results
    ]


def get_user_dropdown(db: Session, organization_id: str):
    results = (
        db.query(User.id, User.name)
        .filter(User.organization_id == organization_id)
        .all()
    )
    return [
        UserDropdownResponse(id=row.id, name=row.name)
        for row in results
    ]


def get_lab_dropdown(db: Session, organization_id: str):
    results = (
        db.query(Laboratory.id, Laboratory.name)
        .filter(
            Laboratory.organization_id == organization_id,
            Laboratory.facility_type == LaboratoryFacilityType.EXTERNAL.value
        )
        .all()
    )
    return [
        LabDropdownResponse(id=row.id, name=row.name)
        for row in results
    ]


def generate_lab_referral_ref_no(db: Session, patient_id: str) -> str:
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    patient_ref = patient.ref_code if (patient and patient.ref_code) else "PAT"

    count = db.query(PatientLabReferral).filter(PatientLabReferral.patient_id == patient_id).count()
    next_number = count + 1
    return f"{patient_ref}-REF-{next_number}"


def create_patient_lab_referral(db: Session, referral_data: PatientLabReferralCreate):
    branch = db.query(Branch).filter(Branch.id == referral_data.branch_id).first()
    doctor = db.query(User).filter(User.id == referral_data.doctor_id).first()

    db_referral = PatientLabReferral(
        organization_id=branch.organization_id,
        branch_id=referral_data.branch_id,
        doctor_id=referral_data.doctor_id,
        patient_id=referral_data.patient_id,
        ref_no=generate_lab_referral_ref_no(db, referral_data.patient_id),
        referred_by=doctor.name if doctor else "Doctor",
        clinical_notes=referral_data.clinical_notes,
        report_id=referral_data.report_id,
        special_instructions=referral_data.special_instructions,
        lab_id=referral_data.lab_id,
        priority=referral_data.priority.value,
    )

    db.add(db_referral)
    db.flush()

    if referral_data.tests_required:
        tests_to_add = []
        for test in referral_data.tests_required:
            tests_to_add.append(
                TestRequired(
                    referral_id=db_referral.id,
                    test_name=test.test_name,
                    test_code=test.test_code,
                    test_description=test.test_description,
                    attachments=test.attachments,
                )
            )
        db.add_all(tests_to_add)

    db.commit()
    db.refresh(db_referral)
    return db_referral


def get_patient_lab_referral_by_id(db: Session, referral_id: str):
    return db.query(PatientLabReferral).filter(PatientLabReferral.id == referral_id).first()


def get_patient_lab_referrals_by_patient(db: Session, patient_id: str):
    return db.query(PatientLabReferral).filter(PatientLabReferral.patient_id == patient_id).all()


def get_patient_lab_referrals_by_organization(db: Session, organization_id: str):
    return db.query(PatientLabReferral).filter(PatientLabReferral.organization_id == organization_id).all()


