from dataclasses import dataclass

@dataclass
class PointCoordinates:
    lat: float
    lon: float

@dataclass
class PointAddresse:
    city: str
    addresse: str