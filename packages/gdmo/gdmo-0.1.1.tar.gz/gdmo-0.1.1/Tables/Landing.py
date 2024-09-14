import json
import os
from datetime import datetime
import re
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
            raise ValueError(f'Loadtype {loadtype} is not supported.')

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

