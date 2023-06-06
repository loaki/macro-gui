from pydantic import BaseModel
from typing import List


class StopCheck(BaseModel):
    pos_x: int
    pos_y: int
    color: str


class Sequence(BaseModel):
    key: str
    pos_x: int = 0
    pos_y: int = 0
    duration: int = 0
    delay: int = 0


class Macro(BaseModel):
    title: str
    sequence: List[Sequence]
    delay: float = 0
    stop_check: StopCheck = None
    loop: bool = False
    pause_bind: str
    stop_bind: str
