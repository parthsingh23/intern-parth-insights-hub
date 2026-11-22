from datetime import date
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Region(str, Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"


class Channel(str, Enum):
    GENERAL_TRADE = "General Trade"
    CHEMIST = "Chemist"
    MODERN_TRADE = "Modern Trade"


class GroupBy(str, Enum):
    REGION = "region"
    STATE = "state"
    BRAND = "brand"
    SKU = "sku"
    CHANNEL = "channel"
    MONTH = "month"


class SalesFilters(BaseModel):
    model_config = ConfigDict(extra="forbid")

    region: Region | None = None
    state: str | None = None
    brand: str | None = None
    sku_code: str | None = None
    channel: Channel | None = None
    date_from: date | None = None
    date_to: date | None = None
    is_return: bool | None = None

    @model_validator(mode="after")
    def validate_date_range(self):
        if (
            self.date_from is not None
            and self.date_to is not None
            and self.date_from > self.date_to
        ):
            raise ValueError("date_from cannot be later than date_to")

        return self


class SalesQuery(SalesFilters):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=50, ge=1, le=200)


class SalesSummaryQuery(SalesFilters):
    group_by: GroupBy | None = None


class SalesItem(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    invoice_no: str = Field(alias="Invoice No")
    invoice_date: date = Field(alias="Invoice Date")
    region: str = Field(alias="Region")
    state: str = Field(alias="State")
    dist_code: str = Field(alias="Dist Code")
    distributor_name: str = Field(alias="Distributor Name")
    sku_code: str = Field(alias="SKU Code")
    sku_name: str = Field(alias="SKU Name")
    brand: str = Field(alias="Brand")
    channel: str = Field(alias="Channel")
    qty: float = Field(alias="Qty")
    net_value: float = Field(alias="Net Value (INR)")
    is_return: bool = Field(alias="is_return")


class SalesResponse(BaseModel):
    items: list[SalesItem]
    page: int
    page_size: int
    total: int


class SalesSummaryGroup(BaseModel):
    group: str
    net_value: float
    quantity: float
    row_count: int


class SalesSummary(BaseModel):
    net_value: float
    quantity: float
    row_count: int
    groups: list[SalesSummaryGroup] | None = None


class SKUItem(BaseModel):
    sku_code: str = Field(alias="SKU Code")
    sku_name: str = Field(alias="SKU Name")
    model_config = ConfigDict(populate_by_name=True)


class DistributorItem(BaseModel):
    dist_code: str = Field(alias="Dist Code")
    distributor_name: str = Field(alias="Distributor Name")
    model_config = ConfigDict(populate_by_name=True)


class ErrorDetail(BaseModel):
    code: str
    message: str


class ErrorResponse(BaseModel):
    error: ErrorDetail
