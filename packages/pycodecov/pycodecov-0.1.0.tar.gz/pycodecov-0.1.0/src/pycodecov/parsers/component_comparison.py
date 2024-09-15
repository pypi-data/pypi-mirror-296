from typing import Any

from ..schemas import ComponentComparison
from .report_total import parse_report_total_data

__all__ = ["parse_component_comparison_data"]


def parse_component_comparison_data(data: dict[str, Any]) -> ComponentComparison:
    """
    Parse component comparison data.

    Args:
        data: component comparison json data.

    Returns:
        A `ComponentComparison` schema.

    Examples:
    >>> data = {
    ...     "component_id": "string",
    ...     "name": "string",
    ...     "base_report_totals": {
    ...         "files": 123,
    ...         "lines": 123,
    ...         "hits": 123,
    ...         "misses": 123,
    ...         "partials": 123,
    ...         "coverage": 12.3,
    ...         "branches": 123,
    ...         "methods": 123,
    ...         "messages": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...         "diff": 123,
    ...     },
    ...     "head_report_totals": {
    ...         "files": 123,
    ...         "lines": 123,
    ...         "hits": 123,
    ...         "misses": 123,
    ...         "partials": 123,
    ...         "coverage": 12.3,
    ...         "branches": 123,
    ...         "methods": 123,
    ...         "messages": 123,
    ...         "sessions": 123,
    ...         "complexity": 12.3,
    ...         "complexity_total": 12.3,
    ...         "complexity_ratio": 12.3,
    ...         "diff": 123,
    ...     },
    ...     "diff_totals": None,
    ... }
    >>> component_comparison = parse_component_comparison_data(data)
    >>> component_comparison
    ComponentComparison(component_id='string', name='string', base_report_totals=ReportTotal(...), head_report_totals=ReportTotal(...), diff_totals=None)
    """  # noqa: E501
    component_id = data.get("component_id")
    name = data.get("name")
    base_report_totals = data.get("base_report_totals")
    head_report_totals = data.get("head_report_totals")
    diff_totals = data.get("diff_totals")

    return ComponentComparison(
        component_id,
        name,
        parse_report_total_data(base_report_totals),
        parse_report_total_data(head_report_totals),
        parse_report_total_data(diff_totals)
        if diff_totals is not None
        else diff_totals,
    )
