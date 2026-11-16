from datetime import datetime, timezone
from decimal import Decimal
from sqlalchemy.orm import Session

from app.model.Subscription import Subscription
from app.model.Payment import Payment
from app.model.Plan import Plan
from app.Enum.SubscriptionStatus import SubscriptionStatus
from app.Enum.AutoRenew import AutoRenew
from app.Enum.PaymentStatus import PaymentStatus
from app.Enum.PaymentMode import PaymentMode
from app.Enum.PaymentProvider import PaymentProvider
from app.owner.controller.subscription import generate_subscription_reference
from app.owner.controller.payment import generate_payment_reference
from app.services.stripe_gateway import retrieve_subscription


def handle_checkout_session_completed(session: dict, db: Session):
    session_id = session.get("id")
    stripe_sub_id = session.get("subscription")
    metadata = session.get("metadata", {}) or {}

    organization_id = metadata.get("organization_id")
    plan_id = metadata.get("plan_id")
    billing_period = metadata.get("billing_period", "monthly")

    if not organization_id or not plan_id:
        return False

    existing_sub = (
        db.query(Subscription)
        .filter(Subscription.stripe_checkout_session_id == session_id)
        .first()
    )
    if existing_sub:
        return existing_sub

    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    amount_total = Decimal(str(session.get("amount_total", 0) / 100))
    currency = (session.get("currency") or "USD").upper()

    end_date = None
    if stripe_sub_id:
        try:
            stripe_sub = retrieve_subscription(stripe_sub_id)
            period_end = stripe_sub.get("current_period_end")
            if period_end:
                end_date = datetime.fromtimestamp(period_end, tz=timezone.utc).replace(tzinfo=None)
        except Exception:
            pass

    # Deactivate existing active subscriptions so only the newest purchased subscription is ACTIVE
    db.query(Subscription).filter(
        Subscription.organization_id == organization_id,
        Subscription.status == SubscriptionStatus.ACTIVE.value,
    ).update({"status": SubscriptionStatus.INACTIVE.value}, synchronize_session=False)

    sub_ref = generate_subscription_reference(db)
    subscription = Subscription(
        subscription_reference=sub_ref,
        organization_id=organization_id,
        plan_id=plan_id,
        start_date=datetime.now(),
        end_date=end_date,
        total_billing_amount=amount_total,
        currency=currency,
        billing_period=billing_period,
        status=SubscriptionStatus.ACTIVE.value,
        stripe_subscription_id=stripe_sub_id,
        stripe_checkout_session_id=session_id,
    )
    db.add(subscription)
    db.flush()

    session_payment_status = session.get("payment_status")
    is_paid = session_payment_status == "paid"
    payment_status = PaymentStatus.PAID.value if is_paid else PaymentStatus.PROCESSING.value
    paid_at = datetime.now() if is_paid else None

    payment = Payment(
        organization_id=organization_id,
        subscription_id=subscription.id,
        amount=amount_total,
        currency=currency,
        payment_mode=PaymentMode.GATEWAY.value,
        provider=PaymentProvider.STRIPE.value,
        provider_payment_id=session_id,
        provider_invoice_id=session.get("invoice"),
        paid_at=paid_at,
        status=payment_status,
        reference_no=generate_payment_reference(),
        notes=f"Initial subscription payment for {plan.name if plan else 'Plan'}",
    )
    db.add(payment)
    db.commit()
    db.refresh(subscription)
    db.refresh(payment)

    return subscription


def handle_invoice_payment_succeeded(invoice: dict, db: Session):
    invoice_id = invoice.get("id")
    stripe_sub_id = invoice.get("subscription")
    billing_reason = invoice.get("billing_reason")

    if billing_reason == "subscription_create":
        return False

    if not stripe_sub_id:
        return False

    subscription = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )
    if not subscription:
        return False

    existing_payment = db.query(Payment).filter(Payment.provider_invoice_id == invoice_id).first()
    if existing_payment:
        if existing_payment.status != PaymentStatus.PAID.value:
            existing_payment.status = PaymentStatus.PAID.value
            existing_payment.paid_at = datetime.now()
            db.commit()
        return existing_payment

    amount_paid = Decimal(str(invoice.get("amount_paid", 0) / 100))
    currency = (invoice.get("currency") or "USD").upper()

    lines = invoice.get("lines", {}).get("data", [])
    if lines:
        period_end = lines[0].get("period", {}).get("end")
        if period_end:
            subscription.end_date = datetime.fromtimestamp(period_end, tz=timezone.utc).replace(tzinfo=None)
            subscription.status = SubscriptionStatus.ACTIVE.value

    payment = Payment(
        organization_id=subscription.organization_id,
        subscription_id=subscription.id,
        amount=amount_paid,
        currency=currency,
        payment_mode=PaymentMode.GATEWAY.value,
        provider=PaymentProvider.STRIPE.value,
        provider_payment_id=invoice.get("payment_intent"),
        provider_invoice_id=invoice_id,
        paid_at=datetime.now(),
        status=PaymentStatus.PAID.value,
        reference_no=generate_payment_reference(),
        notes="Recurring subscription renewal payment",
    )
    db.add(payment)
    db.commit()

    return payment


