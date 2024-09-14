"""Historical weather"""

from datetime import date
from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from .types import (
    CellSelection,
    Coordinate,
    Number,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit,
)
from .utils import (
    ensure_sequence,
    optional_date_to_param,
    optional_number_to_param,
    optional_string_array_to_param,
    remove_none_from_dict,
)

Hourly = Literal[
    'temperature_2m',
    'relative_humidity_2m',
    'dew_point_2m',
    'apparent_temperature',
    'pressure_msl',
    'surface_pressure',
    'precipitation',
    'rain',
    'snowfall',
    'cloud_cover',
    'cloud_cover_low',
    'cloud_cover_mid',
    'cloud_cover_high',
    'shortwave_radiation',
    'direct_radiation',
    'direct_normal_irradiance',
    'diffuse_radiation',
    'sunshine_duration',
    'wind_speed_10m',
    'wind_speed_100m',
    'wind_direction_10m',
    'wind_direction_100m',
    'wind_gusts_10m',
    'et0_fao_evapotranspiration',
    'weather_code',
    'snow_depth',
    'vapour_pressure_deficit',
    'soil_temperature_0_to_7cm',
    'soil_temperature_7_to_28cm',
    'soil_temperature_28_to_100cm',
    'soil_temperature_100_to_255cm',
    'soil_moisture_0_to_7cm',
    'soil_moisture_7_to_28cm',
    'soil_moisture_28_to_100cm',
    'soil_moisture_100_to_255cm',
]

Daily = Literal[
    'weather_code',
    'temperature_2m_max',
    'temperature_2m_min',
    'apparent_temperature_max',
    'apparent_temperature_min',
    'precipitation_sum',
    'rain_sum',
    'snowfall_sum',
    'precipitation_hours',
    'sunrise', 'sunset',
    'sunshine_duration',
    'daylight_duration',
    'wind_speed_10m_max',
    'wind_gusts_10m_max',
    'wind_direction_10m_dominant',
    'shortwave_radiation_sum',
    'et0_fao_evapotranspiration',
]


def prepare_historical_weather_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        elevation: Optional[Number] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        hourly: Optional[Hourly] = None,
        daily: Optional[Sequence[Daily]] = None,
        temperature_unit: Optional[TemperatureUnit] = None,
        wind_speed_unit: Optional[WindSpeedUnit] = None,
        precipitation_unit: Optional[PrecipitationUnit] = None,
        timeformat: Optional[TimeFormat] = None,
        timezone: Optional[str] = None,
        cell_selection: Optional[CellSelection] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://archive-api.open-meteo.com/v1/archive"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'elevation': optional_number_to_param(elevation),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'hourly': optional_string_array_to_param(hourly),
        'daily': optional_string_array_to_param(daily),
        'temperature_unit': temperature_unit,
        'wind_speed_unit': wind_speed_unit,
        'precipitation_unit': precipitation_unit,
        'timeformat': timeformat,
        'timezone': timezone,
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
