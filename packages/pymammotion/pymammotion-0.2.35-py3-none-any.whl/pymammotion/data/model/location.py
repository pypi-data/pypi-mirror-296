"""Contains RTK models for robot location and RTK positions."""

from dataclasses import dataclass


@dataclass
class Point:
    """Returns a lat long."""

    latitude: float = 0.0
    longitude: float = 0.0

    def __init__(self, latitude: float = 0.0, longitude: float = 0.0) -> None:
        self.latitude = latitude
        self.longitude = longitude


@dataclass
class Dock(Point):
    """Stores robot dock position."""

    rotation: int = 0


@dataclass
class Location:
    """Stores/retrieves RTK GPS data."""

    device: Point
    RTK: Point
    dock: Dock
    position_type: int = 0
    orientation: int = 0  # 360 degree rotation +-
    work_zone: int = 0

    def __init__(self) -> None:
        self.device = Point()
        self.RTK = Point()
        self.dock = Dock()
