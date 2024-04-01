#!/bin/bash
# Run from project root to build image
COMPOSE_FILE=${1:-'dockers/dev.yml'}
docker-compose -f $COMPOSE_FILE --project-directory $(pwd) build --no-cache
