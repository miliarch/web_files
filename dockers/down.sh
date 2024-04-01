#!/bin/bash
# Run from project root to stop running container(s)
COMPOSE_FILE=${1:-'dockers/dev.yml'}
docker-compose -f $COMPOSE_FILE --project-directory $(pwd) down
