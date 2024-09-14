# GDMO native classes for standardized interaction with data objects within Azure Databricks

This custom library allows our engineering team to use standardized packages that strip away a load of administrative and repetitive tasks from their daily object interactions. The current classes supported (V0.1.0) are:

## API - APIRequest
Class to perform a standard API Request using the request library, which allows a user to just add their endpoint / authentication / method data, and get the data returned without the need of writing error handling or need to understand how to properly build a request. 

## Tables - Landing
Class to land a dataframe or csv file to the databricks landing zone, and optionally convert this to the bronze layer data. Just say where to store it, and the class will take care of it with error handling associated and a normalized routine is followed. 

## Tables - Delta
No longer one needs to write a twelve-command notebook to create a table. Call this class once and see it happen. 

## Forecast - Forecast
Standardized way of forecasting a dataset. Input a dataframe with a Series, a Time, and a Value column, and see the function automatically select the right forecasting model and generate an output. 