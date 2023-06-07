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
    delay: float = 0


class Macro(BaseModel):
    title: str
    sequence: List[Sequence]
    stop_check: StopCheck = None
    loop: bool = False
    loop_delay: float = 0
    pause_bind: str
    stop_bind: str
