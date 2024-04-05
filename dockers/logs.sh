#!/bin/bash
# Run from project root to deploy container(s)
COMPOSE_FILE=${1:-'dockers/dev.yml'}
export USER_ID=${2:-"$(id -u)"}
docker compose -f $COMPOSE_FILE --project-directory $(pwd) logs -f