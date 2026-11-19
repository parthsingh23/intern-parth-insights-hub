# Emami Analytics Insights Hub

A replica of Emami's Analytics Hub, developed to support business analytics and data-driven decision-making.

## Project Goal

- Build a replica of Emami's Analytics Hub.
- Develop modular backend services, frontend dashboards, and data pipeline components.
- Integrate analytics capabilities into a structured, maintainable, and scalable application.
- Develop reliable data processing workflows to transform raw business data into meaningful insights.

## Project Structure

```text
intern-parth-insights-hub/
├── backend/              # Python backend services
├── frontend/             # TypeScript frontend
├── data_pipeline/        # Data processing and pipeline components
│   ├── output/           # Generated pipeline outputs
│   ├── clean_sales.py    # Secondary sales cleaning pipeline
│   ├── load_sqlite.py    # Load cleaned data into SQLite
│   ├── run_queries.py    # Execute SQL analysis queries
│   └── queries.sql       # SQL analysis queries
├── datasets/             # Raw dataset storage (not tracked by Git)
├── docs/                 # Project and assignment documentation
├── scripts/              # Utility and environment scripts
├── .gitattributes
├── .gitignore
├── .pre-commit-config.yaml
├── .python-version
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Prerequisites

Install the following tools before starting:

| Tool | Minimum version |
|---|---|
| Git | Latest stable |
| Python | 3.11+ |
| Node.js | 20+ |
| npm | Included with Node.js |
| Visual Studio Code | Latest stable |
| GitHub account | SSH authentication configured |

**Operating system:** Linux, macOS, or Windows through WSL2 with Ubuntu. The development scripts and pre-commit configuration use Unix-style paths.

## Getting Started

### 1. Clone the repository

Make sure your GitHub SSH authentication is configured.

```bash
git clone git@github.com:parthsingh23/intern-parth-insights-hub.git

cd intern-parth-insights-hub
```

### 2. Verify the environment

Run the environment verification script:

```bash
bash scripts/check_env.sh
```

The script checks the installed versions of Git, VS Code, Python, Node.js, and npm.

It reports missing or incompatible dependencies and exits with a non-zero status if a required check fails.

### 3. Set up the Python environment

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

**Linux / macOS / WSL:**

```bash
source .venv/bin/activate
```

**Windows:**

```powershell
.\.venv\Scripts\Activate.ps1
```

Install Python dependencies:

```bash
python -m pip install --upgrade pip

pip install -r requirements.txt
```

The requirements file contains the pinned Python development and testing dependencies.

### 4. Set up the frontend environment

Navigate to the frontend directory:

```bash
cd frontend
```

Install dependencies using the lockfile:

```bash
npm ci
```

Return to the repository root:

```bash
cd ..
```

`npm ci` installs the exact dependency versions recorded in `package-lock.json`.

### 5. Configure pre-commit hooks

Install the Git hooks:

```bash
pre-commit install
```

These hooks automatically run configured code-quality checks before a commit is created.

---

# Week 2: Secondary Sales Data Pipeline and Analysis

## Overview

Week 2 focuses on building a data cleaning and analysis workflow using a deliberately messy secondary sales dataset.

The objective is to transform raw Excel data into a validated, structured dataset and use SQL to derive business insights.

The workflow includes:

1. Raw data inspection and profiling.
2. Data cleaning and standardisation using Pandas.
3. Rejection classification and data quality validation.
4. Automated testing using pytest.
5. Loading cleaned data into SQLite.
6. Business analysis using SQL queries.
7. Documentation of data quality findings and analytical results.

**Dataset note:** The supplied workbook contains synthetic training data. It is not actual Emami sales data.

## Dataset

The raw workbook contains two sheets:

- `README`: Dataset description and cleaning instructions.
- `Raw Data`: Secondary sales records.

The dataset contains 5,564 raw records and 12 columns.

| Column | Description |
|---|---|
| Invoice No | Unique invoice identifier |
| Invoice Date | Invoice transaction date |
| Region | Sales region |
| State | State associated with the transaction |
| Dist Code | Distributor identifier |
| Distributor Name | Distributor name |
| SKU Code | Product identifier |
| SKU Name | Product name |
| Brand | Product brand |
| Channel | Sales channel |
| Qty | Quantity sold |
| Net Value (INR) | Net transaction value in INR |

### Dataset Location

Place the supplied workbook at:

```text
datasets/
└── week02/
    └── week02_secondary_sales_raw.xlsx
