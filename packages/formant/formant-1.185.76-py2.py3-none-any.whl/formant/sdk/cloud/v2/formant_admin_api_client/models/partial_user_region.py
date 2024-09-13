from enum import Enum


class PartialUserRegion(str, Enum):
    AMER = "AMER"
    EMEA = "EMEA"
    JAPAC = "JAPAC"

    def __str__(self) -> str:
        return str(self.value)
