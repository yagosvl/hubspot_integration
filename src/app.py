from datetime import datetime
from .logger_setup import logger
from .services.data_input_service import get_contacts
from .services.hubspot_service import sync_data, convert_input_data_to_contact_input

def integrate_contacts():
    start = datetime.now()
    raw_contacts = get_contacts()
    if not raw_contacts:
        logger.info(f"No contacts")
        return
    
    batch_contacts = convert_input_data_to_contact_input(raw_contacts)
    sync_data(batch_contacts)
    end = datetime.now()
    logger.info(f"Contacts integrated in {end-start} seconds")

if __name__ == "__main__":
    integrate_contacts()