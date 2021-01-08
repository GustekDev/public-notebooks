from dataclasses import dataclass
from typing import Union


@dataclass()
class Bet:
    selection: Union[int, str]
    size: int
