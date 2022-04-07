from dataclasses import dataclass


@dataclass
class User:
    index: int
    id: int
    locale: str
    address: str
    plate: str


@dataclass
class Coordinates:
    x: int
    y: int
