from sqlalchemy.orm import Session
from app.model.Supplier import Supplier, SupplierVisit
from app.model.Branch import Branch
from app.model.MedicalRep import MedicalReps
from app.db.schemas.suppliers import SupplierCreate, SupplierUpdate, SupplierVisitCreate
from app.Enum.SupplierType import SupplierType

def create_supplier(db: Session, branch_id: str, supplier_data: SupplierCreate):
    branch = db.query(Branch).filter(Branch.id == branch_id).first()
    if not branch:
        return None
    
    if supplier_data.type == SupplierType.MEDICAL_REPRESENTATIVE:
        if not supplier_data.reps_id:
            return None
        
        db_reps = db.query(MedicalReps).filter(MedicalReps.id == supplier_data.reps_id).first()
        if not db_reps:
            return None
            
        supplier = Supplier(
            organization_id=branch.organization_id,
            branch_id=branch_id,
            type=supplier_data.type.value,
            reps_id=supplier_data.reps_id,
            company=db_reps.company_name,
            email=db_reps.company_email,
            phone=db_reps.company_phone,
            notes=supplier_data.notes,
        )
    else:
        supplier = Supplier(
            organization_id=branch.organization_id,
            branch_id=branch_id,
            type=supplier_data.type.value,
            reps_id=None,
            company=supplier_data.company,
            email=supplier_data.email,
            phone=supplier_data.phone,
            notes=supplier_data.notes,
        )        
        
    db.add(supplier)
    db.commit()
    db.refresh(supplier)
    return supplier

def get_suppliers(db: Session,supplier_id:str):
    if not supplier_id:
        return None
    return db.query(Supplier).filter(Supplier.id == supplier_id).first()

def get_suppliers_by_branch(db: Session,branch_id:str):
    if not branch_id:
        return None
    return db.query(Supplier).filter(Supplier.branch_id == branch_id).all()

def update_supplier(db: Session,supplier_id:str, supplier_data: SupplierUpdate):
    db_supplier = get_suppliers(db,supplier_id)
    if not db_supplier:
        return None
    
    update_data = supplier_data.model_dump(exclude_unset=True)
    
    if db_supplier.type == SupplierType.MEDICAL_REPRESENTATIVE.value:
        reps_id = update_data.get("reps_id", db_supplier.reps_id)
        if reps_id:
            db_reps = db.query(MedicalReps).filter(MedicalReps.id == reps_id).first()
            if db_reps:
                update_data["company"] = db_reps.company_name
                update_data["email"] = db_reps.company_email
                update_data["phone"] = db_reps.company_phone
                update_data["reps_id"] = reps_id

    for field, value in update_data.items():
        setattr(db_supplier, field, value)
        
    db.commit()
    db.refresh(db_supplier)
    return db_supplier

def delete_supplier(db: Session,supplier_id:str):
    db_supplier = get_suppliers(db,supplier_id)
    if not db_supplier:
        return None
    db.delete(db_supplier)
    db.commit()
    return True

import uuid

def create_supplier_visit(db: Session, supplier_id: str, visit_data: SupplierVisitCreate):
    db_supplier = get_suppliers(db, supplier_id)
    if not db_supplier:
        return None
        
    batch_num = generate_supplier_batch_number(db)
    
    if visit_data.supplier_name:
        supplier_name= visit_data.supplier_name
    else:
        supplier_name= db_supplier.company
    
    new_visit = SupplierVisit(
        supplier_id=supplier_id,
        supplier_name=supplier_name,
        visited_date=visit_data.visited_date,
        batch_number=batch_num,
        visit_purpose=visit_data.visit_purpose.value,
        notes=visit_data.notes
    )
    
    db.add(new_visit)
    db.commit()
    db.refresh(new_visit)
    return new_visit

def get_supplier_visits(db: Session, supplier_id: str):
    if not supplier_id:
        return None
    return db.query(SupplierVisit).filter(SupplierVisit.supplier_id == supplier_id).all()

def generate_supplier_batch_number(db: Session) -> str:
    from datetime import datetime
    today = datetime.now()
    today_str = today.strftime("%Y%m%d")
    unique_suffix = uuid.uuid4().hex[:4].upper()
    return f"BATCH-{today_str}-{unique_suffix}"
