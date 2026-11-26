import sys
from decimal import Decimal
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import delete, func, select, text
from sqlalchemy.dialects.postgresql import insert as pg_insert

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from backend.app.database.session import SessionLocal  # noqa: E402
from backend.app.models import (  # noqa: E402
    SKU,
    Brand,
    Distributor,
    Region,
    Sale,
    State,
)

MASTER_FILE = ROOT / "datasets" / "week04" / "week04_masters.xlsx"
SALES_FILE = ROOT / "data_pipeline" / "output" / "clean_sales.csv"

EXPECTED_COUNTS = {
    "regions": 4,
    "states": 12,
    "distributors": 24,
    "brands": 8,
    "skus": 23,
    "sales": 5418,
}


def load_master_data(session, sheet_name, model, primary_key, update_columns):
    df = pd.read_excel(MASTER_FILE, sheet_name=sheet_name)

    if df[primary_key].duplicated().any():
        raise ValueError(f"Duplicate {primary_key} values in {sheet_name}")

    records = df.to_dict(orient="records")

    if not records:
        raise ValueError(f"No records found in sheet: {sheet_name}")

    statement = pg_insert(model).values(records)
    statement = statement.on_conflict_do_update(
        index_elements=[getattr(model, primary_key)],
        set_={column: getattr(statement.excluded, column) for column in update_columns},
    )

    session.execute(statement)
    print(f"{sheet_name}: processed {len(records)} records")


def reset_sequence(session, table_name, column_name):
    statement = text(f"""
        SELECT setval(
            pg_get_serial_sequence('{table_name}', '{column_name}'),
            COALESCE(MAX({column_name}), 1),
            COUNT(*) > 0
        )
        FROM {table_name}
        """)
    session.execute(statement)


def load_sales(session):
    df = pd.read_csv(
        SALES_FILE,
        dtype={"Net Value (INR)": "string"},
    )

    required_columns = {
        "Invoice No",
        "Invoice Date",
        "Dist Code",
        "SKU Code",
        "Channel",
        "Qty",
        "Net Value (INR)",
        "is_return",
    }

    missing = required_columns - set(df.columns)
    if missing:
        raise ValueError(f"Missing sales columns: {sorted(missing)}")

    distributor_map = dict(
        session.execute(
            select(Distributor.distributor_code, Distributor.distributor_id)
        ).all()
    )

    sku_map = dict(session.execute(select(SKU.sku_code, SKU.sku_id)).all())

    unknown_distributors = set(df["Dist Code"].dropna()) - set(distributor_map)
    unknown_skus = set(df["SKU Code"].dropna()) - set(sku_map)

    if unknown_distributors:
        raise ValueError(f"Unknown distributor codes: {sorted(unknown_distributors)}")

    if unknown_skus:
        raise ValueError(f"Unknown SKU codes: {sorted(unknown_skus)}")

    if df[list(required_columns)].isna().any().any():
        raise ValueError("Sales data contains missing required values")

    dates = pd.to_datetime(df["Invoice Date"], errors="raise").dt.date

    records = []

    for index, row in df.iterrows():
        quantity = float(row["Qty"])
        is_return = bool(row["is_return"])

        if (is_return and quantity >= 0) or (not is_return and quantity <= 0):
            raise ValueError(
                f"Invalid quantity/return combination at CSV row {index + 2}"
            )

        records.append(
            {
                "invoice_no": str(row["Invoice No"]),
                "invoice_date": dates.iloc[index],
                "distributor_id": distributor_map[row["Dist Code"]],
                "sku_id": sku_map[row["SKU Code"]],
                "channel": str(row["Channel"]),
                "quantity": quantity,
                "net_value": Decimal(str(row["Net Value (INR)"])),
                "is_return": is_return,
            }
        )

    session.execute(delete(Sale))
    session.execute(Sale.__table__.insert(), records)

    print(f"sales: loaded {len(records)} records")


def print_database_summary(session):
    models = {
        "regions": Region,
        "states": State,
        "distributors": Distributor,
        "brands": Brand,
        "skus": SKU,
        "sales": Sale,
    }

    print("\nDATABASE ROW COUNTS")
    for name, model in models.items():
        count = session.scalar(select(func.count()).select_from(model))
        expected = EXPECTED_COUNTS[name]
        print(f"{name}: {count} (expected {expected})")

        if count != expected:
            raise ValueError(f"{name} count mismatch: expected {expected}, got {count}")

    total_value = session.scalar(select(func.sum(Sale.net_value)))
    return_count = session.scalar(
        select(func.count()).select_from(Sale).where(Sale.is_return.is_(True))
    )

    print(f"\nTotal net value: {total_value}")
    print(f"Return rows: {return_count}")

    if total_value != Decimal("60984552.24"):
        raise ValueError(f"Unexpected net value: {total_value}")

    if return_count != 78:
        raise ValueError(f"Unexpected return count: {return_count}")


def main():
    if not MASTER_FILE.exists():
        raise FileNotFoundError(MASTER_FILE)

    if not SALES_FILE.exists():
        raise FileNotFoundError(SALES_FILE)

    with SessionLocal.begin() as session:
        load_master_data(session, "regions", Region, "region_id", ["region_name"])

        load_master_data(
            session,
            "states",
            State,
            "state_id",
            ["state_name", "region_id"],
        )

        load_master_data(
            session,
            "distributors",
            Distributor,
            "distributor_id",
            ["distributor_code", "distributor_name", "state_id", "city"],
        )

        load_master_data(session, "brands", Brand, "brand_id", ["brand_name"])

        load_master_data(
            session,
            "skus",
            SKU,
            "sku_id",
            [
                "sku_code",
                "sku_name",
                "brand_id",
                "category",
                "pack_size",
                "mrp",
            ],
        )

        reset_sequence(session, "regions", "region_id")
        reset_sequence(session, "states", "state_id")
        reset_sequence(session, "distributors", "distributor_id")
        reset_sequence(session, "brands", "brand_id")
        reset_sequence(session, "skus", "sku_id")

        load_sales(session)
        print_database_summary(session)

    print("\nDatabase seeding completed successfully.")


if __name__ == "__main__":
    main()
