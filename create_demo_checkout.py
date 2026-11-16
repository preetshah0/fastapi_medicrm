import os
import sys
from dotenv import load_dotenv

# Load .env
load_dotenv(".env")

import stripe
from app.core.config import stripe_settings, settings

stripe.api_key = stripe_settings.STRIPE_SECRET_KEY


def main():
    print("⏳ Connecting to Stripe...")
    try:
        # 1. Create a test customer
        customer = stripe.Customer.create(
            name="Demo Clinic Owner",
            email="owner@democlinic.com",
            metadata={"source": "demo_test"}
        )
        print(f"✅ Demo Customer created: {customer.id}")

        # 2. Create a test recurring price ($29/month)
        price = stripe.Price.create(
            unit_amount=2900,  # $29.00
            currency="usd",
            recurring={"interval": "month"},
            product_data={"name": "MediCRM Demo Pro Subscription"},
        )
        print(f"✅ Demo Recurring Price created: {price.id} ($29.00/month)")

        # 3. Create Checkout Session
        frontend_base = (settings.FRONT_END_URL or "http://localhost:3000").rstrip("/")
        session = stripe.checkout.Session.create(
            customer=customer.id,
            mode="subscription",
            payment_method_types=["card"],
            line_items=[{"price": price.id, "quantity": 1}],
            success_url=f"{frontend_base}/checkout/thank-you?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{frontend_base}/checkout/cancel",
            metadata={
                "demo": "true",
                "organization_id": "demo-org-123",
                "plan_id": "demo-plan-123",
                "billing_period": "monthly",
            }
        )

        print("\n" + "=" * 70)
        print("🎉 DEMO CHECKOUT URL GENERATED SUCCESSFULLY!")
        print("=" * 70)
        print(f"\n👉 Open this URL in your browser to test checkout:\n\n{session.url}\n")
        print("=" * 70)
        print("💳 Test Card : 4242 4242 4242 4242")
        print("📅 Expiry    : Any future date (e.g. 12/28)")
        print("🔒 CVC       : 123")
        print("=" * 70)

    except Exception as e:
        print(f"\n❌ Error creating checkout session: {e}")


if __name__ == "__main__":
    main()

