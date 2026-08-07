from sqlalchemy.orm import Session
from app.model.Organization import Organization
from app.model.User import User
from app.model.Role import Roles as Role
from app.model.Branch import Branch
from app.db.schemas.organization import OrganizationCreate, OrganizationUpdate
from app.Enum.OrganizationStatus import OrganizationStatus
from app.Enum.UserStatus import UserStatus
from app.utils.auth_utils import hash_password
import random

def generate_ref(title: str) -> str:
    clean_title = "".join(c for c in title if c.isalnum()).upper()
    prefix = clean_title[:3]
    if len(prefix) < 3:
        prefix = (prefix + "ORG")[:3]
    return f"{prefix}#{random.randint(1000, 9999)}"


def create_organization(db: Session, organization: OrganizationCreate, owner_role: Role) -> Organization:
    db_org = Organization(
        organization_name=organization.organization_name,
        organization_email=organization.organization_email,
        address=organization.address,
        ref=generate_ref(organization.organization_name),
        status=OrganizationStatus.ACTIVE.value,
        profile_photo=organization.profile_photo,
    )
    db.add(db_org)
  
    db_owner = User(
        name=organization.owner_name,
        email=organization.owner_email,
        password=hash_password(organization.password),
        phone=organization.owner_phone,
        specialization=organization.owner_specialization,
        role=owner_role.name,
        status=UserStatus.ACTIVE.value,
        description=organization.owner_description,
        profile_photo=organization.owner_profile_photo,
        organization_id=db_org.id,
    )

    db_owner.roles.append(owner_role)
    db.add(db_owner)

    db_branch = Branch(
        branch_name=organization.branch_name,
        address=organization.branch_address,
        phone_number=organization.branch_phone,
        branch_email=organization.branch_email,
        opening_time=organization.opening_time,
        closing_time=organization.closing_time,
        city=organization.city,
        state=organization.state,
        organization_id=db_org.id,
    )
    db.add(db_branch)
    db.commit()
    db.refresh(db_org)
    db.refresh(db_owner)
    db.refresh(db_branch)
    return db_org


def get_organization(db: Session, ref: str) -> Organization:
    db_org = db.query(Organization).filter(Organization.ref == ref).first()
    return db_org


def update_organization(db: Session, db_org: Organization, organization: OrganizationUpdate) -> Organization:
    update_data = organization.model_dump(exclude_unset=True, mode='json')

    org_fields = ["organization_name", "organization_email", "address", "status", "profile_photo"]
    for field in org_fields:
        if field in update_data and update_data[field] is not None:
            setattr(db_org, field, update_data[field])

    # # Update Owner fields if owner exists
    # db_owner = db.query(User).filter(User.organization_id == db_org.id, User.role == "owner").first()
    # if db_owner:
    #     owner_field_map = {
    #         "owner_name": "name",
    #         "owner_email": "email",
    #         "owner_phone": "phone",
    #
    #         "owner_specialization": "specialization",
    #         "owner_description": "description",
    #         "owner_profile_photo": "profile_photo",
    #     }
    #     for schema_field, model_field in owner_field_map.items():
    #         if schema_field in update_data and update_data[schema_field] is not None:
    #             setattr(db_owner, model_field, update_data[schema_field])

    db.commit()
    db.refresh(db_org)
    # if db_owner:
    #     db.refresh(db_owner)
    return db_org


def delete_organization(db: Session, db_org: Organization) -> bool:
    db.delete(db_org)
    db.commit()
    return True
