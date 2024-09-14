"""Flood"""

from datetime import date
from typing import Literal, Mapping, Optional, Sequence, Tuple, Union

from .types import (
    CellSelection,
    Coordinate,
    TimeFormat,
)
from .utils import (
    ensure_sequence,
    optional_bool_to_param,
    optional_date_to_param,
    optional_int_to_param,
    optional_string_array_to_param,
    remove_none_from_dict,
)

Daily = Literal[
    'river_discharge',
    'river_discharge_mean',
    'river_discharge_median',
    'river_discharge_max',
    'river_discharge_min',
    'river_discharge_p25',
    'river_discharge_p75',
]


def prepare_flood_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        daily: Optional[Sequence[Daily]] = None,
        timeformat: Optional[TimeFormat] = None,
        past_days: Optional[int] = None,
        forecast_days: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cell_selection: Optional[CellSelection] = None,
        ensemble: Optional[bool] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://flood-api.open-meteo.com/v1/flood"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'daily': optional_string_array_to_param(daily),
        'timeformat': timeformat,
        'past_days': optional_int_to_param(past_days, 0, 210),
        'forecast_days': optional_int_to_param(forecast_days, 0, 16),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'ensemble': optional_bool_to_param(ensemble),
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
