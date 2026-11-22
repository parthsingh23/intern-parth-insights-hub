import pytest
from fastapi.testclient import TestClient

from backend.app.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client


def test_get_sales_default_pagination(client):
    response = client.get("/sales")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 50
    assert data["total"] == 5418
    assert len(data["items"]) == 50


def test_get_sales_custom_pagination(client):
    response = client.get("/sales?page=1&page_size=10")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == 10
    assert data["total"] == 5418


def test_get_sales_second_page(client):
    response = client.get("/sales?page=2&page_size=10")

    assert response.status_code == 200

    data = response.json()

    assert data["page"] == 2
    assert len(data["items"]) == 10


def test_get_sales_empty_page(client):
    response = client.get("/sales?page=1000&page_size=50")

    assert response.status_code == 200

    data = response.json()

    assert data["items"] == []
    assert data["total"] == 5418


def test_filter_sales_by_region(client):
    response = client.get("/sales?region=East")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 1367
    assert all(item["Region"] == "East" for item in data["items"])


def test_filter_sales_by_brand(client):
    response = client.get("/sales?brand=Navratna")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] > 0
    assert all(item["Brand"] == "Navratna" for item in data["items"])


def test_filter_sales_by_return_status(client):
    response = client.get("/sales?is_return=true")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 78
    assert all(item["is_return"] is True for item in data["items"])


def test_filter_sales_by_september_2026(client):
    response = client.get(
        "/sales",
        params={
            "is_return": "false",
            "date_from": "2026-09-01",
            "date_to": "2026-09-30",
            "page_size": 1,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 298
    assert len(data["items"]) == 1


def test_sales_summary_overall(client):
    response = client.get("/sales/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["net_value"] == pytest.approx(60984552.24)
    assert data["quantity"] == pytest.approx(568254.0)
    assert data["row_count"] == 5418


def test_sales_summary_group_by_region(client):
    response = client.get("/sales/summary?group_by=region")

    assert response.status_code == 200

    data = response.json()

    assert data["row_count"] == 5418
    assert len(data["groups"]) == 4

    regional_totals = {group["group"]: group["net_value"] for group in data["groups"]}

    assert regional_totals == {
        "East": pytest.approx(11979450.64),
        "North": pytest.approx(14621494.11),
        "South": pytest.approx(15657120.63),
        "West": pytest.approx(18726486.86),
    }


def test_sales_summary_group_by_brand(client):
    response = client.get("/sales/summary?group_by=brand")

    assert response.status_code == 200

    data = response.json()

    assert len(data["groups"]) == 8
    assert sum(group["row_count"] for group in data["groups"]) == 5418


def test_sales_summary_navratna_december_2025(client):
    response = client.get(
        "/sales/summary",
        params={
            "brand": "Navratna",
            "date_from": "2025-12-01",
            "date_to": "2025-12-31",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["net_value"] == pytest.approx(462440.22)
    assert data["row_count"] == 74


def test_sales_summary_group_by_month(client):
    response = client.get("/sales/summary?group_by=month")

    assert response.status_code == 200

    data = response.json()

    assert len(data["groups"]) > 0
    assert all(len(group["group"]) == 7 for group in data["groups"])


def test_get_regions(client):
    response = client.get("/regions")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 4
    assert set(data) == {"East", "North", "South", "West"}


def test_get_brands(client):
    response = client.get("/brands")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 8
    assert "Navratna" in data


def test_get_skus(client):
    response = client.get("/skus")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 23
    assert all("SKU Code" in sku and "SKU Name" in sku for sku in data)


def test_get_distributors(client):
    response = client.get("/distributors")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 24
    assert all(
        "Dist Code" in distributor and "Distributor Name" in distributor
        for distributor in data
    )


def test_invalid_page_size(client):
    response = client.get("/sales?page_size=500")

    assert response.status_code == 422

    data = response.json()

    assert "error" in data
    assert data["error"]["code"] == "VALIDATION_ERROR"
    assert "message" in data["error"]


def test_invalid_date_format(client):
    response = client.get("/sales?date_from=2025-13-01")

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_region(client):
    response = client.get("/sales?region=Mars")

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_invalid_date_range(client):
    response = client.get(
        "/sales",
        params={
            "date_from": "2026-12-01",
            "date_to": "2026-01-01",
        },
    )

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_unknown_sku_code(client):
    response = client.get("/sales?sku_code=UNKNOWN")

    assert response.status_code == 404

    data = response.json()

    assert "error" in data
    assert data["error"]["code"] == "HTTP_404"
    assert "UNKNOWN" in data["error"]["message"]


def test_invalid_group_by(client):
    response = client.get("/sales/summary?group_by=invalid")

    assert response.status_code == 422

    data = response.json()

    assert data["error"]["code"] == "VALIDATION_ERROR"


def test_cors_allows_frontend_origin(client):
    response = client.options(
        "/sales",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.headers.get("access-control-allow-origin") == (
        "http://localhost:3000"
    )


def test_cors_rejects_unapproved_origin(client):
    response = client.options(
        "/sales",
        headers={
            "Origin": "http://localhost:5173",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert "access-control-allow-origin" not in response.headers
