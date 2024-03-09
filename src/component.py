from dataclasses import dataclass

@dataclass
class PassButton:
    x: int
    y: int
    w: int = 50
    h: int = 20