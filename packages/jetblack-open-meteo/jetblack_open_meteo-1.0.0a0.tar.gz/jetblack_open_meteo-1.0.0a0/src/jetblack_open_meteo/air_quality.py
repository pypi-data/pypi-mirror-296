"""Air quality"""

from datetime import date, datetime
from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from .types import (
    CellSelection,
    Coordinate,
    TimeFormat,
)
from .utils import (
    ensure_sequence,
    optional_date_to_param,
    optional_datetime_to_param,
    optional_int_to_param,
    optional_string_array_to_param,
    remove_none_from_dict,
)

Hourly = Literal[
    'pm10',
    'pm2_5',
    'carbon_monoxide',
    'nitrogen_dioxide',
    'sulphur_dioxide',
    'ozone',
    'ammonia',
    'aerosol_optical_depth',
    'dust',
    'uv_index',
    'uv_index_clear_sky',
    'alder_pollen',
    'birch_pollen',
    'grass_pollen',
    'mugwort_pollen',
    'olive_pollen',
    'ragweed_pollen',
    'european_aqi',
    'european_aqi_pm2_5',
    'european_aqi_pm10',
    'european_aqi_nitrogen_dioxide',
    'european_aqi_ozone',
    'european_aqi_sulphur_dioxide',
    'us_aqi',
    'us_aqi_pm2_5',
    'us_aqi_pm10',
    'us_aqi_nitrogen_dioxide',
    'us_aqi_ozone',
    'us_aqi_sulphur_dioxide',
    'us_aqi_carbon_monoxide',
]

Current = Literal[
    'european_aqi',
    'us_aqi',
    'pm10',
    'pm2_5',
    'carbon_monoxide',
    'nitrogen_dioxide',
    'sulphur_dioxide',
    'ozone',
    'aerosol_optical_depth',
    'dust',
    'uv_index',
    'uv_index_clear_sky',
    'ammonia',
    'alder_pollen',
    'birch_pollen',
    'grass_pollen',
    'mugwort_pollen',
    'olive_pollen',
    'ragweed_pollen'
]

Domain = Literal[
    'auto',
    'cams_europe',
    'cams_global'
]


def prepare_air_quality_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        hourly: Optional[Sequence[Hourly]] = None,
        current: Optional[Sequence[Current]] = None,
        domains: Optional[Domain] = None,
        timeformat: Optional[TimeFormat] = None,
        timezone: Optional[str] = None,
        past_days: Optional[int] = None,
        forecast_days: Optional[int] = None,
        forecast_hours: Optional[int] = None,
        past_hours: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        start_hour: Optional[datetime] = None,
        end_hour: Optional[datetime] = None,
        cell_selection: Optional[CellSelection] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'hourly': optional_string_array_to_param(hourly),
        'current': optional_string_array_to_param(current),
        'domains': domains,
        'timeformat': timeformat,
        'timezone': timezone,
        'past_days': optional_int_to_param(past_days, 0, 92),
        'forecast_days': optional_int_to_param(forecast_days, 0, 7),
        'forecast_hours': optional_int_to_param(forecast_hours, 0),
        'past_hours': optional_int_to_param(past_hours, 0),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'start_hour': optional_datetime_to_param(start_hour),
        'end_hour': optional_datetime_to_param(end_hour),
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
