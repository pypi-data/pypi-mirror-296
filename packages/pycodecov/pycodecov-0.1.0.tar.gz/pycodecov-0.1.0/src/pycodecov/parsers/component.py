from typing import Any

from ..schemas import Component

__all__ = ["parse_component_data"]


def parse_component_data(data: dict[str, Any]) -> Component:
    """
    Parse component data.

    Args:
        data: component json data.

    Returns:
        A `Component` schema.

    Examples:
    >>> data = {
    ...     "component_id": "string",
    ...     "name": "string",
    ... }
    >>> component = parse_component_data(data)
    >>> component
    Component(component_id='string', name='string')
    """
    component_id = data.get("component_id")
    name = data.get("name")

    return Component(component_id, name)
