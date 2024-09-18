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

def save_data(table, file_name, file_format):
    """
    Save the data in the specified format.
    """
    try:
        # Ensure the table is of the expected type
        if not isinstance(table, pa.Table):
            raise ValueError(f"Unexpected data type: {type(table)}. Expected pyarrow.Table.")

        if file_format == 'parquet':
            pq.write_table(table, file_name + '.parquet', compression='snappy')  # Use compression to save space
            logging.info(f"Data saved as {file_name}.parquet")
        elif file_format == 'csv':
            # Convert Arrow table to pandas DataFrame for CSV output
            df = table.to_pandas()
            # Write to CSV in chunks
            chunk_size = 100000  # Adjust the chunk size based on your system's memory capacity
            for start in range(0, len(df), chunk_size):
                df_chunk = df[start:start + chunk_size]
                mode = 'w' if start == 0 else 'a'  # Write the first chunk with 'w', append subsequent chunks
                header = start == 0  # Include header only in the first chunk
                df_chunk.to_csv(file_name + '.csv', index=False, mode=mode, header=header)
            logging.info(f"Data saved as {file_name}.csv in chunks.")
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    except Exception as e:
        logging.error(f"Failed to save data in format {file_format}.")
        logging.error(str(e))


def save_data_chunked(table, file_name, file_format, mode='a'):
    """
    Save data in chunks to the specified file format.
    """
    try:
        if file_format == 'parquet':
            # Append to existing Parquet file if it exists
            if mode == 'a' and os.path.exists(file_name + '.parquet'):
                existing_table = pq.read_table(file_name + '.parquet')
                combined_table = pa.concat_tables([existing_table, table])
                pq.write_table(combined_table, file_name + '.parquet')
            else:
                pq.write_table(table, file_name + '.parquet')
            logging.info(f"Data saved as {file_name}.parquet")
        elif file_format == 'csv':
            # Append to CSV file using pandas DataFrame
            df = table.to_pandas()
            if mode == 'a' and os.path.exists(file_name + '.csv'):
                df.to_csv(file_name + '.csv', mode='a', header=False, index=False)
            else:
                df.to_csv(file_name + '.csv', mode='w', header=True, index=False)
            logging.info(f"Data saved as {file_name}.csv")
        else:
            raise ValueError(f"Unsupported file format: {file_format}")
    except Exception as e:
        logging.error(f"Failed to save data in format {file_format}.")
        logging.error(str(e))

def fetch_and_save_query(query, conn_str, file_name, file_format='parquet'):
    """
    Fetch data using the DAX query and save it to the specified file format.
    """
    try:
        logging.info(f"Running DAX query: {query}")
        table = get_DAX(conn_str, query)
        logging.info(f"DAX query executed successfully!")
        
        # Save the data in chunks
        save_data_chunked(table, file_name, file_format)
    except Exception as e:
        logging.error(f"Failed to execute or save query: {query}.")
        logging.error(str(e))


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
        fetch_and_save_query(dax_query, conn_str, os.path.join(path, output_file), file_format)


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
