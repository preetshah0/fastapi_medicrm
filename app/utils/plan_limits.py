from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.model.User import User
from app.model.Subscription import Subscription
from app.model.Patient import Patient, PatientLabReferral
from app.model.Appointment import Appointment
from app.model.Branch import Branch
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.utils.auth_utils import get_current_user_object
from app.utils.ApiResponse import HTTP_403_RESPONSE


def check_feature_limit(feature_name: str):
    """
    FastAPI dependency guard to enforce subscription plan limit for features:
    - max_appointments
    - max_patients
    - max_staff
    - max_lab_referrals

    If limit is -1 or None, unlimited entries are allowed.
    If current organization entry count reaches/exceeds the plan limit, blocks creation with HTTP 403.
    """
    def guard(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user_object),
    ) -> User:
        subscription = (
            db.query(Subscription)
            .filter(
                Subscription.organization_id == current_user.organization_id,
                Subscription.status == SubscriptionStatus.ACTIVE.value,
            )
            .first()
        )

        if not subscription or not subscription.plan:
            HTTP_403_RESPONSE("No active subscription plan found for your organization.")

        plan = subscription.plan
        limit = getattr(plan, feature_name, None)

        if limit is None or limit == -1:
            return current_user

        current_count = 0
        if feature_name == "max_patients":
            current_count = (
                db.query(Patient)
                .filter(Patient.organization_id == current_user.organization_id)
                .count()
            )
        elif feature_name == "max_staff":
            current_count = (
                db.query(User)
                .filter(User.organization_id == current_user.organization_id)
                .count()
            )
        elif feature_name == "max_appointments":
            current_count = (
                db.query(Appointment)
                .join(Branch, Appointment.branch_id == Branch.id)
                .filter(Branch.organization_id == current_user.organization_id)
                .count()
            )
        elif feature_name == "max_lab_referrals":
            current_count = (
                db.query(PatientLabReferral)
                .filter(PatientLabReferral.organization_id == current_user.organization_id)
                .count()
            )

        if current_count >= limit:
            label = feature_name.replace("max_", "").replace("_", " ")
            HTTP_403_RESPONSE(
                f"Feature limit exceeded. Your plan allows a maximum of {limit} {label}."
            )

        return current_user

    return guard
