from typing import Optional
from decimal import Decimal
from app.Enum.BillingPeriod import BillingPeriod
from sqlalchemy.orm import Session
from app.model.Plan import Plan
from app.db.schemas.plan import PlanCreate, PlanUpdate
from app.db.schemas.stripe import (
    StripeProductCreate,
    StripeProductUpdate,
    StripePriceCreate,
    StripePriceUpdate,
)
from app.services.stripe_gateway import (
    create_product,
    update_product,
    create_price,
    update_price,
)
from app.core.module import MODULES


def get_plan_modules():
    module_list = []
    for key, value in MODULES.items():
        module_list.append({
            "category": key, 
            "label": value.get("label"), 
            "modules": value.get("modules")
        })
    return module_list


def get_slug(name: str):
    return name.lower().replace(" ", "-")


def toggle_plan_status(db: Session, db_plan: Plan) -> Plan:
    db_plan.status = not db_plan.status
    if db_plan.stripe_product_id:
        try:
            update_product(
                db_plan.stripe_product_id,
                StripeProductUpdate(active=db_plan.status),
            )
        except Exception:
            pass
    db.commit()
    db.refresh(db_plan)
    return db_plan


def create_plan(db: Session, plan: PlanCreate):
    stripe_product_id = plan.stripe_product_id
    stripe_monthly_price_id = plan.stripe_monthly_price_id
    stripe_yearly_price_id = plan.stripe_yearly_price_id

    # If Stripe product/prices are not provided, auto-create them in Stripe
    if not stripe_product_id:
        try:
            stripe_product = create_product(
                StripeProductCreate(
                    name=plan.name,
                    active=plan.status,
                    description=plan.tagline or f"{plan.name} Plan",
                    metadata={"slug": get_slug(plan.name)},
                )
            )
            stripe_product_id = stripe_product.id
        except Exception:
            pass

    if stripe_product_id:
        price_ids = {
            BillingPeriod.MONTHLY: stripe_monthly_price_id,
            BillingPeriod.YEARLY: stripe_yearly_price_id,
        }
        for period in BillingPeriod:
            price_field = f"{period.value}_price"
            price_val = getattr(plan, price_field, None)
            if not price_ids[period] and price_val is not None:
                try:
                    amount_cents = int(Decimal(str(price_val)) * 100)
                    stripe_price = create_price(
                        StripePriceCreate(
                            product_id=stripe_product_id,
                            amount_in_cents=amount_cents,
                            currency="usd",
                            interval=period.value,
                            metadata={"plan_name": plan.name, "period": period.value},
                        )
                    )
                    price_ids[period] = stripe_price.id
                except Exception:
                    pass

        stripe_monthly_price_id = price_ids[BillingPeriod.MONTHLY]
        stripe_yearly_price_id = price_ids[BillingPeriod.YEARLY]

    db_plan = Plan(
        name=plan.name,
        slug=get_slug(plan.name),
        monthly_price=plan.monthly_price,
        yearly_price=plan.yearly_price,
        tagline=plan.tagline,
        status=plan.status,
        modules=plan.modules,
        max_appointments=plan.max_appointments,
        max_patients=plan.max_patients,
        max_staff=plan.max_staff,
        max_lab_referrals=plan.max_lab_referrals,
        stripe_product_id=stripe_product_id,
        stripe_monthly_price_id=stripe_monthly_price_id,
        stripe_yearly_price_id=stripe_yearly_price_id,
    )
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan


def get_plan(db: Session, plan_id: str):
    return db.query(Plan).filter(Plan.id == plan_id).first()


def get_plans(
    db: Session,
    status: Optional[bool] = None,
    skip: int = 0,
    limit: int = 100,
):
    query = db.query(Plan)
    if status is not None:
        query = query.filter(Plan.status == status)
    return query.order_by(Plan.created_at.desc()).offset(skip).limit(limit).all()


def update_plan(db: Session, plan_id: str, plan: PlanUpdate):
    db_plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not db_plan:
        return None

    update_data = plan.model_dump(exclude_unset=True, mode="json")
    if "name" in update_data and update_data["name"]:
        update_data["slug"] = get_slug(update_data["name"])

    # Synchronize Stripe Product changes
    product_update_fields = {}
    if "name" in update_data:
        product_update_fields["name"] = update_data["name"]
    if "tagline" in update_data:
        product_update_fields["description"] = update_data["tagline"]
    if "status" in update_data and update_data["status"] is not None:
        product_update_fields["active"] = update_data["status"]

    if db_plan.stripe_product_id:
        if product_update_fields:
            try:
                update_product(
                    db_plan.stripe_product_id,
                    StripeProductUpdate(**product_update_fields),
                )
            except Exception:
                pass
    elif not db_plan.stripe_product_id:
        # Auto-provision Stripe product if missing
        try:
            prod_name = plan.name or db_plan.name
            prod_status = plan.status if plan.status is not None else db_plan.status
            prod_tagline = plan.tagline if plan.tagline is not None else db_plan.tagline
            stripe_prod = create_product(
                StripeProductCreate(
                    name=prod_name,
                    active=prod_status,
                    description=prod_tagline or f"{prod_name} Plan",
                    metadata={"slug": get_slug(prod_name)},
                )
            )
            db_plan.stripe_product_id = stripe_prod.id
        except Exception:
            pass

    # Synchronize price changes in Stripe using BillingPeriod enum
    if db_plan.stripe_product_id:
        for period in BillingPeriod:
            price_field = f"{period.value}_price"
            stripe_price_id_field = f"stripe_{period.value}_price_id"

            if price_field in update_data and update_data[price_field] is not None:
                new_price = Decimal(str(update_data[price_field]))
                old_price = getattr(db_plan, price_field)

                if new_price != old_price:
                    try:
                        amount_cents = int(new_price * 100)
                        stripe_price = create_price(
                            StripePriceCreate(
                                product_id=db_plan.stripe_product_id,
                                amount_in_cents=amount_cents,
                                currency="usd",
                                interval=period.value,
                                metadata={"plan_name": db_plan.name, "period": period.value},
                            )
                        )
                        old_price_id = getattr(db_plan, stripe_price_id_field)
                        if old_price_id:
                            try:
                                update_price(old_price_id, StripePriceUpdate(active=False))
                            except Exception:
                                pass
                        setattr(db_plan, stripe_price_id_field, stripe_price.id)
                    except Exception:
                        pass

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

