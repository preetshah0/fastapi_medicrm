from sqlalchemy.orm import Session
from app.model.laboratories import Laboratory, LabVisit
from app.model.Branch import Branch
from app.db.schemas.labs import LabCreate, LabUpdate, LabVisitCreate
from app.Enum.LaboratoryFacilityType import LaboratoryFacilityType

def create_laboratory(db: Session, branch_id: str, lab_data: LabCreate):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None
        
    laboratory = Laboratory(
        organization_id=branch.organization_id,
        branch_id=branch_id,
        name=lab_data.name,
        contact_person=lab_data.contact_person,
        facility_type=lab_data.facility_type.value,
        lab_type=lab_data.lab_type.value,
        address=lab_data.address,
        city=lab_data.city,
        pincode=lab_data.pincode,
        phone_number=lab_data.phone_number,
        email=lab_data.email,
        notes=lab_data.notes,
        status=lab_data.status.value,
    )
    db.add(laboratory)
    db.commit()
    db.refresh(laboratory)
    return laboratory

def get_laboratories_by_branch(db: Session, branch_id: str):
    return db.query(Laboratory).filter(Laboratory.branch_id == branch_id).all()

def get_laboratory(db: Session, lab_id: str):
    return db.query(Laboratory).filter(Laboratory.id == lab_id).first()

def update_laboratory(db: Session, lab_id: str, lab_data: LabUpdate):
    db_lab = get_laboratory(db, lab_id)
    if not db_lab:
        return None
        
    update_data = lab_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if hasattr(value, "value"):  
            setattr(db_lab, field, value.value)
        else:
            setattr(db_lab, field, value)
            
    db.commit()
    db.refresh(db_lab)
    return db_lab

def delete_laboratory(db: Session, lab_id: str):
    db_lab = get_laboratory(db, lab_id)
    if not db_lab:
        return None
    db.delete(db_lab)
    db.commit()
    return True

def create_lab_visit(db: Session, lab_id: str, visit_data: LabVisitCreate):
    laboratory = get_laboratory(db, lab_id)
    if not laboratory:
        return None

    lab_visit = LabVisit(
        lab_id=lab_id,
        visited_date=visit_data.visited_date,
        visit_time=visit_data.visit_time,
        name=visit_data.name,
        email=visit_data.email,
        speciality=visit_data.speciality,
        from_facility=visit_data.from_facility,
        notes=visit_data.notes,
    )
    
    db.add(lab_visit)
    db.commit()
    db.refresh(lab_visit)
    return lab_visit

def get_lab_visits(db: Session, lab_id: str):
    return db.query(LabVisit).filter(LabVisit.lab_id == lab_id).all()
