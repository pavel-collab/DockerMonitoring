# Docker monitoring - web dashboard.
This readme describes how to configure and run web dashboard of docker monitoring app.

1. Install all requirements from root requirements.txt
    ```
    pip install -r requirements.txt
    ```
2. Complete all steps from root readme and configure postgresql database.
3. In `app.py` tune following line:
    * For development mode
    ```
    app.config.from_object('config.DevConfig')
    ```
    * For production mode
    ```
    app.config.from_object('config.ProdConfig')
    ```
    You can find parameters for both configs in `config.py`
4. Web app imports some settings from environment variables. So, before running app
you should initialize this variables.
    * Secret key is used for secure communication between server and client via flask.
        To initialize envirnoment variable with it, run:
        ```
        export SECRET_KEY="your secret key"
        ```
        You can configure it by yourself or generate it with following command:
        ```
        export SECRET_KEY="$(python -c "import os; print(os.urandom(24).hex())")"
        ```
    * Since the postgresql server may be located on another machine or on another
        network, connection uri should be configured separately with such command:
        ```
        export DATABASE_URI="postgresql://user[:password]@[host][:port][/dbname]"
        ```
        For more information about connection URI check [postgresql documentation](https://www.postgresql.org/docs/current/libpq-connect.html#LIBPQ-CONNSTRING-URIS)
    * [In case of Production config] You can specify ip address for flask server:
        ```
        export FLASK_SERVER_IP="0.0.0.0"
        ```

5. After all setup you can start you dashboard by running following command:
    ```
    python3 app.py
    ```
    Flask will show you addresses of your web app like this:
    ```
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5010
    * Running on http://192.168.0.2:5010
    ```
6. Copy address to your browser and use the dashboard!
