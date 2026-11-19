#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(
    cd "$(dirname "${BASH_SOURCE[0]}")/.."
    pwd
)"

cd "$PROJECT_ROOT"

echo "Installing project dependencies..."
uv sync

echo "Cleaning previous builds..."
rm -rf build
rm -rf dist

echo "Building Pac-Man executable..."
uv run pyinstaller \
    --clean \
    --noconfirm \
    packaging/pacman.spec

echo "Copying configuration files..."
cp config.json dist/config.json
cp highscores.json dist/highscores.json

echo
echo "Build completed successfully."
echo "Executable: dist/pacman42"
echo
echo "Launch with:"
echo "./dist/pacman42 ./dist/config.json"