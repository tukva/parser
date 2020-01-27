include .env
export

setup_project:
		docker-compose build
run_project:
		docker-compose up server
run_tests:
		docker-compose -f docker-compose.testing.yml build
		docker-compose -f docker-compose.testing.yml run --rm test_server
		docker-compose -f docker-compose.testing.yml down
