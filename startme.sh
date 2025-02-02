#!/bin/bash

docker compose down -v
docker compose build
docker compose up -d --remove-orphans
docker compose logs -f app