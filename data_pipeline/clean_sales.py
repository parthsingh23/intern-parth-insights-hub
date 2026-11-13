from pathlib import Path

import pandas as pd

file_path = "datasets/week02/week02_secondary_sales_raw.xlsx"


# Normalisation functions
def normalise_region(region):
    regions = {
        "north": "North",
        "n": "North",
        "south": "South",
        "s": "South",
        "east": "East",
        "e": "East",
        "west": "West",
        "w": "West",
    }

    normalised = region.strip().lower()

    return regions.get(normalised, "Region not found")


def parse_amount(net_value):
    if isinstance(net_value, str):
        formatted = net_value.replace("₹", "").replace(",", "")
    else:
        formatted = net_value
    return pd.to_numeric(formatted, errors="coerce")


def parse_date(date_value):
    return pd.to_datetime(date_value, format="mixed", dayfirst=True, errors="coerce")


def normalise_sku(sku_code):
    return sku_code.upper().strip()


def normalise_distributor(dist):
    return dist.title().strip()


def remove_duplicate_invoices(df):
    return df.drop_duplicates(subset="Invoice No", keep="first").copy()


def remove_test_distributors(df):
    return df[df["Dist Code"] != "D999"].copy()


# Separate valid and rejected records
def split_rejects(working_df):
    blank_qty = working_df["Qty"].isna()
    blank_net_value = working_df["Net Value (INR)"].isna()
    negative_qty_not_credit_note = (working_df["Qty"] < 0) & (
        ~working_df["Invoice No"].str.startswith("CN")
    )
    qty_over_1000 = working_df["Qty"] > 1000

    rejected_mask = (
        blank_qty | blank_net_value | negative_qty_not_credit_note | qty_over_1000
    )

    # Create rejection reasons
    reason = pd.Series(index=working_df.index, dtype="object")

    reason.loc[blank_qty] = "blank_qty"
    reason.loc[blank_net_value] = "blank_net_value"
    reason.loc[negative_qty_not_credit_note] = "negative_qty_not_credit_note"
    reason.loc[qty_over_1000] = "qty_over_1000"

    # Separate rejected and clean records
    rejects_df = working_df[rejected_mask].copy()
    clean_df = working_df[~rejected_mask].copy()

    rejects_df["reason"] = reason.loc[rejects_df.index]

    return rejects_df, clean_df


def main():
    sales = pd.read_excel(file_path, sheet_name="Raw Data")

    working_df = sales.copy()

    working_df = remove_duplicate_invoices(working_df)

    working_df = remove_test_distributors(working_df)

    working_df["Region"] = working_df["Region"].apply(normalise_region)
    working_df["Net Value (INR)"] = working_df["Net Value (INR)"].apply(parse_amount)
    working_df["Invoice Date"] = working_df["Invoice Date"].apply(parse_date)
    working_df["SKU Code"] = working_df["SKU Code"].apply(normalise_sku)
    working_df["Distributor Name"] = working_df["Distributor Name"].apply(
        normalise_distributor
    )

    rejects_df, clean_df = split_rejects(working_df)

    clean_df["is_return"] = clean_df["Invoice No"].str.startswith("CN")

    output_dir = "data_pipeline/output"
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    clean_df.to_csv(f"{output_dir}/clean_sales.csv", index=False)
    rejects_df.to_csv(f"{output_dir}/rejects.csv", index=False)

    print("Cleaning completed successfully!")
    print(f"Raw records: {len(sales)}")
    print(f"Clean records: {len(clean_df)}")
    print(f"Rejected records: {len(rejects_df)}")
    print(f"Returns: {clean_df['is_return'].sum()}")

    print("\nRejection breakdown:")
    print(rejects_df["reason"].value_counts())


if __name__ == "__main__":
    main()
