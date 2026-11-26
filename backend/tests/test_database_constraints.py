from datetime import date
from decimal import Decimal

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from backend.app.database.session import SessionLocal
from backend.app.models.distributor import Distributor
from backend.app.models.sale import Sale


def get_valid_distributor_id(session):
    distributor_id = session.scalar(select(Distributor.distributor_id).limit(1))
    assert distributor_id is not None, "No seeded distributor found"
    return distributor_id


def test_return_with_positive_quantity_is_rejected():
    with SessionLocal() as session:
        distributor_id = get_valid_distributor_id(session)

        invalid_sale = Sale(
            invoice_no="CONSTRAINT-TEST-RETURN",
            invoice_date=date(2026, 11, 26),
            distributor_id=distributor_id,
            sku_id=1,
            channel="General Trade",
            quantity=10.0,
            net_value=Decimal("100.00"),
            is_return=True,
        )

        session.add(invalid_sale)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()


def test_sale_with_nonexistent_sku_is_rejected():
    with SessionLocal() as session:
        distributor_id = get_valid_distributor_id(session)

        invalid_sale = Sale(
            invoice_no="CONSTRAINT-TEST-SKU",
            invoice_date=date(2026, 11, 26),
            distributor_id=distributor_id,
            sku_id=-999999,
            channel="General Trade",
            quantity=10.0,
            net_value=Decimal("100.00"),
            is_return=False,
        )

        session.add(invalid_sale)

        with pytest.raises(IntegrityError):
            session.commit()

        session.rollback()