```

The `datasets/` directory is excluded from Git to avoid committing raw datasets.

## Data Cleaning Pipeline

The cleaning pipeline is implemented in:

```text
data_pipeline/clean_sales.py
```

The pipeline uses Pandas to read, transform, validate, and export the secondary sales data.

### Cleaning Operations

The following transformations are applied:

| Operation | Description |
|---|---|
| Duplicate removal | Remove duplicate invoice numbers, keeping the first occurrence |
| Test distributor removal | Remove records associated with distributor code `D999` |
| Region standardisation | Normalise region names and abbreviations into North, South, East, and West |
| Date parsing | Parse supported date formats using day-first interpretation where applicable |
| Amount conversion | Convert currency-formatted values into numeric values |
| SKU standardisation | Trim whitespace and convert SKU codes to uppercase |
| Distributor standardisation | Trim whitespace and standardise distributor names using title case |
| Return identification | Identify credit notes using invoice numbers beginning with `CN` |

### Rejection Rules

Records that violate the specified data quality rules are separated from the cleaned dataset.

| Rejection Reason | Condition |
|---|---|
| `blank_qty` | Quantity is missing |
| `blank_net_value` | Net Value is missing |
| `negative_qty_not_credit_note` | Quantity is negative but invoice number does not begin with `CN` |
| `qty_over_1000` | Quantity exceeds 1,000 |

Each rejected record receives a reason explaining why it was excluded.

Valid credit-note records are retained. Their negative quantities and negative net values represent returns.

A Boolean column named `is_return` identifies these records.

### Running the Cleaning Pipeline

Run the following command from the repository root:

```bash
python data_pipeline/clean_sales.py
```

The script generates:

```text
data_pipeline/
└── output/
    ├── clean_sales.csv
    └── rejects.csv
