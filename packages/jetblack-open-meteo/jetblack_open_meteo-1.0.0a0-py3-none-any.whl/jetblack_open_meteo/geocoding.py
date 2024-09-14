"""Geocoding"""

from typing import Literal, Mapping, Optional, Tuple

from .utils import (
    optional_int_to_param,
    remove_none_from_dict,
)

Format = Literal['json', 'protobuf']


def prepare_geocoding_request(
        name: str,
        count: Optional[int] = None,
        format: Optional[Format] = None,
        language: Optional[str] = None,
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = remove_none_from_dict({
        'name': name,
        'count': optional_int_to_param(count),
        'format': format,
        'language': language,
        'apikey': apikey
    })

    return url, params
