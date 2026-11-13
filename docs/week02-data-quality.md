# Week 2 Data Quality Report

## Summary

The raw workbook contained **5,564 rows and 12 columns**. After duplicate removal, test-distributor removal, standardisation and validation, the pipeline produced **5,418 clean records** and **80 rejected records**. The cleaned output retains **78 credit-note records**.

| Measure | Rows |
|---|---:|
| Raw records | 5,564 |
| Duplicate invoice rows removed | 60 |
| D999 test-distributor rows removed | 6 |
| Records remaining before validation | 5,498 |
| Rejected during validation | 80 |
| Final clean records | **5,418** |

The rejection counts below sum to 80. Each rejected record receives exactly one reason.

## Issues found and treatment

| Issue / cleaning rule | Rows affected | Treatment |
|---|---:|---|
| Duplicate invoice numbers | 60 removed | Kept the first row for each `Invoice No`. |
| Test distributor `D999` | 6 removed | Removed all records for the test distributor. |
| Non-standard Region values | 1,408 normalised | Standardised case, surrounding spaces and one-letter abbreviations to `North`, `South`, `East` or `West`. |
| Mixed invoice-date formats | 5,564 parsed | Parsed mixed formats, interpreting slash-separated dates as day-first. All dates parsed successfully; no invalid dates remained. |
| Net Value formatting | 5,539 non-blank values converted | Removed currency symbols and thousands separators where present, then converted values to numeric. The raw column contained 244 strings and 5,320 numeric values (floats or integers). |
| SKU Code formatting | 142 had surrounding whitespace; 64 changed with uppercasing | Trimmed whitespace and converted SKU codes to uppercase. These counts may overlap and are not added together. |
| Distributor Name formatting | Formatting variants found for all 24 valid distributor codes | Trimmed names and applied title case to standardise formatting. |
| Blank Qty | 35 rejected | Rejected with reason `blank_qty`. |
| Blank Net Value | 25 rejected | Rejected with reason `blank_net_value`. |
| Negative Qty on a non-credit-note invoice | 12 rejected | Rejected with reason `negative_qty_not_credit_note`. |
| Qty greater than 1,000 | 8 rejected | Rejected with reason `qty_over_1000`. |

## Credit notes and returns

Invoices whose numbers start with `CN` were treated as credit notes. Their negative quantities and negative net values were preserved, and `is_return` was set to `true`.

- Credit-note rows in the raw data: 79
- Duplicate credit-note row removed with duplicate invoice handling: 1
- Credit-note rows retained in the clean output: **78**

Negative quantities on invoices not starting with `CN` were rejected.

## Judgement calls and limitations

1. **Duplicate handling:** when an invoice number appeared more than once, the pipeline kept the first occurrence. The observed duplicate rows were exact duplicate rows.
2. **Date interpretation:** slash-separated dates were interpreted as `dd/mm/yyyy`, as specified in the workbook README. Other supported formats were parsed using mixed-format date parsing.
3. **Distributor names:** differences within the same distributor code were formatting variations (case and surrounding spaces). Names were standardised using trimming and title case.
4. **Out-of-period dates:** the README describes the extract as covering April 2025 to September 2026, but parsed dates range from 4 January 2025 to 9 December 2026. The pipeline retained these records because none of the listed cleaning rules instructed removal based on date range. This discrepancy should be confirmed with the data owner.
5. **No manual source edits:** the raw workbook was not edited by hand. Cleaning and rejection decisions are implemented in the repeatable Python pipeline.

## Validation outcome

The cleaned dataset passed the key assignment checks:

- 5,418 clean rows and 80 rejected rows.
- Rejection breakdown: 35 `blank_qty`, 25 `blank_net_value`, 12 `negative_qty_not_credit_note`, and 8 `qty_over_1000`.
- `Invoice No` is unique in the clean output.
- No `D999` records remain.
- `Region` contains only `North`, `South`, `East` and `West`.
- All invoice dates parsed successfully; quantity and net value are numeric.
- 78 credit-note rows remain with `is_return = true` and negative quantity and net value.
- Total net value: **₹60,984,552.24**.
- Total quantity: **568,254**.

The source workbook identifies the dataset as synthetic training data, not actual Emami sales data.
