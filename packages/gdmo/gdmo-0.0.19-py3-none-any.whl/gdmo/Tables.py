import json
import os
import re
from datetime import datetime
from pyspark.sql.functions import lit
from delta.tables import *

class Landing:
    """
        A class for landing API ingests and other data into Azure Data Lake Storage (ADLS).
    
        Attributes:
        - database (str): The name of the database where the data should be landed.
        - target (str): The location name used to folderize the landed data within the database folder.
        - filename (str): The filename with extension for the landed data.
        - catalog (str): The catalog used to identify the environment (e.g., dev, fq, prd).
        - container (str): The ADLS container name.
        - location (str): The ADLS folder path for landing the data.
        - destination (str): The full destination path for landing the data.
        - content_type (str): The content type of the data (default: JSON).
        - timestamp (datetime): The timestamp of the landing operation.
    
        Methods:
        - get_folder(): Returns the location chosen for the landed data.
        - get_file_path(): Returns the complete file path.
        - set_destination(destination): Sets the destination path for landing the data.
        - set_content_type(content_type): Sets the content type for the data.
        - set_autorename(rename=True): Change the autorename that happens when adding a file to landing.
        - set_static_col(cols=[]): Set additional static columns for the bronze layer table.
        - set_config(data): Store the config on the ingested data for the bronze layer.
        - put_json_content(json_data): Stores JSON data into a JSON file at the specified location with the given filename.
        - put_bronze(loadtype, parameters=None): Store the landed data into the designated bronze layer table.
    """

    def __init__(self, spark, dbutils, database, target, filename = '', catalog = 'hive_metastore'):
        """
        Initializes a Landing object on the specified object.

        Args:
        - database (str): Required. DB Name that is used as primary segmentor in the landing zone.
        - target   (str): Required. Location name that is used to folderize the landed data within the database folder.
        - catalog  (str): Optional. Defaults to hive_metastore but should be used with UC to identify dev/fq/prd
        """
        
        self._database      = database # Required. the bronze database  that the data should be landed in
        self._target        = target   # Required. the bronze tablename that the data should be landed in
        self._catalog       = catalog  # Optional. the bronze catalog   that the data should be landed in
        self._dbutils       = dbutils  # Optional. the bronze catalog   that the data should be landed in
        self._spark         = spark    # Optional. the bronze catalog   that the data should be landed in
        self._filename      = self._clean_filename(filename)  # Optional. the filename with extension that the data should be landed in
        self._container     = 'bidl'
        self._location      = os.environ.get("ADLS").format(container=self._container,path=self._target)
        self._destination   = f'{self._location}{self._target.replace("__","/").lower()}'
        self._joincolumns   = None
        self._bronze_table  = self._database+'.'+self._target
        self._static_cols   = []
        self._loadtype      = 'append' #By default just add it into bronze
        
        # Ensure the specified location exists, create it if it doesn't
        if not os.path.exists(self._location):
            print('Folder path did not exist yet. Making the dir now.')
            os.makedirs(self._location, exist_ok=True)

        # Construct the full file path
        self._file_path = os.path.join(self._location, self._filename)

        self._content_type  = 'parquet'
        self._timestamp     = datetime.now()
        
        print(f'location: {self._location} | file: {self._filename}')
    
    def _clean_filename(self, filename):
        # Remove illegal characters from the filename
        cleaned_filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        return cleaned_filename

    def _infer_table(self, df):
        # Infer the schema from the DataFrame
        try:
            df.createOrReplaceTempView("temp_view")
            inferred_schema = self._spark.sql(f"DESCRIBE temp_view").toPandas()

            # Create Delta table with the inferred schema
            self._spark.sql(f"CREATE TABLE {self._bronze_table} USING DELTA AS SELECT * FROM temp_view")
            return True

        except Exception as e:
            raise Exception(f"Delta table creation failed with Error: {e}")

    def set_static_col(self, cols = {}):
        """
        Set additional static columns for the bronze layer table.
        
        Args:
        - cols (list): List of static columns to be added to the bronze layer table.
        """
        print(f'Added columns to bronze layer table: {cols}')
        self._static_cols.append(cols)
        
        return self

    def set_config(self, data):
        """
        Store the config on the ingested data that allows us to put it to bronze layer
        """

        self._loadtype    = data['loadtype']
        self._joincolumns = data['join']

        return self
  
    def put_json_content(self, json_data):
        """
        Stores JSON data into a JSON file at the specified location with the given filename.

        Args:
        - json_data (dict): The JSON data to be stored in the file.

        Returns:
        str: The full path of the saved JSON file.
        """
        try:

            # Get the row count of the JSON data
            row_count = len(json_data)

            # Write the JSON data to the file
            json_string = json.dumps(json_data, indent=4)
            
            #parquetfile     = self._file_path.replace('.json', '.parquet')
            #parquetfilename = self._filename.replace( '.json', '.parquet')
            try:
                # Write the JSON data to the file in ADLS Gen2
                df = self._spark.read.json(self._spark.sparkContext.parallelize([json_string]))
                # Write the DataFrame to a Parquet file on ADLS Gen2
                df.write.mode("overwrite").parquet(self._file_path)
                #self._dbutils.fs.put(self._file_path, json_string, overwrite=True)
                print("JSON data successfully written to the file.")
            except Exception as e:
                # Handle any exceptions that occur during the file write operation
                error_message = f"Error writing JSON data to file: {e}"
                print(error_message)

            #with open(self._file_path, 'w') as file:
            #    json.dump(json_data, file, indent=4)
            #time.sleep(10)

            # Check if the file was created
            files = self._dbutils.fs.ls(self._location)
            found_files = [file_info.name for file_info in files]

            #if parquetfilename in found_files:
            #return self._file_path, row_count
            #else:
            #    found_files_str = ", ".join(found_files)
            #    raise FileNotFoundError(f"The file was not found in the specified directory. looking for file {parquetfilename}, but files in the listed directory: {found_files_str}")
            
            return self
        
        except (OSError, IOError) as e:
            # Handle file I/O errors
            error_message = f"Error occurred while writing JSON data to file: {e}"
            raise IOError(error_message)
        except Exception as e:
            # Handle other exceptions
            error_message = f"An error occurred: {e}"
            raise Exception(error_message)
   
    def put_bronze(self):
        """
        Store the landed data into the designated bronze layer table.

        Parameters:
        None

        Returns:
        - bool: True if the data is successfully stored in the bronze layer table.

        Raises:
        - ValueError: If any errors occur during the data loading process.
        """

        # Load the Parquet file thats landed into a Spark DataFrame
        try:
            df = self._spark.read.parquet(self._file_path)
            stage = df.withColumn('delta__load_date', lit(datetime.now()))\
                      .withColumn('delta__deleted',   lit(0))\
                      .select("delta__load_date", "delta__deleted", *df.columns)
        except Exception as e:
            raise ValueError(f"Error reading file: {self._file_path}", e)

        # Check if any additional static columns are required in bronze, and add them to the dataframe
        if self._static_cols:
            try:
                for static_col in self._static_cols:
                    for col, value in static_col.items():
                        stage = stage.withColumn(col, lit(value))
            except Exception as e:
                raise Exception(f"Error adding static columns to dataframe: {static_col}")

        # Make sure the delta bronze table is there and working
        print(f'Table name: {self._bronze_table}')

        table_exists = self._spark.catalog.tableExists(self._bronze_table)

        if not table_exists:
            print(f'Table {self._bronze_table} does not exist; inferring the schema and trying to create it.')
            self._infer_table(stage)
        else:
            delta_table = DeltaTable.forName(self._spark, self._bronze_table)
            delta_schema = delta_table.toDF().schema
            stage_schema = stage.schema

            if delta_schema != stage_schema:
                # Find the exact schema differences
                delta_fields = set((f.name, f.dataType) for f in delta_schema)
                stage_fields = set((f.name, f.dataType) for f in stage_schema)

                missing_fields = delta_fields - stage_fields
                extra_fields = stage_fields - delta_fields

                if missing_fields or extra_fields:
                    error_message = "Schema mismatch between stage DataFrame and Delta table.\n"
                    if missing_fields:
                        error_message += "Fields missing in stage DataFrame: {}\n".format(missing_fields)
                    if extra_fields:
                        error_message += "Extra fields in stage DataFrame: {}\n".format(extra_fields)
                    raise ValueError(error_message)

        if self._loadtype =="overwrite":
            #Truncate and overwrite
            try:
                stage.write.mode("overwrite").saveAsTable(self._bronze_table)
            except Exception as e:
                raise ValueError(f"Error overwriting data: {e}")

        elif self._loadtype =="append":
            #Just append the data with a new delta__load_date
            try:
                stage.write.mode("append").saveAsTable(self._bronze_table)
            except Exception as e:
                raise ValueError(f"Error appending data: {e}")

        elif self._loadtype =="merge":
            #Parameters are then required
            if self._joincolumns == None:
                raise ValueError(f'No parameters added. A Merge load will need to know which values are used as join condition.')

            joinstring = ' AND '.join([f's.{cond} = f.{cond}' for cond in self._joincolumns])
            try:
                final = DeltaTable.forName(self._spark, self._bronze_table)
                final.alias('f') \
                    .merge(stage.alias('s'),joinstring) \
                    .whenMatchedUpdateAll() \
                    .whenNotMatchedInsertAll() \
                    .execute()
            except Exception as e:
                raise ValueError(f"Error merging data: {e}")

        else:
            raise ValueError(f'Loadtype {self._loadtype} is not supported.')

        return True
   
    def get_folder(self):
        """
        Returns the location it has chosen for the landed data

        Args:
        - None

        Returns:
        - Folder location on ADLS
        """
        return self._location
    
    def get_file_path(self):
        """
        Returns the complete file path

        Args:
        - None

        Returns:
        - file path
        """
        return self._file_path

    def set_bronze(self, table):
        """
        Sets the destination path for landing the data.

        Args:
        - destination (str): The ADLS folder path for the landing.
        """
        if not table.startswith("bronze__"):
            table = "bronze__" + table
        self._bronze_table = self._database+'.'+table
        return self

    def set_content_type(self, content_type):
        """
        Sets the content type for the data.

        Args:
        - content_type (str): The content type (JSON, CSV, XLSX, PARQUET).
        """
        self._content_type = content_type
        return True
    
    def set_autorename(self, rename = True):
        """
        Optional function to change the autorename that happens when adding a file to landing. By default the ingested filename is changed (or inferred) and includes the loading timestamp as part of the filename

        Args:
        - rename (bool): Required. True / False flag.
        """

        return True

class Delta:
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
            dbutils = DBUtils(self._spark)
        
        else:
            
            import IPython
            dbutils = IPython.get_ipython().user_ns["dbutils"]
        
        return dbutils