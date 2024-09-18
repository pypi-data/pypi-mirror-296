#main.py
import pyarrow.parquet as pq
import pyarrow.csv as pcsv
import pandas as pd
import pyarrow as pa
import msal
import os
import logging
import json
from pathlib import Path  # Import Path for directory handling
from download_pbi_xmla.ssas_api import set_conn_string, get_DAX

logging.basicConfig(level=logging.DEBUG)

def save_data_chunked(table, file_name, file_format, chunk_number):
    """
    Save data in chunks to separate files.
    """
    try:
        chunk_file_name = f"{file_name}_chunk_{chunk_number}"  # Create a unique file name for each chunk
        
        if file_format == 'parquet':
            pq.write_table(table, chunk_file_name + '.parquet')
            logging.info(f"Chunk {chunk_number} saved as {chunk_file_name}.parquet")
        elif file_format == 'csv':
            df = table.to_pandas()
            df.to_csv(chunk_file_name + '.csv', index=False)
            logging.info(f"Chunk {chunk_number} saved as {chunk_file_name}.csv")
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    except Exception as e:
        logging.error(f"Failed to save chunk {chunk_number} in format {file_format}.")
        logging.error(str(e))

def fetch_and_save_query(query_template, conn_str, file_name, file_format='parquet', chunk_size=500):
    """
    Fetch data using the DAX query template and save it in chunks to separate files.
    """
    start_index = 0
    chunk_number = 1

    while True:
        # Format the query with dynamic start index and chunk size
        chunk_query = query_template.format(start_index=start_index, chunk_size=chunk_size)
        
        try:
            logging.info(f"Running DAX query for chunk {chunk_number} with start index {start_index}: {chunk_query}")
            table = get_DAX(conn_str, chunk_query)
            
            if table.num_rows == 0:
                # No more rows to fetch
                break

            # Save each chunk separately
            save_data_chunked(table, file_name, file_format, chunk_number)
            
            start_index += chunk_size  # Update start index for next chunk
            chunk_number += 1
        
        except Exception as e:
            logging.error(f"Failed to execute or save query for chunk {chunk_number} with start index {start_index}.")
            logging.error(str(e))
            break

def get_access_token(client_id, client_secret, tenant_id):
    authority_url = f"https://login.microsoftonline.com/{tenant_id}"
    app = msal.ConfidentialClientApplication(
        client_id,
        authority=authority_url,
        client_credential=client_secret
    )
    scopes = ["https://analysis.windows.net/powerbi/api/.default"]
    result = app.acquire_token_for_client(scopes)
    if "access_token" in result:
        logging.info("Token acquired successfully")
        return result["access_token"]
    else:
        logging.error("Failed to acquire token")
        raise ValueError("Failed to acquire token")

def fetch_dax_queries(config_file, path, client_id, client_secret, tenant_id):
    # Ensure the save path exists
    Path(path).mkdir(parents=True, exist_ok=True)

    with open(config_file, 'r') as file:
        config = json.load(file)

    chunk_size = config.get('chunk_size', 500)  # Fetch the chunk size from config, default to 500 if not specified

    token = get_access_token(client_id, client_secret, tenant_id)
    conn_str = f"Provider=MSOLAP;Data Source={config['server']};Initial Catalog={config['database']};Persist Security Info=True;Impersonation Level=Impersonate;Password={token}"

    logging.debug(f"Connection string: {conn_str}")

    # Extract user-defined parameters
    parameters = config.get("parameters", {})

    # Process DAX queries
    for query_info in config.get('dax_queries', []):
        # Replace placeholders in the DAX query with actual parameter values
        dax_query = query_info['query']
        for key, value in parameters.items():
            dax_query = dax_query.replace(f"{{{key}}}", value)

        output_file = query_info['output_file']
        file_format = query_info.get('format', 'parquet')  # Default to 'parquet' if not specified
        fetch_and_save_query(dax_query, conn_str, os.path.join(path, output_file), file_format, chunk_size)

def main():
    from dotenv import load_dotenv

    # Load environment variables from .env file
    load_dotenv()

    # Fetch secrets and other settings from environment variables
    CLIENT_ID = os.getenv('CLIENT_ID').strip()
    CLIENT_SECRET = os.getenv('CLIENT_SECRET').strip()
    TENANT_ID = os.getenv('TENANT_ID').strip()
    CONFIG_FILE = os.getenv('CONFIG_FILE').strip()
    SAVE_PATH = os.getenv('SAVE_PATH')

    if SAVE_PATH:
        SAVE_PATH = SAVE_PATH.strip()
    else:
        SAVE_PATH = ''  # Provide a default value or handle the absence appropriately

    # Debug print statements to verify environment variables
    logging.debug(f"CLIENT_ID: {CLIENT_ID}")
    logging.debug(f"CLIENT_SECRET: {'*' * len(CLIENT_SECRET) if CLIENT_SECRET else None}")
    logging.debug(f"TENANT_ID: {TENANT_ID}")
    logging.debug(f"Config File: {CONFIG_FILE}")
    logging.debug(f"Save Path: {SAVE_PATH}")

    try:
        fetch_dax_queries(
            config_file=CONFIG_FILE,
            path=SAVE_PATH,
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            tenant_id=TENANT_ID
        )
    except Exception as e:
        logging.error(f"Failed to run the main function: {str(e)}")

if __name__ == "__main__":
    main()
