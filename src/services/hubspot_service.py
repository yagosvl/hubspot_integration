import os
from ..logger_setup import logger
from concurrent.futures import ThreadPoolExecutor, as_completed
from hubspot.crm.contacts import BatchInputSimplePublicObjectBatchInputUpsert, SimplePublicObjectBatchInput
from hubspot import HubSpot

MAX_WORKERS = 10
BATCH_SIZE = 100

def convert_input_data_to_contact_input(raw_contacts : list) -> list[SimplePublicObjectBatchInput]:
    return [
        SimplePublicObjectBatchInput(
                id_property="email",
                id=contact["email"],
                properties={
                    "firstname": contact.get("first_name", ""),
                    "lastname": contact.get("last_name", ""),
                    "phone": contact.get("phone_number", ""),
                    "gender": contact.get("gender", "")
                }
            ) for contact in raw_contacts if contact.get("email", "")
    ]

def sync_data(batch_input : BatchInputSimplePublicObjectBatchInputUpsert):
    batch_subset = [batch_input[i : i+BATCH_SIZE] for i in range(0, len(batch_input), BATCH_SIZE)]
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(create_or_update_contacts, batch): batch for batch in batch_subset
        }
        for future in as_completed(futures):
            futures[future]
            try:
                response = future.result()
                if "error" in response:
                    logger.error(f"Error upserting contacts in HubSpot: {response['error']}")
            except Exception as e:
                logger.error(f"Exception upserting contacts in HubSpot: {e}")

def create_or_update_contacts(batch_input : list):
    HUBSPOT_ACCESS_TOKEN = os.getenv("HUBSPOT_ACCESS_TOKEN")
    if not HUBSPOT_ACCESS_TOKEN:
        raise OSError("Configuration Error: Hubspot configuration missing.")
    hs_client = HubSpot(access_token=HUBSPOT_ACCESS_TOKEN)
    t = BatchInputSimplePublicObjectBatchInputUpsert(inputs=batch_input)
    return hs_client.crm.contacts.batch_api.upsert(t).to_dict()