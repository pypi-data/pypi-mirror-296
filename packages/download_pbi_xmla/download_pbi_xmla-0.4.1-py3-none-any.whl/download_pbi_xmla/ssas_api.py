#ssas_api.py
import pyarrow as pa
import pyarrow.parquet as pq
import numpy as np
import platform
from functools import wraps
from pathlib import Path
import logging
import warnings
from datetime import datetime  # Ensure datetime is imported

logger = logging.getLogger(__name__)

# Platform check
if platform.system() == "Windows":
    try:
        import clr  # name for pythonnet
    except ImportError:
        msg = """
        Could not import 'clr', install the 'pythonnet' library. 
        For conda, `conda install -c pythonnet pythonnet`
        """
        raise ImportError(msg)
else:
    clr = None
    logger.warning("This package requires 'pythonnet' and .NET assemblies to work on Windows.")

def _load_assemblies(amo_path=None, adomd_path=None):
    if clr is None:
        raise EnvironmentError("This function can only be run on Windows with 'pythonnet' installed.")

    root = Path(r"C:\Windows\Microsoft.NET\assembly\GAC_MSIL")
    if amo_path is None:
        amo_path = str(
            max((root / "Microsoft.AnalysisServices.Tabular").iterdir())
            / "Microsoft.AnalysisServices.Tabular.dll"
        )
    if adomd_path is None:
        adomd_path = str(
            max((root / "Microsoft.AnalysisServices.AdomdClient").iterdir())
            / "Microsoft.AnalysisServices.AdomdClient.dll"
        )

    logger.info("Loading .Net assemblies...")
    clr.AddReference("System")
    clr.AddReference("System.Data")
    clr.AddReference(amo_path)
    clr.AddReference(adomd_path)

    global System, DataTable, AMO, ADOMD

    import System
    from System.Data import DataTable
    import Microsoft.AnalysisServices.Tabular as AMO
    import Microsoft.AnalysisServices.AdomdClient as ADOMD

    logger.info("Successfully loaded these .Net assemblies: ")
    for a in clr.ListAssemblies(True):
        logger.info(a.split(",")[0])

def _assert_dotnet_loaded(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if platform.system() != "Windows":
            raise EnvironmentError("This function can only be run on Windows with 'pythonnet' installed.")
        
        amo_path = kwargs.pop("amo_path", None)
        adomd_path = kwargs.pop("adomd_path", None)
        try:
            type(DataTable)
        except NameError:
            logger.warning(".Net assemblies not loaded and imported, doing so now...")
            _load_assemblies(amo_path=amo_path, adomd_path=adomd_path)
        return func(*args, **kwargs)
    return wrapper

@_assert_dotnet_loaded
def set_conn_string(server, db_name, username, password):
    if not db_name:
        raise ValueError("Database name (Initial Catalog) must be specified.")
    
    conn_string = (
        "Provider=MSOLAP;Data Source={};Initial Catalog={};User ID={};"
        "Password={};Persist Security Info=True;Impersonation Level=Impersonate".format(
            server, db_name, username, password
        )
    )
    return conn_string

@_assert_dotnet_loaded
def get_DAX(connection_string, dax_string):
    table = _get_DAX(connection_string, dax_string)
    arrow_table = _parse_DAX_result(table)
    return arrow_table

def _get_DAX(connection_string, dax_string) -> "DataTable":
    dataadapter = ADOMD.AdomdDataAdapter(dax_string, connection_string)
    table = DataTable()
    logger.info("Getting DAX query...")
    dataadapter.Fill(table)
    logger.info(f"DAX query successfully retrieved with {table.Rows.Count} rows.")
    
    # Log the number of columns and their types
    for col in table.Columns.List:
        logger.debug(f"Column: {col.ColumnName}, DataType: {col.DataType.FullName}")

    return table

def _parse_DAX_result(table: "DataTable") -> pa.Table:
    cols = [c for c in table.Columns.List]
    rows = []
    for r in range(table.Rows.Count):
        row = [table.Rows[r][c] for c in cols]
        rows.append(row)

    arrays = []
    for i, col in enumerate(cols):
        column_name = col.ColumnName
        data_type = col.DataType.FullName
        data = [row[i] if not isinstance(row[i], System.DBNull) else None for row in rows]

        logger.debug(f"Processing column '{column_name}' with data type '{data_type}'")

        try:
            if data_type == "System.DateTime":
                # Convert to datetime
                data = [datetime.strptime(x.ToString('s'), "%Y-%m-%dT%H:%M:%S") if x is not None else None for x in data]
                arrays.append(pa.array(data, type=pa.timestamp('s')))
            elif data_type == "System.Int64":
                # Convert to int64
                arrays.append(pa.array(data, type=pa.int64()))
            elif data_type == "System.Double":
                # Convert to float64
                arrays.append(pa.array(data, type=pa.float64()))
            elif data_type == "System.Boolean":
                # Convert boolean to string ("True" or "False") or directly to pyarrow boolean type
                bool_data = [bool(x) if x is not None else None for x in data]
                arrays.append(pa.array(bool_data, type=pa.bool_()))
            else:
                # Convert to string
                str_data = [str(x) if x is not None else None for x in data]
                arrays.append(pa.array(str_data, type=pa.string()))
        except Exception as e:
            logger.error(f"Failed to convert column '{column_name}' to {data_type}: {str(e)}")
            raise

    # Check for empty arrays
    if not arrays:
        logger.error("No data was parsed from the DataTable.")
        raise ValueError("No data was parsed from the DataTable.")

    schema = pa.schema([(col.ColumnName, arrays[i].type) for i, col in enumerate(cols)])
    arrow_table = pa.Table.from_arrays(arrays, schema=schema)

    return arrow_table

@_assert_dotnet_loaded
def process_database(connection_string, refresh_type, db_name):
    process_model(
        connection_string=connection_string,
        item_type="model",
        refresh_type=refresh_type,
        db_name=db_name,
    )

@_assert_dotnet_loaded
def process_table(connection_string, table_name, refresh_type, db_name):
    process_model(
        connection_string=connection_string,
        item_type="table",
        item=table_name,
        refresh_type=refresh_type,
        db_name=db_name,
    )

@_assert_dotnet_loaded
def process_model(connection_string, db_name, refresh_type="full", item_type="model", item=None):
    assert item_type.lower() in ("table", "model"), f"Invalid item type: {item_type}"
    if item_type.lower() == "table" and not item:
        raise ValueError("If item_type is table, must supply an item (a table name) to process")

    AMOServer = AMO.Server()
    logger.info("Connecting to database...")
    AMOServer.Connect(connection_string)

    refresh_dict = {"full": AMO.RefreshType.Full}

    db = AMOServer.Databases[db_name]

    if item_type.lower() == "table":
        table = db.Model.Tables.Find(item)
        table.RequestRefresh(refresh_dict[refresh_type])
    else:
        db.Model.RequestRefresh(refresh_dict[refresh_type])

    op_result = db.Model.SaveChanges()
    if op_result.Impact.IsEmpty:
        logger.info("No objects affected by the refresh")

    logger.info("Disconnecting from Database...")
    AMOServer.Disconnect()
