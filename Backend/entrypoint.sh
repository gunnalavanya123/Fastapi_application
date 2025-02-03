#!/bin/sh

# Change to the project directory
cd /backend

# Install dependencies from requirements.txt
pip3 install -r requirements.txt

# Uncomment the line below if you have database migrations to run
# python3 manage.py migrate

# Execute the passed command (CMD from Dockerfile)
exec "$@"
