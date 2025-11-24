# hubspot_integration
Project to integrate contacts using Hubspot API. The project was develop using Python 3.12.10

## Runnig the Project:

To run the project you first need to configure 3 enviroment variables:

- HUBSPOT_ACCESS_TOKEN
- CONTACS_SERVICE_URL
- CONTACS_SERVICE_TOKEN

After that you can run the following comands:

~~~
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m  src.app
~~~
