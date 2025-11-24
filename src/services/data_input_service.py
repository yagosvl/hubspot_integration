import os
from requests import session
from ..logger_setup import logger

def get_contacts():
    CONTACS_SERVICE_URL, CONTACS_SERVICE_TOKEN = os.getenv("CONTACS_SERVICE_URL"), os.getenv("CONTACS_SERVICE_TOKEN")
    if not CONTACS_SERVICE_URL or not CONTACS_SERVICE_TOKEN:
        raise OSError("Configuration error: essencial data to access contacs missing")
    
    try:
        s = session()
        contacts = s.get(CONTACS_SERVICE_URL, headers={"Authorization": f"Bearer {CONTACS_SERVICE_TOKEN}"})
        contacts.raise_for_status()
        return contacts.json()
    except Exception as ex:
        logger.warning(f"Error during fetch contacts {ex}")
        return []