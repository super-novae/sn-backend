activate:
	source env/bin/activate

run:
	flask run

migrate:
	flask db migrate
	flask db upgrade

test_admin:
	pytest api/tests/test_admin.py --verbose

test_election:
	pytest api/tests/test_election.py --verbose

test_organization:
	pytest api/tests/test_organization.py --verbose

test_superuser:
	pytest api/tests/test_superuser.py --verbose

test_all: test_admin test_election test_organization test_superuser

lint:
	pylint --disable=all --enable=unused-import api/*.py
	black --diff --check api/*.py