from datetime import date
from typing import Any

from ..repositories.sales_repository import SalesRepository


class SalesService:
    def __init__(self, repository: SalesRepository) -> None:
        self.repository = repository

    def get_sales(
        self,
        region: str | None = None,
        state: str | None = None,
        brand: str | None = None,
        sku_code: str | None = None,
        channel: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        is_return: bool | None = None,
        page: int = 1,
        page_size: int = 50,
    ) -> dict[str, Any]:

        filters = {
            "region": region,
            "state": state,
            "brand": brand,
            "sku_code": sku_code,
            "channel": channel,
            "date_from": date_from,
            "date_to": date_to,
            "is_return": is_return,
        }

        filtered_data = self.repository.filter(
            **{key: value for key, value in filters.items() if value is not None}
        )

        total = len(filtered_data)

        start = (page - 1) * page_size
        end = start + page_size

        page_data = filtered_data.iloc[start:end]

        items = page_data.copy()
        items["Invoice Date"] = items["Invoice Date"].dt.strftime("%Y-%m-%d")

        items = items.astype(object).where(items.notna(), None)

        return {
            "items": items.to_dict(orient="records"),
            "page": page,
            "page_size": page_size,
            "total": total,
        }

    def get_summary(
        self,
        region: str | None = None,
        state: str | None = None,
        brand: str | None = None,
        sku_code: str | None = None,
        channel: str | None = None,
        date_from: date | None = None,
        date_to: date | None = None,
        is_return: bool | None = None,
        group_by: str | None = None,
    ) -> dict[str, Any]:

        filters = {
            "region": region,
            "state": state,
            "brand": brand,
            "sku_code": sku_code,
            "channel": channel,
            "date_from": date_from,
            "date_to": date_to,
            "is_return": is_return,
        }

        filters = {key: value for key, value in filters.items() if value is not None}

        return self.repository.aggregate(
            filters=filters,
            group_by=group_by,
        )

    def get_regions(self) -> list[str]:
        return self.repository.get_regions()

    def get_brands(self) -> list[str]:
        return self.repository.get_brands()

    def get_skus(self) -> list[dict[str, str]]:
        return self.repository.get_skus()

    def get_distributors(self) -> list[dict[str, str]]:
        return self.repository.get_distributors()

    def has_sku(self, sku_code: str) -> bool:
        return self.repository.has_sku(sku_code)
