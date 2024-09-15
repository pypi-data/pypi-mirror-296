from dataclasses import dataclass
from datetime import datetime

__all__ = ["CoverageTrend"]


@dataclass(slots=True)
class CoverageTrend:
    """
    A schema used to store info about coverage trend.

    Attributes:
        timestamp: coverage trend timestamp.
        min: minimum value coverage trend.
        max: maximum value coverage trend.
        avg: average value coverage trend.
    """

    timestamp: datetime
    min: float
    max: float
    avg: float
