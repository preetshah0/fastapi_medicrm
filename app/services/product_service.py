from decimal import Decimal
from typing import Optional
from app.db.schemas.products import (
    ProductUnitQuantitiesResponse,
    ProductTierPricesResponse,
    SuggestedBatchPricingResponse,
)


def calculate_unit_quantities(
    initial_outer_qty: int,
    packs_per_outer: int = 1,
    conversion_factor: int = 1
) -> ProductUnitQuantitiesResponse:
    strips_per_box = max(1, packs_per_outer or 1)
    tabs_per_strip = max(1, conversion_factor or 1)

    total_subpacks = initial_outer_qty * strips_per_box
    total_base_units = total_subpacks * tabs_per_strip

    quantities = ProductUnitQuantitiesResponse(
        subpack_qty=total_subpacks,
        base_unit_qty=total_base_units,
    )
    return quantities


def calculate_tier_selling_prices(
    base_unit_sp: Decimal,
    conversion_factor: int = 1,
    packs_per_outer: int = 1
) -> ProductTierPricesResponse:
    tabs_per_strip = max(1, conversion_factor or 1)
    strips_per_box = max(1, packs_per_outer or 1)

    base_sp = Decimal(str(base_unit_sp or 0))

    subpack_sp = round(base_sp * Decimal(str(tabs_per_strip)), 2)
    pack_sp = round(subpack_sp * Decimal(str(strips_per_box)), 2)

    tier_prices = ProductTierPricesResponse(
        subpack_sp=subpack_sp,
        pack_sp=pack_sp,
    )
    return tier_prices


def calculate_suggested_batch_pricing(
    batch_cost_price: Decimal,
    outer_box_qty: int,
    packs_per_outer: int = 1,
    conversion_factor: int = 1
) -> SuggestedBatchPricingResponse:
    quantities = calculate_unit_quantities(
        initial_outer_qty=outer_box_qty,
        packs_per_outer=packs_per_outer,
        conversion_factor=conversion_factor
    )

    total_base_units = quantities.base_unit_qty
    total_subpacks = quantities.subpack_qty
    total_cost = Decimal(str(batch_cost_price or 0))

    if total_base_units > 0 and total_cost > 0:
        base_unit_cost = round(total_cost / Decimal(str(total_base_units)), 4)
        subpack_cost = round(base_unit_cost * Decimal(str(conversion_factor or 1)), 2)
        pack_cost = round(subpack_cost * Decimal(str(packs_per_outer or 1)), 2)
    else:
        base_unit_cost = Decimal("0.00")
        subpack_cost = Decimal("0.00")
        pack_cost = Decimal("0.00")

    batch_pricing = SuggestedBatchPricingResponse(
        total_subpacks=total_subpacks,
        total_base_units=total_base_units,
        base_unit_cost=base_unit_cost,
        subpack_cost=subpack_cost,
        pack_cost=pack_cost,
    )
    return batch_pricing


def calculate_base_units_to_deduct(
    quantity: int,
    sale_unit: str,
    conversion_factor: int = 1,
    packs_per_outer: int = 1
) -> int:
    strips_per_box = max(1, packs_per_outer or 1)
    tabs_per_strip = max(1, conversion_factor or 1)
    tablets_per_box = strips_per_box * tabs_per_strip

    unit_key = (sale_unit or "unit").lower()

    if unit_key == "outer":
        deduct_qty = quantity * tablets_per_box
    elif unit_key in ("inner", "subpack"):
        deduct_qty = quantity * tabs_per_strip
    else:
        deduct_qty = quantity

    return deduct_qty


def calculate_sale_row_total(
    quantity: int,
    unit_price: Decimal,
    discount: Decimal = Decimal("0.00")
) -> Decimal:
    price = Decimal(str(unit_price or 0))
    disc = Decimal(str(discount or 0))
    qty = Decimal(str(quantity or 0))

    total = (qty * price) - disc
    final_total = max(Decimal("0.00"), round(total, 2))
    return final_total
