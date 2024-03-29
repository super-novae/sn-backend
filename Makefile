create_env:
	python3 -m venv env
	source env/bin/activate
	pip install -r requirements.txt

check_coverage:
	pytest --cov-config=.coveragerc --cov-report term-missing --cov=api --cov-fail-under=80

generate_coverage_report:
	pytest --cov-config=.coveragerc --cov-report term-missing --cov-report html:test_coverage --cov=api --cov-fail-under=80

# activate:
# 	source ./env/bin/activate

run:
	flask run --reload

grun:
	gunicorn run:app

migrate:
	flask db migrate
	flask db upgrade

upgrade:
	flask db upgrade

vulnerability-assessment:
	pip-audit --ignore-vuln CVE-2022-42969 --requirement requirements.txt

test_admin:
	pytest api/tests/test_admin.py --verbose

test_data:
	pytest api/tests/test_data.py --verbose

test_election:
	pytest api/tests/test_election.py --verbose

test_organization:
	pytest api/tests/test_organization.py --verbose

test_superuser:
	pytest api/tests/test_superuser.py --verbose

test_all: test_admin test_admin test_election test_organization test_superuser

lint:
	pylint --disable=all --enable=unused-import,unused-variable --score=yes api/
	black --diff --check --color  --target-version py310 --line-length 79 api/

docker-build:
	docker image build --file=./Dockerfile --tag=rising2392:sn-backend-api .

docker-run-local:
	docker container run -d --name sn-backend-api -p 8000:8000 --env-file .env rising2392:sn-backend-api