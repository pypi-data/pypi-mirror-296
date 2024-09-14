"""DWD Germany"""

from datetime import date, datetime
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
    optional_datetime_to_param,
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
    'showers',
    'snowfall',
    'snow_depth',
    'weather_code',
    'pressure_msl',
    'surface_pressure',
    'cloud_cover',
    'cloud_cover_low',
    'cloud_cover_mid',
    'cloud_cover_high',
    'evapotranspiration',
    'et0_fao_evapotranspiration',
    'vapour_pressure_deficit',
    'wind_speed_10m',
    'wind_speed_80m',
    'wind_speed_120m',
    'wind_speed_180m',
    'wind_direction_10m',
    'wind_direction_80m',
    'wind_direction_120m',
    'wind_direction_180m',
    'wind_gusts_10m',
    'temperature_80m',
    'temperature_120m',
    'temperature_180m',
    'soil_temperature_0cm',
    'soil_temperature_6cm',
    'soil_temperature_18cm',
    'soil_temperature_54cm',
    'soil_moisture_0_to_1cm',
    'soil_moisture_1_to_3cm',
    'soil_moisture_3_to_9cm',
    'soil_moisture_9_to_27cm',
    'soil_moisture_27_to_81cm',
    # Additional Variables.
    'is_day',
    'lightning_potential',
    'updraft',
    'cape',
    'freezing_level_height',
    'snowfall_height',
    'sunshine_duration',
    # Solar radiation variables
    'shortwave_radiation',
    'direct_radiation',
    'diffuse_radiation',
    'direct_normal_irradiance',
    'terrestrial_radiation',
    'shortwave_radiation_instant',
    'direct_radiation_instant',
    'diffuse_radiation_instant',
    'direct_normal_irradiance_instant',
    'terrestrial_radiation_instant'
]

Minutely15 = Literal[
    'shortwave_radiation',
    'direct_radiation',
    'direct_normal_irradiance',
    'diffuse_radiation',
    'global_tilted_irradiance',
    'sunshine_duration',
    'lightning_potential',
    'precipitation',
    'snowfall',
    'rain',
    'showers',
    'snowfall_height',
    'freezing_level_height',
    'cape',
]

Daily = Literal[
    'temperature_2m_max',
    'temperature_2m_min',
    'apparent_temperature_max',
    'apparent_temperature_min',
    'precipitation_sum',
    'rain_sum',
    'showers_sum',
    'snowfall_sum',
    'precipitation_hours',
    'weather_code',
    'sunrise',
    'sunset',
    'sunshine_duration',
    'daylight_duration',
    'wind_speed_10m_max',
    'wind_gusts_10m_max',
    'wind_direction_10m_dominant',
    'shortwave_radiation_sum',
    'et0_fao_evapotranspiration',
]

Current = Literal[
    'temperature_2m',
    'relative_humidity_2m',
    'apparent_temperature',
    'is_day',
    'precipitation',
    'rain',
    'showers',
    'snowfall',
    'weather_code',
    'cloud_cover',
    'pressure_msl',
    'surface_pressure',
    'wind_speed_10m',
    'wind_direction_10m',
    'wind_gusts_10m'
]

PressureLevel = Literal[
    '1000hPa',
    '975hPa',
    '950hPa',
    '925hPa',
    '900hPa',
    '850hPa',
    '800hPa',
    '700hPa',
    '600hPa',
    '500hPa',
    '400hPa',
    '300hPa',
    '250hPa',
    '200hPa',
    '150hPa',
    '100hPa',
    '70hPa',
    '50hPa',
    '30hPa'
]

PressureVariable = Literal[
    'temperature',
    'relative_humidity',
    'cloud_cover',
    'windspeed',
    'winddirection',
    'geopotential_height'
]

Pressure = Tuple[PressureVariable, PressureLevel]


def prepare_dwd_icon_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        elevation: Optional[Number] = None,
        hourly: Optional[Sequence[Hourly]] = None,
        pressure: Optional[Sequence[Pressure]] = None,
        minutely_15: Optional[Sequence[Minutely15]] = None,
        daily: Optional[Sequence[Daily]] = None,
        current: Optional[Sequence[Current]] = None,
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
    url = "https://api.open-meteo.com/v1/dwd-icon"

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
        'minutely_15': optional_string_array_to_param(minutely_15),
        'daily': optional_string_array_to_param(daily),
        'current': optional_string_array_to_param(current),
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
