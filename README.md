## Project Goal

Build a replica of Emami's Analytics Hub to support business analytics and data-driven decision-making.
Develop modular backend services, frontend dashboards, and data pipeline components.
Integrate analytics capabilities into a structured, maintainable, and scalable application.

## Prerequisites

The following tools are required for development:

- Git
- Visual Studio Code
- Python 3.11 or later
- Node.js 20 or later
- npm
- GitHub account with SSH authentication configured

## Environment Setup

Clone the repository:

```bash
git clone git@github.com:parthsingh23/intern-parth-insights-hub.git
cd intern-parth-insights-hub
```

Run the environment verification script:

```bash
bash scripts/check_env.sh
```

The script checks the installed versions of the required development tools and reports any missing dependencies.

## Branching and Commit Conventions

### Branch Structure

- `main`: Stable integration branch.
- `dev`: Development and review branch.
- `prod`: Production branch.
- `week1-setup`: Week 1 assignment branch created from `dev`.

### Workflow

1. Create an assignment-specific branch from `dev`.
2. Make changes and commit them using Conventional Commits.
3. Push the assignment branch to GitHub.
4. Open a Pull Request targeting `dev`.
5. Address review comments and obtain approval.
6. Merge approved changes from `dev` into `main`.

### Commit Message Format

Use Conventional Commits:

`type(scope): description`

Examples:

- `feat(backend): add fiscal year utility`
- `test(frontend): add INR formatting tests`
- `docs(readme): document development workflow`
- `chore(setup): configure project structure`
