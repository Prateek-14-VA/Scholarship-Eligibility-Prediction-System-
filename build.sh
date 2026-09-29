#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

# Retrain the model in Render's Python environment
python scripts/train_models.py

# Initialize the database tables (creates if not exist)
python scripts/setup_database.py

echo "Build completed successfully"