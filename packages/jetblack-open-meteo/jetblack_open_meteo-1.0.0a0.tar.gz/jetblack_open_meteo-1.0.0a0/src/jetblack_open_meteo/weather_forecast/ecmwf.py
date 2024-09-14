"""ECMWF"""

from datetime import date
from typing import (
    List,
    Literal,
    Mapping,
    Optional,
    Sequence,
    Tuple,
    Union,
    cast
)

from ..types import (
    CellSelection,
    Coordinate,
    Number,
    PrecipitationUnit,
    TemperatureUnit,
    TimeFormat,
    WindSpeedUnit
)
from ..utils import (
    ensure_sequence,
    optional_date_to_param,
    optional_int_to_param,
    optional_number_to_param,
    optional_string_array_to_param,
    remove_none_from_dict,
)

Hourly = Literal[
    'temperature_2m',
    'relative_humidity_2m',
    'dew_point_2m',
    'apparent_temperature',
    'precipitation',
    'rain',
    'snowfall',
    'weather_code',
    'pressure_msl',
    'surface_pressure',
    'cloud_cover',
    'cloud_cover_low',
    'cloud_cover_mid',
    'cloud_cover_high',
    'vapour_pressure_deficit',
    'wind_speed_10m',
    'wind_direction_10m',
    'wind_gusts_10m',
    'surface_temperature',
    'soil_temperature_0_to_7cm',
    'runoff',
    'total_column_integrated_water_vapour',
]

PressureType = Literal[
    'temperature_2m',
    'relative_humidity_2m',
    'cloud_cover',
    'wind_speed_10m',
    'wind_direction_10m',
    'geopotential_height_1000hPa'
]

PressureLevel = Literal[
    '1000hPa',
    '925hPa',
    '850hPa',
    '700hPa',
    '500hPa',
    '300hPa',
    '250hPa',
    '200hPa',
    '50hPa'
]

Pressure = Tuple[PressureType, PressureLevel]


def prepare_ecmwf_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        elevation: Optional[Number] = None,
        hourly: Optional[Sequence[Hourly]] = None,
        pressure: Optional[Sequence[Pressure]] = None,
        temperature_unit: Optional[TemperatureUnit] = None,
        wind_speed_unit: Optional[WindSpeedUnit] = None,
        precipitation_unit: Optional[PrecipitationUnit] = None,
        timeformat: Optional[TimeFormat] = None,
        past_days: Optional[int] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        cell_selection: Optional[CellSelection] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://api.open-meteo.com/v1/ecmwf"

    coordinate = ensure_sequence(coordinate)

    variables = cast(List[str], list(hourly) if hourly else [])

    if pressure:
        variables += [
            f'{pressure_type}_{pressure_level}'
            for pressure_type, pressure_level in pressure
        ]

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'elevation': optional_number_to_param(elevation),
        'hourly': optional_string_array_to_param(variables if variables else None),
        'temperature_unit': temperature_unit,
        'wind_speed_unit': wind_speed_unit,
        'precipitation_unit': precipitation_unit,
        'timeformat': timeformat,
        'past_days': optional_int_to_param(past_days, 0, 92),
        'start_date': optional_date_to_param(start_date),
        'end_date': optional_date_to_param(end_date),
        'cell_selection': cell_selection,
        'apikey': apikey
    })

    return url, params
