from typing import Optional
from app.Enum.PlanStatus import PlanStatus
from sqlalchemy.orm import Session
from app.model.Plan import Plan
from app.db.schemas.plan import PlanCreate, PlanUpdate
from app.core.module import MODULES
def get_plan_modules():
    module_list = []
    for key,value in MODULES.items():
        module_list.append({
            "category": key, 
            "label": value.get("label"), 
            "modules": value.get("modules")
        })
    return module_list

def get_slug(name:str):
    return name.lower().replace(" ", "-")

def publish_plan(db:Session, plan:Plan):
    if plan.status == PlanStatus.DRAFT.value:
        plan.status = PlanStatus.ACTIVE.value
        db.commit()
        db.refresh(plan)
    return plan

def toggle_plan_status(db: Session, db_plan: Plan) -> Plan:
    if db_plan.status != PlanStatus.DRAFT.value:
        if db_plan.status == PlanStatus.ACTIVE.value:
            db_plan.status = PlanStatus.INACTIVE.value
        else:
            db_plan.status = PlanStatus.ACTIVE.value

        db.commit()
        db.refresh(db_plan)
    return db_plan
        

def create_plan(db:Session, plan:PlanCreate):
    db_plan = Plan(
        name = plan.name,
        slug = get_slug(plan.name),
        monthly_price = plan.monthly_price,
        yearly_price = plan.yearly_price,
        tagline = plan.tagline,
        status = plan.status.value,
        modules = plan.modules,
        max_appointments = plan.max_appointments,
        max_patients = plan.max_patients,
        max_staff = plan.max_staff,
        max_lab_referrals = plan.max_lab_referrals,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

def get_plan(db:Session, plan_id:str):
    return db.query(Plan).filter(Plan.id == plan_id).first()

def get_plans(
    db:Session,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    query = db.query(Plan)
    if status:
        query = query.filter(Plan.status == status)
    return query.order_by(Plan.created_at.desc()).offset(skip).limit(limit).all()


def update_plan(db: Session, plan_id: str, plan: PlanUpdate):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        return None

    update_data = plan.model_dump(exclude_unset=True, mode="json")
    if "name" in update_data and update_data["name"]:
        update_data["slug"] = get_slug(update_data["name"])

    for key, value in update_data.items():
        setattr(db_plan, key, value)

    db.commit()
    db.refresh(db_plan)
    return db_plan


def delete_plan(db: Session, plan_id: str):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        return None
    db.delete(db_plan)
    db.commit()
    return db_plan

