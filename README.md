## Setup project

1. Install `docker` and `docker-compose`
1. Rename `default.env` file to `.env`
1. Set environment variable in `.env` file
1. Setup project via `make setup_project`
1. Create migrations via `docker-compose run --rm liquibase update`

## Run project

Run via `make run_project`

## Run tests

Run via `make run_tests`
