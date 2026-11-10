# Emami Analytics Insights Hub

A replica of Emami's Analytics Hub, developed to support business analytics and data-driven decision-making.

## Project Goal

- Build a replica of Emami's Analytics Hub.
- Develop modular backend services, frontend dashboards, and data pipeline components.
- Integrate analytics capabilities into a structured, maintainable, and scalable application.

## Project Structure

```text
intern-parth-insights-hub/
├── backend/              # Python backend services
├── frontend/             # TypeScript frontend
├── data_pipeline/        # Data processing and pipeline components
├── datasets/             # Dataset storage
├── docs/                 # Project documentation
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

```bash
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

## Development and Testing

The project uses automated tests and code-quality tools to maintain consistency and catch errors early.

### Python Tests

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

### Python Code Quality

**Tools:** Ruff and Black

Check Python code for linting issues:

```bash
ruff check .
```

Check Python formatting without modifying files:

```bash
black --check .
```

### Frontend Tests

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

### Frontend Code Quality

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

### Run All Pre-commit Checks

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

## Quick Validation Checklist

After setting up the repository, run the following commands from the project root.

```bash
# Environment
bash scripts/check_env.sh

# Python tests
pytest -v

# Python quality checks
ruff check .
black --check .

# Frontend tests and quality checks
cd frontend
npm test
npm run lint
npm run format:check
npx tsc --noEmit

# Return to root
cd ..

# All pre-commit hooks
pre-commit run --all-files
```

A successful run confirms that the required environment checks, automated tests, and configured code-quality checks pass.

## Branching and Commit Conventions

### Branch Structure

- `main`: Stable integration branch.
- `dev`: Development and review branch.
- `prod`: Production branch.
- Assignment-specific branches: Created from `dev` for individual assignments.

Example:

```text
main
 └── dev
      └── week1-setup
```

### Workflow

1. Create an assignment-specific branch from `dev`.
2. Make changes and commit them using Conventional Commits.
3. Push the assignment branch to GitHub.
4. Open a Pull Request targeting `dev`.
5. Address review comments and obtain approval.
6. Merge approved changes into `dev`.
7. After the review process, integrate approved development changes into `main`.

### Commit Message Format

Follow Conventional Commits:

```text
type(scope): description
```

Examples:

```text
feat(backend): add fiscal year utility
test(frontend): add INR formatting tests
docs(readme): document development workflow
chore(setup): configure project structure
```

## Contributing

1. Clone the repository.
2. Set up the development environment.
3. Create an assignment-specific branch from `dev`.
4. Implement and test your changes.
5. Ensure all code-quality checks pass.
6. Commit and push your changes.
7. Open a Pull Request targeting `dev`.

Please follow the existing project structure, coding conventions, and commit message guidelines.
