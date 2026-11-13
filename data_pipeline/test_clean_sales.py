import pandas as pd

from data_pipeline.clean_sales import (
    normalise_region,
    parse_amount,
    parse_date,
    remove_duplicate_invoices,
    remove_test_distributors,
    split_rejects,
)


def test_normalise_region():
    result = normalise_region("  north  ")
    assert result == "North"


def test_normalise_region_abbreviation():
    result = normalise_region("E")
    assert result == "East"


def test_parse_amount():
    result = parse_amount("₹12,345.60")
    assert result == 12345.60


def test_parse_date():
    result = parse_date("15/07/2026")
    assert result == pd.Timestamp("2026-07-15")


def test_remove_duplicate_invoices():
    df = pd.DataFrame(
        {"Invoice No": ["INV001", "INV001", "INV002"], "Qty": [10, 10, 20]}
    )

    result = remove_duplicate_invoices(df)

    assert len(result) == 2
    assert result["Invoice No"].is_unique
    assert result.iloc[0]["Qty"] == 10


def test_remove_test_distributors():
    df = pd.DataFrame(
        {
            "Invoice No": ["INV001", "INV002", "INV003"],
            "Dist Code": ["D001", "D999", "D002"],
        }
    )

    result = remove_test_distributors(df)

    assert len(result) == 2
    assert "D999" not in result["Dist Code"].values


def test_split_rejects():
    df = pd.DataFrame(
        {
            "Invoice No": [
                "INV001",
                "INV002",
                "INV003",
                "INV004",
                "CN001",
                "INV005",
            ],
            "Qty": [None, 10, -5, 1201, -2, 10],
            "Net Value (INR)": [1000, None, -500, 5000, -200, 1000],
        }
    )

    rejects_df, clean_df = split_rejects(df)

    assert len(rejects_df) == 4
    assert len(clean_df) == 2

    assert rejects_df["reason"].value_counts().to_dict() == {
        "blank_qty": 1,
        "blank_net_value": 1,
        "negative_qty_not_credit_note": 1,
        "qty_over_1000": 1,
    }

    assert "CN001" in clean_df["Invoice No"].values
    assert "INV005" in clean_df["Invoice No"].values