def handle_invoice_payment_failed(invoice: dict, db: Session):
    stripe_sub_id = invoice.get("subscription")
    if not stripe_sub_id:
        return False

    subscription = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )
    if not subscription:
        return False

    amount_due = Decimal(str(invoice.get("amount_due", 0) / 100))
    currency = (invoice.get("currency") or "USD").upper()

    payment = Payment(
        organization_id=subscription.organization_id,
        subscription_id=subscription.id,
        amount=amount_due,
        currency=currency,
        payment_mode=PaymentMode.GATEWAY.value,
        provider=PaymentProvider.STRIPE.value,
        provider_payment_id=invoice.get("payment_intent"),
        provider_invoice_id=invoice.get("id"),
        status=PaymentStatus.FAILED.value,
        reference_no=generate_payment_reference(),
        notes="Recurring renewal payment failed",
    )
    db.add(payment)
    db.commit()
    return payment


def handle_customer_subscription_deleted(stripe_sub: dict, db: Session):
    stripe_sub_id = stripe_sub.get("id")
    if not stripe_sub_id:
        return False

    subscription = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )
    if not subscription:
        return False

    subscription.status = SubscriptionStatus.CANCELLED.value
    subscription.auto_renew = AutoRenew.INACTIVE.value
    subscription.cancelled_at = datetime.now()
    subscription.end_date = datetime.now()
    db.commit()
    return subscription


def handle_customer_subscription_updated(stripe_sub: dict, db: Session):
    stripe_sub_id = stripe_sub.get("id")
    if not stripe_sub_id:
        return False

    subscription = (
        db.query(Subscription)
        .filter(Subscription.stripe_subscription_id == stripe_sub_id)
        .first()
    )
    if not subscription:
        return False

    # Sync auto_renew setting
    cancel_at_period_end = stripe_sub.get("cancel_at_period_end", False)
    subscription.auto_renew = (
        AutoRenew.INACTIVE.value if cancel_at_period_end else AutoRenew.ACTIVE.value
    )

    # Sync period end date
    period_end = stripe_sub.get("current_period_end")
    if period_end:
        subscription.end_date = datetime.fromtimestamp(period_end, tz=timezone.utc).replace(tzinfo=None)

    # Sync status
    stripe_status = stripe_sub.get("status")
    if stripe_status == "active" and subscription.status != SubscriptionStatus.CANCELLED.value:
        subscription.status = SubscriptionStatus.ACTIVE.value
    elif stripe_status in ("canceled", "cancelled", "incomplete_expired"):
        subscription.status = SubscriptionStatus.CANCELLED.value
        subscription.auto_renew = AutoRenew.INACTIVE.value
        subscription.cancelled_at = datetime.now()  

    db.commit()
    db.refresh(subscription)
    return subscription


def handle_payment_intent_processing(payment_intent: dict, db: Session):
    pi_id = payment_intent.get("id")
    if not pi_id:
        return False

    invoice_id = payment_intent.get("invoice")
    payment = (
        db.query(Payment)
        .filter(
            (Payment.provider_payment_id == pi_id) | (Payment.provider_invoice_id == invoice_id)
        )
        .first()
    )
    if payment and payment.status != PaymentStatus.PAID.value:
        payment.status = PaymentStatus.PROCESSING.value
        db.commit()
        return payment
    return False


def handle_payment_intent_canceled(payment_intent: dict, db: Session):
    pi_id = payment_intent.get("id")
    if not pi_id:
        return False

    invoice_id = payment_intent.get("invoice")
    payment = (
        db.query(Payment)
        .filter(
            (Payment.provider_payment_id == pi_id) | (Payment.provider_invoice_id == invoice_id)
        )
        .first()
    )
    if payment and payment.status != PaymentStatus.PAID.value:
        payment.status = PaymentStatus.CANCELLED.value
        db.commit()
        return payment
    return False
