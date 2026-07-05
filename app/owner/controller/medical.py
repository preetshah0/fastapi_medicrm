from sqlalchemy.orm import Session
from app.model.medical_reps import MedicalReps, MedicalRepVisit
from app.model.Branch import Branch
from app.db.schemas.medical_reps import MedicalRepsCreate, MedicalRepsUpdate, MedicalRepVisitCreate

def create_medical_representatives(db: Session, branch_id: str, medical_rep_data: MedicalRepsCreate):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None

    db_medical_rep = MedicalReps(
        branch_id=branch_id,
        organization_id=branch.organization_id,
        reps_name=medical_rep_data.reps_name,
        reps_email=medical_rep_data.reps_email,
        reps_phone=medical_rep_data.reps_phone,
        notes=medical_rep_data.notes,
        reps_profile_photo=medical_rep_data.reps_profile_photo,
        company_name=medical_rep_data.company_name,
        city=medical_rep_data.city,
    )
    
    db.add(db_medical_rep)
    db.commit()
    db.refresh(db_medical_rep)
    return db_medical_rep

def create_mr_visit(db: Session, medical_rep_id: str, mr_visit_data: MedicalRepVisitCreate):
    db_mr_visit = MedicalRepVisit(
        reps_id=medical_rep_id,
        visited_date=mr_visit_data.visited_date,
        notes=mr_visit_data.notes,
        visit_purpose=mr_visit_data.visit_purpose,
        product=mr_visit_data.product,
    )
    
    db.add(db_mr_visit)
    db.commit()
    db.refresh(db_mr_visit)
    return db_mr_visit
    

def update_medical_representatives(db: Session, medical_rep_id: str, medical_rep_data: MedicalRepsUpdate):
    db_medical_rep = db.query(MedicalReps).filter(MedicalReps.id == medical_rep_id).first()
    if not db_medical_rep:
        return None
    
    update_data = medical_rep_data.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        setattr(db_medical_rep, key, value)
    
    db.commit()
    db.refresh(db_medical_rep)
    return db_medical_rep

def delete_medical_representatives(db: Session, medical_rep_id: str):
    db_medical_rep = db.query(MedicalReps).filter(MedicalReps.id == medical_rep_id).first()
    if not db_medical_rep:
        return None
    
    db.delete(db_medical_rep)
    db.commit()
    return True
    
def get_medical_representatives(db: Session, branch_id: str):
    return db.query(MedicalReps).filter(MedicalReps.branch_id == branch_id).all()

def get_product(db: Session, medical_rep_id: str):
    mr = db.query(MedicalReps).filter(MedicalReps.id == medical_rep_id).first()
    if not mr or not mr.company_name:
        return None
    company_reps = db.query(MedicalReps.id).filter(MedicalReps.company_name == mr.company_name).subquery()
    products = db.query(MedicalRepVisit.product).filter(
        MedicalRepVisit.reps_id.in_(company_reps),
        MedicalRepVisit.product.isnot(None)
    ).distinct().all()
    if not products:
        return None
    result = []
    for p in products:
        if p[0]:
            result.append(p[0])
    return result   

def get_mr_visit(db: Session, medical_rep_id: str):
    return db.query(MedicalRepVisit).filter(MedicalRepVisit.reps_id == medical_rep_id).all()