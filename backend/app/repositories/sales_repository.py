from datetime import date, timedelta
from typing import Any

import pandas as pd

from ..config import SALES_DATA_PATH


class SalesRepository:
    GROUP_BY_COLUMNS = {
        "region": "Region",
        "state": "State",
        "brand": "Brand",
        "sku": "SKU Code",
        "channel": "Channel",
        "month": "Invoice Date",
    }

    def __init__(self) -> None:
        if not SALES_DATA_PATH.exists():
            raise FileNotFoundError(f"Sales dataset not found: {SALES_DATA_PATH}")

        self._data = pd.read_csv(SALES_DATA_PATH)

        required_columns = {
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
        }

        missing_columns = required_columns - set(self._data.columns)

        if missing_columns:
            raise ValueError(
                f"Dataset is missing required columns: " f"{sorted(missing_columns)}"
            )

        self._data["Invoice Date"] = pd.to_datetime(
            self._data["Invoice Date"],
            errors="coerce",
        )

        self._data["is_return"] = (
            self._data["is_return"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map({"true": True, "false": False})
        )

        if self._data["Invoice Date"].isna().any():
            raise ValueError("Dataset contains invalid invoice dates.")

        if self._data["is_return"].isna().any():
            raise ValueError("Dataset contains invalid return flags.")

        if self._data[["Qty", "Net Value (INR)"]].isna().any().any():
            raise ValueError("Dataset contains missing numeric values.")

    def filter(
        self,
        region: str | None = None,
        state: str | None = None,
        brand: str | None = None,
        sku_code: str | None = None,
        channel: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        is_return: bool | None = None,
    ) -> pd.DataFrame:

        mask = pd.Series(True, index=self._data.index)

        if region is not None:
            mask &= self._data["Region"] == region

        if state is not None:
            mask &= self._data["State"] == state

        if brand is not None:
            mask &= self._data["Brand"] == brand

        if sku_code is not None:
            mask &= self._data["SKU Code"] == sku_code

        if channel is not None:
            mask &= self._data["Channel"] == channel

        if date_from is not None:
            start_date = pd.Timestamp(date_from)
            mask &= self._data["Invoice Date"] >= start_date

        if date_to is not None:
            end_date = pd.Timestamp(date_to + timedelta(days=1))
            mask &= self._data["Invoice Date"] < end_date

        if is_return is not None:
            mask &= self._data["is_return"] == is_return

        return self._data.loc[mask].copy()

    def aggregate(
        self,
        filters: dict[str, Any] | None = None,
        group_by: str | None = None,
    ) -> dict[str, Any]:

        filtered_data = self.filter(**(filters or {}))

        result = {
            "net_value": round(float(filtered_data["Net Value (INR)"].sum()), 2),
            "quantity": float(filtered_data["Qty"].sum()),
            "row_count": int(len(filtered_data)),
        }

        if group_by is None:
            return result

        if group_by not in self.GROUP_BY_COLUMNS:
            raise ValueError(f"Unsupported group_by value: {group_by}")

        group_column = self.GROUP_BY_COLUMNS[group_by]

        if group_by == "month":
            grouping_data = filtered_data.assign(
                _group=filtered_data["Invoice Date"].dt.to_period("M").astype(str)
            )
            group_column = "_group"
        else:
            grouping_data = filtered_data

        grouped = (
            grouping_data.groupby(group_column, dropna=False)
            .agg(
                net_value=("Net Value (INR)", "sum"),
                quantity=("Qty", "sum"),
                row_count=("Invoice No", "size"),
            )
            .reset_index()
        )

        result["groups"] = [
            {
                "group": str(row[group_column]),
                "net_value": round(float(row["net_value"]), 2),
                "quantity": float(row["quantity"]),
                "row_count": int(row["row_count"]),
            }
            for _, row in grouped.iterrows()
        ]

        return result

    def get_regions(self) -> list[str]:
        return sorted(self._data["Region"].dropna().unique().tolist())

    def get_brands(self) -> list[str]:
        return sorted(self._data["Brand"].dropna().unique().tolist())

    def get_skus(self) -> list[dict[str, str]]:
        skus = (
            self._data[["SKU Code", "SKU Name"]]
            .drop_duplicates()
            .sort_values("SKU Code")
        )

        return skus.to_dict(orient="records")

    def get_distributors(self) -> list[dict[str, str]]:
        distributors = (
            self._data[["Dist Code", "Distributor Name"]]
            .drop_duplicates()
            .sort_values("Dist Code")
        )

        return distributors.to_dict(orient="records")

    def has_sku(self, sku_code: str) -> bool:
        return self._data["SKU Code"].eq(sku_code).any()
