# jetblack-open-meteo

A client API for [open-meteo](https://open-meteo.com).

## Status

This is work in progress.

## Usage

Rather than provide a client, this library provides the url and params.

This means you can use the http library of you choice.

For example with requests:

```python
import pandas as pd
import requests

from jetblack_open_meteo import prepare_weather_forecast_request


url, params = prepare_weather_forecast_request(
    (51.50242846391432, -0.1423227420691731),
    hourly=['temperature_2m'],
)

# Use requests to get the data.
response = requests.get(url, params=params)
data = response.json()

df = pd.DataFrame(data['hourly'])
print(df)
```
