import os
import re
import requests
import json
import tempfile

class IDeltaTable:
    """
    A class for creating and managing Delta tables in Azure Databricks.

    Attributes:
    - db_name (str): Required. The name of the database containing the table.
    - table_name (str): Required. The name of the table.
    - spark (pyspark.sql.SparkSession): Required. The SparkSession object to use for interacting with the table.
    - columns (list of dictionaries): Optional. A list of dictionaries, where each dictionary contains the column name, data type, and an optional comment.
    - options (dict): Optional. A dictionary containing the table options.
    - primary_key (str): Optional. The name of the primary key column.
    - partitioning (str): Optional. The name of the partitioning column.

    Methods:
    - set_columns(columns): Sets the column list for the table.
    - set_comment(comment): Sets the comment for the table.
    - set_options(options): Sets the options for the table.
    - set_primary_key(primary_key): Sets the primary key for the table.
    - set_partitioning(partitioning): Sets the partitioning for the table.
    - add_column(column_name, data_type, comment): Adds a single column to the table.
    - drop_existing(): Drops the existing table and removes it from the ADFS file system.
    - save(): Saves the table to the specified database and location.
    """
    def __init__(self, db_name, table_name, spark, catalog = 'hive_metastore'):
        """
        Initializes a DeltaTable object with the specified database name, table name, and SparkSession object.

        Args:
        - db_name (str): Required. The name of the database containing the table.
        - table_name (str): Required. The name of the table.
        - spark (pyspark.sql.SparkSession): Required. The SparkSession object to use for interacting with the table.
        """
        # Check if the database exists
        databases = [db.name for db in spark.catalog.listDatabases()]
        if db_name not in databases:
            raise ValueError(f"Database {db_name} not found in the SparkSession.")

        # Check if the table name is valid
        if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
            raise ValueError(f"Invalid table name: {table_name}. Table names can only contain alphanumeric characters and underscores.")

        # Check if the spark variable is a SparkSession object
        if not isinstance(spark, SparkSession):
            raise ValueError("The spark variable must be a SparkSession object.")

        self._catalog = catalog
        self._db_name = db_name
        self._table_name = table_name
        self._spark = spark
        self._columns = []
        self._options = {}
        self._primary_key = None
        self._partitioning = None

        location = os.environ.get("ADLS").format(container="bidl", path=self._db_name)
        self._table_location = f'{location}/{self._table_name.replace("__", "/").lower()}'
          
    def set_columns(self, columns):
        """
        Sets the column list for the table.

        Args:
        - columns (list of dictionaries): Required. A list of dictionaries, where each dictionary contains the column name, data type, and an optional comment.

        Returns:
        - self (DeltaTable): Returns the DeltaTable object.
        """
        # Check if columns is a list of dictionaries
        if not isinstance(columns, list) or not all(isinstance(col, dict) for col in columns):
            raise ValueError("The columns argument must be a list of dictionaries.")

        # Check if each dictionary in columns contains the required keys
        for col in columns:
            if not all(key in col for key in ["name", "data_type"]):
                raise ValueError("Each dictionary in the columns argument must contain the 'name' and 'data_type' keys.")

        # Add blank comments if not present in the dictionary
        for col in columns:
            if "comment" not in col:
                col["comment"] = ""

        self._columns = columns
        return self
        
    def set_comment(self, comment):
        """
        Sets the comment for the table.

        Args:
        - comment (string): Required. A string containing the table comment.

        Returns:
        - self
        """
        if not isinstance(comment, str) or len(comment.strip()) < 20:
            raise ValueError("The comment argument must be a populated string of at least 20 characters long.")
        self._comment = comment
        return self

    def set_options(self, options):
        """
        Sets the options for the table.

        Args:
        - options (dict): Required. A dictionary containing the table options.

        Returns:
        - None
        """
        self._options = options
        return self
        
    def set_primary_key(self, primary_key):
        """
        Sets the primary key for the table.

        Args:
        - primary_key (str): Required. The name of the primary key column.

        Returns:
        - None
        """
        self._primary_key = primary_key
        return self
        
    def set_partitioning(self, partitioning):
        """
        Sets the partitioning for the table.

        Args:
        - partitioning (str): Required. The name of the partitioning column.

        Returns:
        - None
        """
        self._partitioning = partitioning
        return self
        
    def add_column(self, column):
        """
        Adds a column to the table.

        Args:
        - column (dict): Required. A dictionary containing the column name, data type, and comment.

        Returns:
        - self
        """
        # Check if the column is in the right format
        if not isinstance(column, dict) or not all(key in column for key in ["name", "data_type", "comment"]):
            raise ValueError("The column argument must be a dictionary with 'name', 'data_type', and 'comment' keys.")

        # Check if the column name is at least 3 characters long
        if len(column["name"].strip()) < 3:
            raise ValueError("The 'name' value in the column argument must be at least 3 characters long.")

        # Check if the comment is not identical to the column name
        if column["name"].strip().lower() == column["comment"].strip().lower():
            raise ValueError("The 'comment' value in the column argument must not be identical to the column name.")

        # Check if the comment is at least 10 characters long
        if len(column["comment"].strip()) < 10:
            raise ValueError("The 'comment' value in the column argument must be at least 10 characters long.")
        
        # Check if the column already exists in the table
        existing_columns = [col["name"] for col in self._columns]
        if column["name"] in existing_columns:
            raise ValueError(f"The column '{column['name']}' already exists in the table.")

        # Alter the table to add the column
        alter_table_query = f"ALTER TABLE {self._catalog}.{self._db_name}.{self._table_name} ADD COLUMN {column['name']} {column['data_type']} COMMENT '{column['comment']}'"
        self._spark.sql(alter_table_query)

        # Add the column to the list of columns
        self._columns.append(column)

        return self

    def drop_existing(self):
        """
        Drops the existing table and removes it from the ADFS file system.

        Returns:
        - None
        """
        
        try:
            drop_sql_str = f"DROP TABLE IF EXISTS {self._db_name}.{self._table_name}"
            self._spark.sql(drop_sql_str)
                        
            dbutils = self._get_dbutils()

            dbutils.fs.rm(self._table_location, True)
            return self
        except Exception as e:
            print(f'Error during Table Drop: {e}')
            return False
            
    def create_table(self):
        """
        Saves the table to the specified database.

        Returns:
        - None
        """
        columns = ", ".join([f"{col['name']} {col['data_type']} COMMENT '{col['comment']}'" for col in self._columns])
        options = ", ".join([f"{key} = '{value}'" for key, value in self._options.items()])
        primary_key = f"tblproperties('primary_key'='{self._primary_key}')" if self._primary_key else ""
        partitioning = f"PARTITIONED BY ({self._partitioning})" if self._partitioning else ""
        table_comment = f"COMMENT {self._comment}" if self._comment else ""
        
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self._catalog}.{self._db_name}.{self._table_name} (
                {columns}
            )
            USING DELTA
            location "{self._table_location}"
            {partitioning}
            {primary_key}
            {options}
            {table_comment}
        """
        try:
            self._spark.sql(create_table_query)
            self._show()
        except Exception as e:
            if "Table already exists" in str(e):
                existing_table_desc = self._spark.sql(f"describe detail {self._db_name}.{self._table_name}").toPandas()
                existing_table_desc_str = "\n".join([f"{row['col_name']}\t{row['data_type']}\t{row['comment']}" for _, row in existing_table_desc.iterrows()])
                error_msg = f"Table {self._db_name}.{self._table_name} already exists. Please add the 'drop_existing()' function to the create statement if you want to overwrite the existing table.\n\nExisting table description:\n{existing_table_desc_str}"
            else:
                error_msg = f"Error during table save: {e}"
            raise Exception(error_msg)
            
    def create_table_if_not_exists(self):
        """
        Saves the table to the specified database.

        Returns:
        - None
        """
        columns = ", ".join([f"{col['name']} {col['data_type']} COMMENT '{col['comment']}'" for col in self._columns])
        options = ", ".join([f"{key} = '{value}'" for key, value in self._options.items()])
        primary_key = f"tblproperties('primary_key'='{self._primary_key}')" if self._primary_key else ""
        partitioning = f"PARTITIONED BY ({self._partitioning})" if self._partitioning else ""
        table_comment = f"COMMENT {self._comment}" if self._comment else ""
        
        create_table_query = f"""
            CREATE TABLE IF NOT EXISTS {self._db_name}.{self._table_name} (
                {columns}
            )
            USING DELTA
            location "{self._table_location}"
            {partitioning}
            {primary_key}
            {options}
            {table_comment}
        """
        try:
            self._spark.sql(create_table_query)
            self._show()
        except Exception as e:
            print(f"Table {self._db_name}.{self._table_name} already exists.")

    def _show(self):
        """
        Returns a DataFrame object containing the description of the table.

        Returns:
        - df (pyspark.sql.DataFrame): A DataFrame object containing the description of the table.
        """
        describe_sql_str = f"DESCRIBE DETAIL {self._db_name}.{self._table_name}"
        return self._spark.sql(describe_sql_str)

    def get_data_from_sharepoint(self, file_path):

        #To be implementen

        return self

    def _get_dbutils(self):
        """
        Private function to get a dbutils instance available allowing the drop_existing function to drop a table from ADLS

        Returns:
        - dbutils object
        """
        dbutils = None
        
        if self._spark.conf.get("spark.databricks.service.client.enabled") == "true":
            
            from pyspark.dbutils import DBUtils
            dbutils = DBUtils(spark)
        
        else:
            
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]
        
        return dbutils
    
class IRestAPI:
    def __init__(self, url):
        """
        Initializes a RestAPI object with the specified url.

        Args:
        - url (str): Required. URL to send the request to.
        """
        if not url.startswith('http'):
            raise ValueError('Invalid URL. Must start with http:// or https://')
        self._url       = url # Required. URL to send the request to.
        self._method    = 'POST' # Required. Identifies the method used in the call
        self._headers   = {'Content-Type':'application/json'} # Optional. A dictionary of HTTP headers to send to the specified url.
        self._json      = None
        self._data      = None
        self._params    = {} # Optional. A dictionary of query parameters to send with the request.
        self._response  = ''

    def set_header(self, key, value):
        """
        Sets the specified key-value pair in the HTTP headers dictionary.
   
        Args:
        - key (str): Required. The key to set in the headers dictionary.
        - value (str): Required. The value to set for the specified key.

        Returns:
        - bool: True if the key-value pair was successfully set in the headers dictionary.
        """
        if not isinstance(key, str):
            raise TypeError('Header key must be a string')
        if not isinstance(value, str):
            raise TypeError('Header value must be a string')
        self._headers[key] = value
        return self

    def set_auth(self, value):
        """
        Sets the specified HTTP authentication tuple.

        Args:
        - value (tuple): Required. A tuple to enable a certain HTTP authentication.

        Returns:
        - bool: True if the authentication tuple was successfully set.
        """
        self._auth = value
        return self

    def set_param(self, key, value):
        """
        Sets the specified key-value pair in the parameters dictionary.

        Args:
        - key (str): Required. The key to set in the parameters dictionary.
        - value (str): Required. The value to set for the specified key.

        Returns:
        - bool: True if the key-value pair was successfully set in the parameters dictionary.
        """
        self._params[key] = value
        return self

    def set_content_type(self, value):
        """
        Sets the specified content type in the HTTP headers dictionary.

        Args:
        - value (str): Required. The content type to set in the headers dictionary.

        Returns:
        - bool: True if the content type was successfully set in the headers dictionary.

        Raises:
        - ValueError: If the specified content type is invalid.
        """
        content_types = [
            'application/vnd.android.package-archive',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'application/vnd.oasis.opendocument.graphics',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.mozilla.xul+xml',
            'video/mpeg',
            'video/mp4',
            'video/quicktime',
            'video/x-ms-wmv',
            'video/x-msvideo',
            'video/x-flv',
            'video/webm',
            'text/css',
            'text/csv',
            'text/html',
            'text/javascript',
            'text/plain',
            'text/xml',
            'multipart/mixed',
            'multipart/alternative',
            'multipart/related',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/x-icon',
            'image/vnd.djvu',
            'image/svg+xml',
            'audio/mpeg',
            'audio/x-ms-wma',
            'audio/vnd.rn-realaudio',
            'audio/x-wav',
            'application/java-archive',
            'application/EDI-X12',
            'application/EDIFACT',
            'application/javascript',
            'application/octet-stream',
            'application/ogg',
            'application/pdf',
            'application/xhtml+xml',
            'application/x-shockwave-flash',
            'application/json',
            'application/ld+json',
            'application/xml',
            'application/zip',
            'application/x-www-form-urlencoded'
        ]
        
        if value not in content_types:
            raise ValueError(f"Invalid content type: {value}")
        
        self._headers['Content-Type'] = value
        return self

    def set_method(self, method):
        """
        Sets the specified HTTP method.

        Args:
        - method (str): Required. The HTTP method to set.

        Returns:
        - bool: True if the HTTP method was successfully set.
        """
        if method not in ["POST", "GET", "PATCH", "PUT"]:
            raise ValueError("Invalid HTTP method. Only POST, GET, PATCH, and PUT methods are allowed.")
        self._method = method        
        return self

    def set_data(self, data):
        """
        Sets the specified data to be sent in the HTTP request.

        Args:
        - data (dict, list of tuples, bytes, or file object): Required. The data to send in the HTTP request.

        Returns:
        - bool: True if the data was successfully set.
        """
        self._data = data
        return self

    def set_json(self, json_data):
        """
        Sets the specified JSON data to be sent in the HTTP request.

        Args:
        - json_data (str): Required. The JSON data to send in the HTTP request.

        Returns:
        - bool: True if the JSON data was successfully set.

        Raises:
        - ValueError: If the specified JSON data is invalid.
        """
        try:
            json.loads(json_data)
        except ValueError:
            raise ValueError("Invalid JSON data")

        self._json = json_data
        return self

    def make_request(self):
        """
        Sends the HTTP request using the specified parameters.

        Returns:
        - RestAPI: The RestAPI object.
        """
        data = self._data if self._data else None
        json = self._json if self._json else None
        params = self._params if self._params else None

        try:
            if self._method == "POST":
                self._response = requests.post(self._url, headers=self._headers, json=json, data=data, timeout=7200)
            elif self._method == "GET":
                self._response = requests.get(self._url, headers=self._headers, params=params, timeout=7200)
            #elif self._method == "DELETE":
            #    self._response = requests.delete(self._url, headers=self._headers, data=data)
            #elif self._method == "PATCH":
            #    self._response = requests.patch(self._url, headers=self._headers, data=data)
            #elif self._method == "PUT":
            #    self._response = requests.put(self._url, headers=self._headers, data=data)
            else:
                raise ValueError(f"Method {self._method} not supported")

            self._response.raise_for_status()

        except requests.exceptions.RequestException as e:
            message  = f"HTTP error: {e}\n"
            message += f"Headers: {self._headers}\n"
            message += f"Method: {self._method}\n"
            message += f"Data: {data}\n"
            message += f"Params: {params}\n"
            message += f"URL: {self._url}\n"
            raise requests.exceptions.HTTPError(message)

        return self

    def get_json_response(self):
        """
        Returns the JSON response from the HTTP request.

        Returns:
        - dict: The JSON response from the HTTP request.
        """
        response = self._response
        try:
            json_response = response.json()
        except ValueError:
            raise ValueError('Response is not valid JSON')
        return json_response
    
    def get_raw_response(self):
        return self._response

    def store_json_response(self):
        """
        Stores the JSON response to a temporary file.

        Returns:
        - str: The path to the temporary file.
        """
        json_response = self.get_json_response()
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as f:
            f.write(json.dumps(json_response))
            file_path = f.name
        return file_path