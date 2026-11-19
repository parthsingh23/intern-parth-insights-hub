# Week 02: Secondary Sales Data Profiling

## 1. Dataset Overview

The raw distributor secondary sales dataset was loaded from the Excel workbook using Pandas.

| Metric | Value |
|---|---:|
| Total rows | 5,564 |
| Total columns | 12 |
| First index | 0 |
| Last index | 5,563 |
| Date range | 4 January 2025 – 9 December 2026 |

The dataset contains distributor sales information, including invoice details, regions, distributor information, product details, quantities and net sales values.

## 2. Column Information and Data Types

The dataset contains the following columns and data types:

| Column | Data Type |
|---|---|
| Invoice No | str |
| Invoice Date | object |
| Region | str |
| State | str |
| Dist Code | str |
| Distributor Name | str |
| SKU Code | str |
| SKU Name | str |
| Brand | str |
| Channel | str |
| Qty | float64 |
| Net Value (INR) | object |

**Data type summary:**

- 9 columns have `str` data type.
- 2 columns have `object` data type.
- 1 column has `float64` data type.

The Invoice Date and Net Value columns require further standardisation before analysis.

## 3. Missing Value Analysis

The following missing values were identified:

| Column | Non-null Values | Missing Values |
|---|---:|---:|
| Qty | 5,529 | 35 |
| Net Value (INR) | 5,539 | 25 |
| All other columns | 5,564 | 0 |

There are 35 missing quantity values and 25 missing net value values.

According to the assignment rules, records with missing Qty or Net Value must be moved to the rejects dataset with an appropriate reason.

## 4. Distinct Value Analysis

### Region

The Region column contains **24 distinct representations**, whereas only four standard regions are expected:

- North
- South
- East
- West

The variations include inconsistent capitalisation, leading/trailing spaces and single-letter abbreviations.

Examples include `north`, `NORTH`, ` North`, `N`, `E`, `W` and `S`.

These values need to be normalised into the four standard region names.

### Channel

The Channel column contains three distinct categories:

| Channel | Record Count |
|---|---:|
| General Trade | 3,906 |
| Modern Trade | 840 |
| Chemist | 818 |

General Trade has the highest number of records, while Chemist has the lowest.

### Distributor Code

There are **25 distinct distributor codes**.

D024 has the highest number of records, with 258 occurrences.

D999 appears six times and represents the test distributor `TEST DIST`. These records must be removed according to the assignment rules.

## 5. Invoice and Duplicate Analysis

The dataset contains:

| Metric | Count |
|---|---:|
| Total records | 5,564 |
| Unique invoice numbers | 5,504 |
| Duplicate invoice occurrences | 60 |

The Invoice No column contains 60 duplicate occurrences. The complete DataFrame also contains 60 duplicate rows.

The cleaning process must retain only one record per invoice number.

## 6. Date Analysis

The Invoice Date column contains mixed date formats and Python data types.

The distribution of Python types is:

| Python Type | Count |
|---|---:|
| str | 3,297 |
| datetime.datetime | 2,267 |
| **Total** | **5,564** |

The raw data contains multiple date representations, including:

- `2026-06-26`
- `15/07/2026`
- `10-Jul-25`
- `2026-09-06 00:00:00`

The dates were explored using Pandas `to_datetime()` with `format="mixed"`, `dayfirst=True` and `errors="coerce"`.

The resulting date analysis showed:

| Metric | Result |
|---|---|
| Minimum date | 4 January 2025 |
| Maximum date | 9 December 2026 |
| Unparseable dates | 0 |

All 5,564 date values were successfully parsed during this profiling exercise.

The cleaning pipeline must standardise these values into a consistent date representation.

## 7. Other Data Quality Observations

### Inconsistent Net Value Formatting

The Net Value (INR) column has an `object` data type and contains inconsistent representations.

Examples include:

- `₹4,295.07`
- `20743.72`
- `99999999`

Currency symbols and thousands separators need to be handled so that the final values can be stored as numeric data.

Six records contain a Net Value of `99999999`. All six belong to D999 / TEST DIST and are covered by the test-record removal rule.

### Credit Notes

Credit notes are identified by invoice numbers starting with `CN`.

The investigation found:

| Metric | Count |
|---|---:|
| Credit note records | 79 |
| Duplicate credit note occurrences | 1 |
| Unique credit note invoice numbers | 78 |

Credit note records contain negative quantities and net values. These negative values are valid for returns and must be preserved.

The cleaning pipeline must also add a Boolean `is_return` column to identify credit note records.

The credit note records were not associated with D999 in the profiling results.

### Other Standardisation Requirements

The Distributor Name and SKU Code columns also require standardisation:

- SKU Code should be trimmed and converted to uppercase.
- Distributor Name should be trimmed and consistently capitalised, using other records with the same distributor code as a reference.

## 8. Summary of Data Quality Issues

The following issues were identified before cleaning:

| No. | Data Quality Issue | Observation | Required Action |
|---:|---|---|---|
| 1 | Duplicate invoices | 60 duplicate invoice occurrences | Retain one record per invoice number |
| 2 | Missing values | 35 missing Qty and 25 missing Net Value values | Move affected records to rejects |
| 3 | Inconsistent regions | 24 representations instead of four standard regions | Normalise to North, South, East and West |
| 4 | Inconsistent dates | Mixed formats and Python data types | Parse and standardise dates |
| 5 | Inconsistent numeric formatting | Net Value contains currency symbols and separators | Convert Net Value to numeric |
| 6 | Test records | Six D999 records | Remove test records |
| 7 | Credit note duplicates | One duplicate occurrence among 79 credit note records | Preserve one record per unique credit note invoice |

Additional validation rules from the assignment require rejecting:

- Negative quantities where the invoice number does not start with `CN`.
- Quantities greater than 1,000.

## 9. Conclusion

The raw dataset contains 5,564 records across 12 columns. The profiling exercise identified duplicate invoices, missing values, inconsistent region representations, mixed date formats, inconsistent currency formatting and test records.

Credit notes require special handling because their negative quantities and net values are valid return transactions.

These findings establish the baseline for the cleaning pipeline. The next step is to implement the prescribed cleaning and rejection rules, preserve valid credit notes, and validate the resulting datasets against the assignment's acceptance criteria.