```

The script creates the output directory if it does not exist.

## Cleaning Results

The expected output from the supplied dataset is:

| Metric | Expected Result |
|---|---:|
| Raw records | 5,564 |
| Clean records | 5,418 |
| Rejected records | 80 |
| Valid returns retained | 78 |
| Duplicate invoice records removed | 60 |
| Test distributor records removed | 6 |

### Rejection Breakdown

| Rejection Reason | Records |
|---|---:|
| `blank_qty` | 35 |
| `blank_net_value` | 25 |
| `negative_qty_not_credit_note` | 12 |
| `qty_over_1000` | 8 |
| **Total** | **80** |

## Automated Testing

The cleaning pipeline includes unit tests implemented using pytest.

Test file:

```text
data_pipeline/test_clean_sales.py
```

The tests cover:

- Region name standardisation.
- Region abbreviation handling.
- Currency and amount parsing.
- Date parsing.
- Duplicate invoice removal.
- Test distributor removal.
- Rejection classification.

Run the tests:

```bash
python -m pytest data_pipeline/test_clean_sales.py -v
```

Run the complete Python test suite:

```bash
python -m pytest -v
```

## SQLite Integration

The cleaned CSV is loaded into a SQLite database for analytical queries.

The database loading script is:

```text
data_pipeline/load_sqlite.py
```

Run:

```bash
python data_pipeline/load_sqlite.py
```

This creates the SQLite database:

```text
data_pipeline/output/sales.db
```

The cleaned CSV is loaded into a table named:

```sql
sales
```

The loading script uses `if_exists="replace"` to replace the existing table when rerun, preventing duplicate records from accumulating.

The generated SQLite database is excluded from Git because it can be recreated from the cleaned CSV.

## SQL Business Analysis

SQL queries are maintained separately in:

```text
data_pipeline/queries.sql
```

The queries cover six analytical requirements:

| Query | Analysis |
|---|---|
| 1 | Total net sales value and total quantity |
| 2 | Net sales value by region and percentage contribution |
| 3 | Top five SKUs by net sales value |
| 4 | Monthly net sales trend |
| 5 | Return value as a percentage of gross sales by region |
| 6 | Three distributors with the highest return value |

Execute all queries:

```bash
python data_pipeline/run_queries.py
```

The script executes the SQL statements against the generated SQLite database and displays their results.

### Analytical Results

The expected overall figures are:

| Metric | Result |
|---|---:|
| Total Net Value | ₹60,984,552.24 |
| Total Quantity | 568,254 |

The regional analysis identifies West as the largest contributor to net sales value, followed by South, North, and East.

The return analysis calculates return value relative to gross sales, allowing comparisons of return rates across regions.

Detailed SQL statements, query outputs, and interpretations are documented in:

```text
docs/week02-queries.md
```

## Week 2 Documentation

The following documents record the profiling, cleaning, and analysis work:

| File | Description |
|---|---|
| `docs/week02-profile.md` | Initial dataset profiling, column information, missing values, distinct counts, and identified data quality issues |
| `docs/week02-data-quality.md` | Cleaning operations, affected record counts, validation results, and judgement calls |
| `docs/week02-queries.md` | SQL queries, analytical results, and business interpretations |

---

# Development and Testing

The project uses automated tests and code-quality tools to maintain consistency and catch errors early.

## Python Tests

**Framework:** pytest

Run all Python tests:

```bash
pytest -v
```

Run tests for a specific module:

```bash
pytest backend/warmup/test_utils.py -v
```

Current Python test coverage includes:

| Function | What is tested |
|---|---|
| `fiscal_year()` | Indian financial year calculation |
| `format_inr()` | Indian currency formatting |
| `parse_pack_size()` | Pack-size parsing and unit extraction |
| Data cleaning functions | Region, amount, date, duplicate, test-row, and rejection handling |

## Python Code Quality

**Tools:** Ruff and Black

Check Python code for linting issues:

```bash
ruff check .
```

Check Python formatting without modifying files:

```bash
black --check .
```

## Frontend Tests

**Framework:** Vitest

Navigate to the frontend directory:

```bash
cd frontend
```

Run frontend tests:

```bash
npm test
```

Current frontend tests cover the `formatInr()` utility, including Indian number grouping, decimal formatting, zero values, and different number sizes.

## Frontend Code Quality

**Tools:** ESLint, Prettier, and TypeScript

Run ESLint:

```bash
npm run lint
```

Check formatting:

```bash
npm run format:check
```

Run the TypeScript type checker:

```bash
npx tsc --noEmit
```

Return to the repository root:

```bash
cd ..
```

## Run All Pre-commit Checks

To execute every configured pre-commit hook manually:

```bash
pre-commit run --all-files
```

Configured hooks:

| Tool | Purpose |
|---|---|
| Ruff | Python linting |
| Black | Python formatting |
| ESLint | Frontend linting |
| Prettier | Frontend formatting |

---

# Quick Validation Checklist

After setting up the repository, run the following commands from the project root.

### Environment and Python

```bash
# Environment
bash scripts/check_env.sh

# Python tests
pytest -v

# Python quality checks
ruff check .
black --check .
```

### Week 2 Data Pipeline

```bash
# Clean the raw dataset
python data_pipeline/clean_sales.py

# Load cleaned data into SQLite
python data_pipeline/load_sqlite.py

# Execute SQL queries
python data_pipeline/run_queries.py

# Run data pipeline tests
pytest data_pipeline/ -v
```

### Frontend

```bash
cd frontend

npm test
npm run lint
npm run format:check
npx tsc --noEmit

cd ..
```

### Pre-commit

```bash
pre-commit run --all-files
```

A successful run confirms that the required environment checks, automated tests, data pipeline operations, and configured code-quality checks pass.

---

# Branching and Commit Conventions

## Branch Structure

- `main`: Stable integration branch.
- `dev`: Development and review branch.
- `prod`: Production branch.
- Assignment-specific branches: Created from `dev` for individual assignments.

Example:

```text
main
└── dev
     ├──