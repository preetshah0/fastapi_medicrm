import logging
from fastapi import APIRouter, Header, HTTPException, Request, Depends, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db.schemas.stripe import StripeWebhookVerifyRequest
from app.services.stripe_gateway import construct_webhook_event
from app.services.stripe_webhook_service import (
    handle_checkout_session_completed,
    handle_invoice_payment_succeeded,
    handle_invoice_payment_failed,
    handle_customer_subscription_deleted,
    handle_customer_subscription_updated,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/stripe", tags=["stripe-webhook"])


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(..., alias="Stripe-Signature"),
    db: Session = Depends(get_db),
):

    raw_payload = await request.body()

    try:
        event = construct_webhook_event(
            StripeWebhookVerifyRequest(
                payload=raw_payload,
                sig_header=stripe_signature,
            )
        )
    except Exception as e:
        logger.error(f"Stripe webhook verification failed: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid webhook signature: {str(e)}")

    event_type = event["type"]
    data_object = event["data"]["object"]

    logger.info(f"Processing Stripe Webhook event: {event_type}")

    match event_type:
        case "checkout.session.completed":
            handle_checkout_session_completed(session=data_object, db=db)

        case "invoice.payment_succeeded":
            handle_invoice_payment_succeeded(invoice=data_object, db=db)

        case "invoice.payment_failed":
            handle_invoice_payment_failed(invoice=data_object, db=db)

        case "customer.subscription.deleted":
            handle_customer_subscription_deleted(stripe_sub=data_object, db=db)

        case "customer.subscription.updated":
            handle_customer_subscription_updated(stripe_sub=data_object, db=db)

        case _:
            logger.debug(f"Unhandled Stripe webhook event: {event_type}")

    return {"status": "success"}
