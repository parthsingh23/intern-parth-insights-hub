from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request

from ..schemas.sales import (
    DistributorItem,
    ErrorResponse,
    SalesQuery,
    SalesResponse,
    SalesSummary,
    SalesSummaryQuery,
    SKUItem,
)
from ..services.sales_service import SalesService

router = APIRouter(tags=["Sales"])


def get_sales_service(request: Request) -> SalesService:
    return request.app.state.sales_service


@router.get(
    "/sales",
    response_model=SalesResponse,
    summary="Get sales records",
    description=(
        "Retrieve sales records with optional filters and pagination. "
        "The maximum page size is 200."
    ),
    responses={
        404: {
            "model": ErrorResponse,
            "description": "The supplied SKU code does not exist.",
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid query parameters.",
        },
    },
)
def get_sales(
    query: Annotated[SalesQuery, Query()],
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> dict:
    if query.sku_code is not None and not service.has_sku(query.sku_code):
        raise HTTPException(
            status_code=404,
            detail=f"Unknown sku_code: {query.sku_code}",
        )

    filters = query.model_dump(exclude={"page", "page_size"})

    if query.region is not None:
        filters["region"] = query.region.value

    if query.channel is not None:
        filters["channel"] = query.channel.value

    return service.get_sales(
        **filters,
        page=query.page,
        page_size=query.page_size,
    )


@router.get(
    "/sales/summary",
    response_model=SalesSummary,
    summary="Get sales summary",
    description=(
        "Calculate sales totals using optional filters. "
        "Results can optionally be grouped by region, state, brand, "
        "SKU, channel, or month."
    ),
    responses={
        404: {
            "model": ErrorResponse,
            "description": "The supplied SKU code does not exist.",
        },
        422: {
            "model": ErrorResponse,
            "description": "Invalid query parameters.",
        },
    },
)
def get_sales_summary(
    query: Annotated[SalesSummaryQuery, Query()],
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> dict:
    if query.sku_code is not None and not service.has_sku(query.sku_code):
        raise HTTPException(
            status_code=404,
            detail=f"Unknown sku_code: {query.sku_code}",
        )

    filters = query.model_dump(exclude={"group_by"})

    if query.region is not None:
        filters["region"] = query.region.value

    if query.channel is not None:
        filters["channel"] = query.channel.value

    group_by = query.group_by.value if query.group_by else None

    return service.get_summary(
        **filters,
        group_by=group_by,
    )


@router.get(
    "/regions",
    response_model=list[str],
    summary="List regions",
    description="Return all distinct sales regions.",
)
def get_regions(
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> list[str]:
    return service.get_regions()


@router.get(
    "/brands",
    response_model=list[str],
    summary="List brands",
    description="Return all distinct brands in the sales dataset.",
)
def get_brands(
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> list[str]:
    return service.get_brands()


@router.get(
    "/skus",
    response_model=list[SKUItem],
    summary="List SKUs",
    description="Return distinct SKU codes and their corresponding names.",
)
def get_skus(
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> list[dict[str, str]]:
    return service.get_skus()


@router.get(
    "/distributors",
    response_model=list[DistributorItem],
    summary="List distributors",
    description="Return distinct distributor codes and their corresponding names.",
)
def get_distributors(
    service: Annotated[SalesService, Depends(get_sales_service)],
) -> list[dict[str, str]]:
    return service.get_distributors()
