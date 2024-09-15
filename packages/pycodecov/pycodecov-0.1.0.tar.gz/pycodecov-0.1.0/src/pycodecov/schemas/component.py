from dataclasses import dataclass

__all__ = ["Component"]


@dataclass(slots=True)
class Component:
    """
    A schema used to store info about component.

    Attributes:
        component_id: component id.
        name: component name.
    """

    component_id: str
    name: str
