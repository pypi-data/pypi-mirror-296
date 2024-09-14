"""Marine Forecast"""

from datetime import date, datetime
from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from .types import (
    CellSelection,
    Coordinate,
    LengthUnit,
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
    'wave_height',
    'wind_wave_height',
    'swell_wave_height',
    'wave_direction',
    'wind_wave_direction',
    'swell_wave_direction',
    'wave_period',
    'wind_wave_period',
    'swell_wave_period',
    'wind_wave_peak_period',
    'swell_wave_peak_period',
]

Daily = Literal[
    'wave_height_max',
    'wind_wave_height_max',
    'swell_wave_height_max',
    'wave_direction_dominant',
    'wind_wave_direction_dominant',
    'swell_wave_direction_dominant',
    'wave_period_max',
    'wind_wave_period_max',
    'swell_wave_period_max',
    'wind_wave_peak_period_max',
    'swell_wave_peak_period_max',
]

CurrentCondition = Literal[
    'wave_height',
    'wave_direction',
    'wave_period',
    'wind_wave_height',
    'wind_wave_direction',
    'wind_wave_period',
    'wind_wave_peak_period',
    'swell_wave_height',
    'swell_wave_direction',
    'swell_wave_period',
    'swell_wave_peak_period'
]


def prepare_marine_forecast_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        hourly: Optional[Sequence[Hourly]] = None,
        daily: Optional[Sequence[Daily]] = None,
        current: Optional[Sequence[CurrentCondition]] = None,
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
        length_unit: Optional[LengthUnit] = None,
        cell_selection: Optional[CellSelection] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://marine-api.open-meteo.com/v1/marine"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'hourly': optional_string_array_to_param(hourly),
        'daily': optional_string_array_to_param(daily),
        'current': optional_string_array_to_param(current),
        'timeformat': timeformat,
        'timezone': timezone,
        'past_days': optional_int_to_param(past_days, 0, 92),
        'forecast_days': optional_int_to_param(forecast_days, 0, 8),
        'forecast_hours': optional_int_to_param(forecast_hours, 0),
        'past_hours': optional_int_to_param(past_hours, 0),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'start_hour': optional_datetime_to_param(start_hour),
        'length_unit': length_unit,
        'end_hour': optional_datetime_to_param(end_hour),
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
