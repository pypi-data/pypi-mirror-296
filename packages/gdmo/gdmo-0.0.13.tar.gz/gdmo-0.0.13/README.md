# gdmo

[![PyPI](https://img.shields.io/pypi/v/gdmo.svg)](https://pypi.org/project/gdmo/)
[![Tests](https://github.com/StephanKuiper-Insight/gdmo/actions/workflows/test.yml/badge.svg)](https://github.com/StephanKuiper-Insight/gdmo/actions/workflows/test.yml)
[![Changelog](https://img.shields.io/github/v/release/StephanKuiper-Insight/gdmo?include_prereleases&label=changelog)](https://github.com/StephanKuiper-Insight/gdmo/releases)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/StephanKuiper-Insight/gdmo/blob/main/LICENSE)


# GDMO native classes for standardized interaction with data objects within Azure Databricks

This custom library allows our engineering team to use standardized packages that strip away a load of administrative and repetitive tasks from their daily object interactions. The current classes supported (V0.1.0) are: 


# Installation

Install this library using `pip`:
```bash
pip install gdmo
```
# Usage

## Forecast - Forecast
Standardized way of forecasting a dataset. Input a dataframe with a Series, a Time, and a Value column, and see the function automatically select the right forecasting model and generate an output. 

Example usage:

```python
from gdmo import TimeSeriesForecast
forecaster = TimeSeriesForecast(spark, 'Invoiced Revenue')\
                    .set_columns('InvoiceDate', 'ProductCategory', 'RevenueUSD')\
                    .set_forecast_length(forecast_length)\
                    .set_last_data_point(lastdatamonth)\
                    .set_input(df)\
                    .set_growth_cap(0.02)\
                    .set_use_cap_growth(True)\
                    .set_modelselection_breakpoints(12, 24)\
                    .set_track_outcome(False)\
                    .build_forecast()

forecaster.inspect_forecast()
```

## API - APIRequest
Class to perform a standard API Request using the request library, which allows a user to just add their endpoint / authentication / method data, and get the data returned without the need of writing error handling or need to understand how to properly build a request. 

Example usage:

```python

request = APIRequest(uri)\
            .set_content_type('application/json') \
            .set_header('bearer xxxxx') \
            .set_method('GET') \
            .set_parameters({"Month": "2024-01-01"})\
            .make_request()

response = request.get_json_response()
display(response)
```
