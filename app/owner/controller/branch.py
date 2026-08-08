from sqlalchemy.orm import Session
from app.model.Branch import Branch, BranchUser
from app.model.User import User
from app.model.Role import Roles
from app.db.schemas.branch import BranchCreate, BranchUpdate


def create_branch(db: Session, organization_id: str, branch_data: BranchCreate):
    db_branch = Branch(
        organization_id=organization_id,
        branch_name=branch_data.branch_name,
        branch_email=branch_data.branch_email,
        phone_number=branch_data.phone_number,
        address=branch_data.address,
        status=branch_data.status.value,
        city=branch_data.city,
        state=branch_data.state,
        opening_time=branch_data.opening_time,
        closing_time=branch_data.closing_time,
    )

    db.add(db_branch)
    db.commit()
    db.refresh(db_branch)
    return db_branch


def get_branch(db: Session, branch_id: str):
    return db.query(Branch).filter(Branch.id == branch_id).first()


def get_branches_by_organization(db: Session, organization_id: str, skip: int = 0, limit: int = 10):
    return (
        db.query(Branch).filter(Branch.organization_id == organization_id).offset(skip).limit(limit).all()
    )


def update_branch(db: Session, branch_id: str, branch_data: BranchUpdate):
    db_branch = get_branch(db, branch_id)
    if not db_branch:
        return None

    update_data = branch_data.model_dump(exclude_unset=True, mode="json")
    for key, value in update_data.items():
        if key == "status" and value is not None:
            setattr(db_branch, key, value.value if hasattr(value, "value") else value)
        else:
            setattr(db_branch, key, value)

    db.commit()
    db.refresh(db_branch)
    return db_branch


def delete_branch(db: Session, branch_id: str):
    db_branch = get_branch(db, branch_id)
    if db_branch:
        db.delete(db_branch)
        db.commit()
    return True


def assign_users_to_branch(db: Session, db_branch: Branch, users_roles: list[tuple[User, Roles]], status: str = "active"):
    created_assignments = []
    for db_user, db_role in users_roles:
        existing_assignment = (
            db.query(BranchUser).filter(BranchUser.user_id == db_user.id, BranchUser.branch_id == db_branch.id).first()
        )
        if existing_assignment:
            continue
            
        user_roles = {
            "user_name": db_user.name,
            "role_name": db_role.name
        }

        assignment = BranchUser(
            branch_id=db_branch.id,
            user_id=db_user.id,
            role_id=db_role.id,
            user_roles=user_roles,
            status=status,
        )
        db.add(assignment)
        created_assignments.append(assignment)

    if created_assignments:
        db.commit()
        for assignment in created_assignments:
            db.refresh(assignment)

    return created_assignments


def get_users_by_branch(db: Session, branch_id: str, skip: int = 0, limit: int = 10):
    return db.query(BranchUser).filter(BranchUser.branch_id == branch_id).offset(skip).limit(limit).all()