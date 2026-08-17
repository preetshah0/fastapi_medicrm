from app.Enum.MasterOptionType import MasterOptionType
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from app.model.MasterOption import Master
from app.db.schemas.master_options import (
    MasterOptionCreate, 
    MasterOptionUpdate,
    MasterOptionDropdownResponse,
    MasterOptionTypeResponse,
)


def get_master_option_types():
    return [
        MasterOptionTypeResponse(value=item.value, label=item.label)
        for item in MasterOptionType
    ]




def generate_slug(name: str) -> str:
    return name.lower().replace(" ", "-")


def create_master_option(db: Session, master_option_data: MasterOptionCreate, organization_id: str) -> Master:
    slug = generate_slug(master_option_data.name)

    master_option = Master(
        organization_id=organization_id,
        type=master_option_data.type.value,
        name=master_option_data.name,
        slug=slug,
        description=master_option_data.description,
        is_active=master_option_data.is_active,
    )
    db.add(master_option)
    db.commit()
    db.refresh(master_option)
    return master_option


def get_master_options(
    db: Session, 
    organization_id: str, 
    option_type: MasterOptionType,
    is_active: bool = True,
    skip: int = 0,
    limit: int = 10
):
    return (
        db.query(Master)
        .filter(
            Master.organization_id == organization_id,
            Master.type == option_type.value,
            Master.is_active == is_active
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_master_option_by_id(db: Session, master_option_id: str, organization_id: str):
    return db.query(Master).filter(
        Master.id == master_option_id,
        Master.organization_id == organization_id
    ).first()


def update_master_option(
    db: Session, 
    master_option_id: str, 
    master_option_data: MasterOptionUpdate, 
    organization_id: str
):
    master_option = get_master_option_by_id(db, master_option_id, organization_id)

    update_data = master_option_data.model_dump(exclude_unset=True)

    if "type" in update_data and update_data["type"] is not None:
        update_data["type"] = update_data["type"].value

    if "name" in update_data and update_data["name"] is not None:
        new_slug = generate_slug(update_data["name"])
        update_data["slug"] = new_slug

    for field, value in update_data.items():
        setattr(master_option, field, value)

    db.commit()
    db.refresh(master_option)
    return master_option


def delete_master_option(db: Session, master_option_id: str, organization_id: str):
    master_option = get_master_option_by_id(db, master_option_id, organization_id)

    db.delete(master_option)
    db.commit()
    return True


def get_master_option_dropdown(
    db: Session,
    organization_id: str,
    option_type: MasterOptionType
):
    results = (
        db.query(Master.id, Master.name)
        .filter(
            Master.organization_id == organization_id,
            Master.type == option_type.value,
            Master.is_active == True
        )
        .all()
    )

    return [MasterOptionDropdownResponse(id=row.id, name=row.name) for row in results]