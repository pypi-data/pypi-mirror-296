"""Elevation"""

from typing import Mapping, Optional, Sequence, Tuple, Union

from .types import Coordinate
from .utils import (
    ensure_sequence,
    remove_none_from_dict,
)


def prepare_elevation_request(
        coordinate: Union[Coordinate, Sequence[Coordinate]],
        apikey: Optional[str] = None
) -> Tuple[str, Mapping[str, str]]:
    url = "https://api.open-meteo.com/v1/elevation"

    coordinate = ensure_sequence(coordinate)

    params = remove_none_from_dict({
        'latitude': ','.join([str(latitude) for latitude, _ in coordinate]),
        'longitude': ','.join([str(longitude) for _, longitude in coordinate]),
        'apikey': apikey
    })

    return url, params
