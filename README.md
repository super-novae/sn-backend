# sn-backend
Backend repo for voting system

## Backend Models
https://dbdiagram.io/d/629c499b54ce2635275fd31d

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

5. Create file for environment variables
   ```bash
   touch .env
   ```

6. Add contents to the .env file
   ```txt
    FLASK_ENV=development
    FLASK_APP=run.py
    SWAGGER_UI_CSS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui.min.css
    SWAGGER_UI_BUNDLE_JS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-bundle.min.js
    SWAGGER_UI_STANDALONE_PRESET_JS=https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.11.1/swagger-ui-standalone-preset.min.js
    REDOC_STANDALONE_JS=https://cdn.redoc.ly/redoc/latest/bundles/redoc.standalone.js
    ```

7. Run application
    ```bash
    flask run
    ```

