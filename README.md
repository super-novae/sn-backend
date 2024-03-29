# sn-backend
Backend repo for voting system

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

## Test Coverage Report
1. Clone the repo
2. Open test coverage folder `./test_coverage/`
3. Open the file `index.html` to view the test coverage report

## Dockerhub Image
1. Visit dockerhub the latest docker image (https://hub.docker.com/repository/docker/rising2392/sn-backend-api)

## Backend Models
1. View the models used in backend (https://dbdiagram.io/d/629c499b54ce2635275fd31d)

## Project set-up
1. Clone the project
   ```bash
   git clone https://github.com/super-novae/sn-backend.git
   ```
2. Create virtual environment
   ```bash
   python3 -m venv env --prompt=sn-backend
   ```

3. Activate virtual environment
   ```bash
   source env/bin/activate
   ```

4. Install project dependencies
   ```bash
   pip install -r requirements.txt
   ```

5. Create needed databases for development in PostgreSQL shell
   ```bash
   CREATE DATABASE supernovae_dev_db;
   CREATE DATABASE supernovae_test_db;
   ```

6. Create file for environment variables
   ```bash
   touch .env
   ```

7. Add contents to the .env file
   ```txt
    FLASK_ENV=dev
    FLASK_APP=run.py
    SECRET_KEY=super_secret_key
    SWAGGER_UI_CSS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css
    SWAGGER_UI_BUNDLE_JS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.min.js
    SWAGGER_UI_STANDALONE_PRESET_JS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-standalone-preset.min.js
    REDOC_STANDALONE_JS=https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js
    DEV_DATABASE_URL=postgresql://postgres:password@localhost:5432/supernovae_dev_db
    TEST_DATABASE_URL=postgresql://postgres:password@localhost:5432/supernovae_test_db
    MAIL_SERVER=smtp.gmail.com
    MAIL_PORT=465
    MAIL_USERNAME=username@email.com
    MAIL_PASSWORD=superuserpassword
    ```

8. Perform initial migrations
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
9. Create a super user by opening `flask shell` and running the following commands
    ```bash
   from api.superuser.models import Superuser
   from api.extensions import db
   su = Superuser(name="Super User", username="super_u", email="superu@email.com")
   su.password = "helloworld__"
   db.session.add(su)
   db.session.commit()
   ```
10. Run application
    ```bash
    flask run
    ```

**Note**

There are two databases for development, DEV & TEST. Both of these databases are supposed to have the same structure at all times. I'm working on a script to handle that but for migrations would have to be manually applied to the test database as well.
