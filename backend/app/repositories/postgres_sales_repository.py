from typing import Any

import pandas as pd
from sqlalchemy import MetaData, Table, func, select

from backend.app.database.session import SessionLocal, engine


class PostgresSalesRepository:
    COLUMNS = [
        "Invoice No",
        "Invoice Date",
        "Region",
        "State",
        "Dist Code",
        "Distributor Name",
        "SKU Code",
        "SKU Name",
        "Brand",
        "Channel",
        "Qty",
        "Net Value (INR)",
        "is_return",
    ]

    GROUP_BY_COLUMNS = {
        "region": "Region",
        "state": "State",
        "brand": "Brand",
        "sku": "SKU Code",
        "channel": "Channel",
    }

    def __init__(self):
        metadata = MetaData()
        self._view = Table(
            "v_sales_denorm",
            metadata,
            autoload_with=engine,
        )

    def _build_filters(
        self,
        region=None,
        state=None,
        brand=None,
        sku_code=None,
        channel=None,
        date_from=None,
        date_to=None,
        is_return=None,
    ):
        conditions = []

        filters = {
            "Region": region,
            "State": state,
            "Brand": brand,
            "SKU Code": sku_code,
            "Channel": channel,
            "is_return": is_return,
        }

        for column_name, value in filters.items():
            if value is not None:
                conditions.append(self._view.c[column_name] == value)

        if date_from is not None:
            conditions.append(self._view.c["Invoice Date"] >= date_from)

        if date_to is not None:
            conditions.append(self._view.c["Invoice Date"] <= date_to)

        return conditions

    def filter(
        self,
        region=None,
        state=None,
        brand=None,
        sku_code=None,
        channel=None,
        date_from=None,
        date_to=None,
        is_return=None,
    ) -> pd.DataFrame:
        conditions = self._build_filters(
            region=region,
            state=state,
            brand=brand,
            sku_code=sku_code,
            channel=channel,
            date_from=date_from,
            date_to=date_to,
            is_return=is_return,
        )

        statement = (
            select(self._view)
            .where(*conditions)
            .order_by(self._view.c["Invoice Date"], self._view.c["Invoice No"])
        )

        with SessionLocal() as session:
            rows = session.execute(statement).mappings().all()

        data = pd.DataFrame(rows, columns=self.COLUMNS)

        if not data.empty:
            data["Invoice Date"] = pd.to_datetime(data["Invoice Date"])
            data["Qty"] = pd.to_numeric(data["Qty"])
            data["Net Value (INR)"] = pd.to_numeric(data["Net Value (INR)"])

        return data

    def aggregate(
        self,
        filters=None,
        group_by=None,
    ) -> dict[str, Any]:
        filters = filters or {}

        conditions = self._build_filters(**filters)

        net_value = func.coalesce(func.sum(self._view.c["Net Value (INR)"]), 0)
        quantity = func.coalesce(func.sum(self._view.c["Qty"]), 0)
        row_count = func.count()

        statement = select(
            net_value.label("net_value"),
            quantity.label("quantity"),
            row_count.label("row_count"),
        ).where(*conditions)

        with SessionLocal() as session:
            result = session.execute(statement).mappings().one()

            summary = {
                "net_value": round(float(result["net_value"]), 2),
                "quantity": float(result["quantity"]),
                "row_count": int(result["row_count"]),
            }

            if group_by is None:
                return summary

            if group_by == "month":
                group_column = func.to_char(self._view.c["Invoice Date"], "YYYY-MM")
            else:
                column_name = self.GROUP_BY_COLUMNS.get(group_by)
                if column_name is None:
                    raise ValueError(f"Unsupported group_by value: {group_by}")
                group_column = self._view.c[column_name]

            grouped_statement = (
                select(
                    group_column.label("group"),
                    net_value.label("net_value"),
                    quantity.label("quantity"),
                    row_count.label("row_count"),
                )
                .where(*conditions)
                .group_by(group_column)
                .order_by(group_column)
            )

            grouped_rows = session.execute(grouped_statement).mappings().all()

            summary["groups"] = [
                {
                    "group": str(row["group"]),
                    "net_value": round(float(row["net_value"]), 2),
                    "quantity": float(row["quantity"]),
                    "row_count": int(row["row_count"]),
                }
                for row in grouped_rows
            ]

        return summary

    def get_regions(self) -> list[str]:
        statement = (
            select(self._view.c["Region"]).distinct().order_by(self._view.c["Region"])
        )

        with SessionLocal() as session:
            return list(session.scalars(statement).all())

    def get_brands(self) -> list[str]:
        statement = (
            select(self._view.c["Brand"]).distinct().order_by(self._view.c["Brand"])
        )

        with SessionLocal() as session:
            return list(session.scalars(statement).all())

    def get_skus(self) -> list[dict[str, str]]:
        statement = (
            select(
                self._view.c["SKU Code"],
                self._view.c["SKU Name"],
            )
            .distinct()
            .order_by(self._view.c["SKU Code"])
        )

        with SessionLocal() as session:
            rows = session.execute(statement).mappings().all()

        return [
            {
                "SKU Code": row["SKU Code"],
                "SKU Name": row["SKU Name"],
            }
            for row in rows
        ]

    def get_distributors(self) -> list[dict[str, str]]:
        statement = (
            select(
                self._view.c["Dist Code"],
                self._view.c["Distributor Name"],
            )
            .distinct()
            .order_by(self._view.c["Dist Code"])
        )

        with SessionLocal() as session:
            rows = session.execute(statement).mappings().all()

        return [
            {
                "Dist Code": row["Dist Code"],
                "Distributor Name": row["Distributor Name"],
            }
            for row in rows
        ]

    def has_sku(self, sku_code: str) -> bool:
        statement = (
            select(self._view.c["SKU Code"])
            .where(self._view.c["SKU Code"] == sku_code)
            .limit(1)
        )

        with SessionLocal() as session:
            return session.scalar(statement) is not None
