"""Ensemble models"""

from datetime import date, datetime
from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from .types import (
    CellSelection,
    Coordinate,
    Number,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit
)
from .utils import (
    ensure_sequence,
    optional_date_to_param,
    optional_datetime_to_param,
    optional_int_to_param,
    optional_number_to_param,
    optional_string_array_to_param,
    remove_none_from_dict,
)

Models = Literal[
    'icon_seamless',
    'icon_global',
    'icon_eu',
    'icon_d2',
    'gfs_seamless',
    'gfs025',
    'gfs05',
    'ecmwf_ifs04',
    'gem_global',
    'bom_access_global_ensemble'
]

Hourly = Literal[
    'temperature_2m',
    'relative_humidity_2m',
    'dew_point_2m',
    'apparent_temperature',
    'pressure_msl',
    'surface_pressure',
    'cloud_cover',
    'wind_speed_10m',
    'wind_speed_80m',
    'wind_speed_120m',
    'wind_direction_10m',
    'wind_direction_80m',
    'wind_direction_120m',
    'wind_gusts_10m',
    'shortwave_radiation',
    'direct_radiation',
    'direct_normal_irradiance',
    'diffuse_radiation',
    'sunshine_duration',
    'vapour_pressure_deficit',
    'evapotranspiration',
    'et0_fao_evapotranspiration',
    'weather_code',
    'precipitation',
    'snowfall',
    'rain',
    'weather_code',
    'snow_depth',
    'freezing_level_height',
    'visibility',
    'cape',
    'surface_temperature',
    'soil_temperature_0_to_10cm',
    'soil_temperature_10_to_40cm',
    'soil_temperature_40_to_100cm',
    'soil_temperature_100_to_200cm',
    'soil_moisture_0_to_10cm',
    'soil_moisture_10_to_40cm',
    'soil_moisture_40_to_100cm',
    'soil_moisture_100_to_200cm',
]


def prepare_ensemble_models_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        models: Optional[Sequence[Models]] = None,
        elevation: Optional[Number] = None,
        hourly: Optional[Sequence[Hourly]] = None,
        temperature_unit: Optional[TemperatureUnit] = None,
        wind_speed_unit: Optional[WindSpeedUnit] = None,
        precipitation_unit: Optional[PrecipitationUnit] = None,
        timeformat: Optional[TimeFormat] = None,
        timezone: Optional[str] = None,
        past_days: Optional[int] = None,
        forecast_days: Optional[int] = None,
        forecast_hours: Optional[int] = None,
        forecast_minutely_15: Optional[int] = None,
        past_hours: Optional[int] = None,
        past_minutely_15: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        start_hour: Optional[datetime] = None,
        end_hour: Optional[datetime] = None,
        start_minutely_15: Optional[datetime] = None,
        end_minutely_15: Optional[datetime] = None,
        cell_selection: Optional[CellSelection] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://ensemble-api.open-meteo.com/v1/ensemble"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'models': optional_string_array_to_param(models),
        'elevation': optional_number_to_param(elevation),
        'hourly': optional_string_array_to_param(hourly),
        'temperature_unit': temperature_unit,
        'wind_speed_unit': wind_speed_unit,
        'precipitation_unit': precipitation_unit,
        'timeformat': timeformat,
        'timezone': timezone,
        'past_days': optional_int_to_param(past_days, 0, 92),
        'forecast_days': optional_int_to_param(forecast_days, 0, 16),
        'forecast_hours': optional_int_to_param(forecast_hours, 0),
        'forecast_minutely_15': optional_int_to_param(forecast_minutely_15, 0),
        'past_hours': optional_int_to_param(past_hours, 0),
        'past_minutely_15': optional_int_to_param(past_minutely_15, 0),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'start_hour': optional_datetime_to_param(start_hour),
        'end_hour': optional_datetime_to_param(end_hour),
        'start_minutely_15': optional_datetime_to_param(start_minutely_15),
        'end_minutely_15': optional_datetime_to_param(end_minutely_15),
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
