#!/usr/bin/env bash

set -u

FAILED=0

echo "========== Environment Check =========="

# Git Version
if command -v git >/dev/null 2>&1; then
    echo "Git : $(git --version)"
else
    echo "Git isn't available"
    FAILED=1
fi

# VS Code Version
if command -v code >/dev/null 2>&1; then
    echo "Code: $(code --version)"
else
    echo "Code isn't available"
    FAILED=1
fi

# Python Version
if command -v python3 >/dev/null 2>&1; then
    PYTHON_MAJOR=$(python3 -c "import sys; print(sys.version_info.major)")
    PYTHON_MINOR=$(python3 -c "import sys; print(sys.version_info.minor)")

    if [[ $PYTHON_MAJOR -gt 3 || ($PYTHON_MAJOR -eq 3 && $PYTHON_MINOR -ge 11) ]]; then
        echo "Python: $(python3 --version)"
    else
        echo "Python 3.11 or later is required"
        FAILED=1
    fi
else
    echo "Python isn't available"
    FAILED=1
fi

# Node version

if command -v node >/dev/null 2>&1; then
    NODE_MAJOR=$(node -p 'process.versions.node.split(".")[0]')

    if [[ $NODE_MAJOR -ge 20 ]]; then
        echo "Node: $(node --version)"
    else
        echo "Node version 20 or higher is required"
        FAILED=1
    fi
else
    echo "Node isn't available"
    FAILED=1
fi

# NPM version
if command -v npm >/dev/null 2>&1; then
    echo "npm: $(npm --version)"
else
    echo "npm isn't available"
    FAILED=1
fi

if [[ $FAILED -eq 0 ]]; then
    echo "All environment checks passed!"
else
    echo "Some environment checks failed!"
fi

exit "$FAILED"
