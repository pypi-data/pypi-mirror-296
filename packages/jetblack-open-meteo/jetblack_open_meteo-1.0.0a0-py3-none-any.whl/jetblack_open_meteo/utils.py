"""Forecast"""

from datetime import date, datetime
from decimal import Decimal
import math
from typing import Dict, Mapping, Optional, Sequence, TypeVar, Union

from .types import Number

T = TypeVar('T')


def remove_none_from_dict(dct: Mapping[str, Optional[str]]) -> Dict[str, str]:
    return {
        key: value
        for key, value in dct.items()
        if value is not None
    }


def ensure_sequence(value: Union[T, Sequence[T]]) -> Sequence[T]:
    if isinstance(value, list):
        return value
    return [value]  # type: ignore


def optional_number_to_param(value: Optional[Number]) -> Optional[str]:
    if value is None:
        return None
    if (
        (isinstance(value, Decimal) and value.is_nan()) or
        (isinstance(value, float) and math.isnan(value))
    ):
        return 'nan'
    return str(value)


def optional_string_array_to_param(value: Optional[Sequence[str]]) -> Optional[str]:
    if value is None:
        return None
    return ','.join(value)


def optional_int_to_param(
        value: Optional[int],
        min_value: Optional[int] = None,
        max_value: Optional[int] = None
) -> Optional[str]:
    if value is None:
        return None
    assert min_value is None or value >= min_value
    assert max_value is None or value <= max_value
    return str(value)


def optional_date_to_param(value: Optional[date]) -> Optional[str]:
    if value is None:
        return None
    return value.isoformat()


def optional_datetime_to_param(value: Optional[datetime]) -> Optional[str]:
    if value is None:
        return None
    return value.strftime('%Y-%m-%dT%H:%M')


def optional_bool_to_param(value: Optional[bool]) -> Optional[str]:
    if value is None:
        return None
    return 'true' if value else 'false'
