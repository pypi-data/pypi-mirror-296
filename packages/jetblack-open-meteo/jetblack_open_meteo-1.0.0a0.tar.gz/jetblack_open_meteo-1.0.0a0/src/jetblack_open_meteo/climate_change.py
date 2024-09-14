"""Climate change"""


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

EnsembleModels = Literal[
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

Daily = Literal[
    'temperature_2m_max'
    'temperature_2m_min'
    'temperature_2m_mean',
    'cloud_cover_mean',
    'relative_humidity_2m_max'
    'relative_humidity_2m_min'
    'relative_humidity_2m_mean',
    'soil_moisture_0_to_10cm_mean',
    'precipitation_sum',
    'rain_sum',
    'snowfall_sum',
    'wind_speed_10m_mean'
    'wind_speed_10m_max',
    'pressure_msl_mean',
    'shortwave_radiation_sum'
]


def prepare_climate_change_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        models: Optional[Sequence[EnsembleModels]] = None,
        elevation: Optional[Number] = None,
        daily: Optional[Sequence[Daily]] = None,
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
    url = "https://climate-api.open-meteo.com/v1/climate"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'models': optional_string_array_to_param(models),
        'elevation': optional_number_to_param(elevation),
        'daily': optional_string_array_to_param(daily),
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
