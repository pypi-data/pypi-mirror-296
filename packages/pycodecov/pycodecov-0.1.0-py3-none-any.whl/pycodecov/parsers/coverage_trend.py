from datetime import datetime
from typing import Any

from ..schemas import CoverageTrend

__all__ = ["parse_coverage_trend_data"]


def parse_coverage_trend_data(data: dict[str, Any]) -> CoverageTrend:
    """
    Parse coverage trend data.

    Args:
        data: coverage trend json data.

    Returns:
        A `CoverageTrend` schema.

    Examples:
    >>> data = {
    ...     "timestamp": "2024-03-25T16:38:25.747678Z",
    ...     "min": 12.3,
    ...     "max": 12.3,
    ...     "avg": 12.3,
    ... }
    >>> coverage_trend = parse_coverage_trend_data(data)
    >>> coverage_trend
    CoverageTrend(timestamp=datetime.datetime(...), min=12.3, max=12.3, avg=12.3)
    """  # noqa: E501
    timestamp = data.get("timestamp")
    min = data.get("min")
    max = data.get("max")
    avg = data.get("avg")

    return CoverageTrend(datetime.fromisoformat(timestamp), min, max, avg)
