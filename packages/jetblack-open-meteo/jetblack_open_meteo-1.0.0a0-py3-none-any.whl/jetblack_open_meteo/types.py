"""Types"""

from decimal import Decimal
from typing import Literal, Tuple, Union

Number = Union[int, float, Decimal]
Coordinate = Tuple[Number, Number]

TemperatureUnit = Literal['celsius', 'fahrenheit']
WindSpeedUnit = Literal['kmh', 'ms', 'mph', 'kn']
PrecipitationUnit = Literal['mm', 'inch']
TimeFormat = Literal['iso8601', 'unixtime', 'utc_offset_seconds']
CellSelection = Literal['land', 'sea', 'nearest']
LengthUnit = Literal['metric', 'imperial']
