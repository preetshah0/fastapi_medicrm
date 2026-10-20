import stripe
from app.core.config import stripe_settings
from app.db.schemas.stripe import (
    StripeCustomerCreate,
    StripeProductCreate,
    StripeProductUpdate,
    StripePriceCreate,
    StripePriceUpdate,
    StripeCheckoutSessionCreate,
    StripeCancelSubscriptionRequest,
    StripePortalCreate,
    StripeWebhookVerifyRequest,
)

stripe.api_key = stripe_settings.STRIPE_SECRET_KEY

def create_product(payload: StripeProductCreate):
    """Create a Stripe Product for a plan."""
    params = {
        "name": payload.name,
        "active": payload.active,
        "metadata": payload.metadata or {},
    }
    if payload.description:
        params["description"] = payload.description
    return stripe.Product.create(**params)

def update_product(product_id: str, payload: StripeProductUpdate):
    """Update an existing Stripe Product for a plan."""
    params = {}
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        match key:
            case "name":
                params["name"] = value
            case "active":
                params["active"] = value
            case "description":
                params["description"] = value
            case "metadata":
                params["metadata"] = value
    return stripe.Product.modify(product_id, **params)

def create_price(payload: StripePriceCreate):
    """Create a recurring Stripe Price for a product."""
    return stripe.Price.create(
        product=payload.product_id,
        unit_amount=payload.amount_in_cents,
        currency=payload.currency.lower(),
        recurring={"interval": payload.interval},
        metadata=payload.metadata or {},
    )

def update_price(price_id: str, payload: StripePriceUpdate):
    """Update a Stripe Price (e.g. archive it by setting active=False)."""
    params = {}
    for key, value in payload.model_dump(exclude_unset=True).items():
        if value is None:
            continue
        match key:
            case "active":
                params["active"] = value
            case "metadata":
                params["metadata"] = value
    return stripe.Price.modify(price_id, **params)

def create_customer(payload: StripeCustomerCreate):
    """Create a Stripe Customer for an organization."""
    return stripe.Customer.create(
        name=payload.name,
        email=payload.email,
        metadata=payload.metadata or {},
    )


def get_customer(customer_id: str):
    """Retrieve a Stripe Customer by ID."""
    return stripe.Customer.retrieve(customer_id)



def create_checkout_session(payload: StripeCheckoutSessionCreate):
    """Create a Stripe Checkout Session for subscription purchase."""
    return stripe.checkout.Session.create(
        customer=payload.customer_id,
        payment_method_types=["card"],
        line_items=[{"price": payload.price_id, "quantity": 1}],
        mode="subscription",
        success_url=payload.success_url,
        cancel_url=payload.cancel_url,
        metadata=payload.metadata or {},
    )


def retrieve_checkout_session(session_id: str):
    """Retrieve a Stripe Checkout Session by ID."""
    return stripe.checkout.Session.retrieve(session_id)


def retrieve_subscription(subscription_id: str):
    """Retrieve a Stripe Subscription by ID."""
    return stripe.Subscription.retrieve(subscription_id)


def cancel_subscription(payload: StripeCancelSubscriptionRequest):
    """Cancel a subscription immediately or at period end."""
    if payload.at_period_end:
        return stripe.Subscription.modify(
            payload.subscription_id,
            cancel_at_period_end=True,
        )
    return stripe.Subscription.delete(payload.subscription_id)


def create_billing_portal_session(payload: StripePortalCreate):
    """Create a Customer Portal session for the organization owner."""
    return stripe.billing_portal.Session.create(
        customer=payload.customer_id,
        return_url=payload.return_url,
    )


def construct_webhook_event(payload: StripeWebhookVerifyRequest):
    """Verify and construct a Stripe webhook event from the raw payload and signature."""
    return stripe.Webhook.construct_event(
        payload=payload.payload,
        sig_header=payload.sig_header,
        secret=stripe_settings.STRIPE_WEBHOOK_SECRET,
    )
