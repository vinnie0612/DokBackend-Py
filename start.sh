#!/bin/bash

# Stop old container
docker-compose down

# Pull changes
git config pull.rebase true
git pull

# Run Docker Compose
docker-compose up $2 --build