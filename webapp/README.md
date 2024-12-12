# Docker monitoring - web dashboard.
This readme describes how to configure and run web dashboard of docker monitoring app.

1. Install all requirements from root requirements.txt
    ```
    pip install -r requirements.txt
    ```
2. Complete all steps from root readme and configure postgresql database.
3. Set required parameters in `config.json`.
4. After all setup you can start you dashboard by running following command:
    ```
    python3 app.py
    ```
    Webapp will write server addresses into log file like this:
    ```
    * Running on all addresses (0.0.0.0)
    * Running on http://127.0.0.1:5010
    * Running on http://192.168.0.2:5010
    ```
5. Copy address to your browser and use the dashboard!
