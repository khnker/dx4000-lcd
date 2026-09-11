from dataclasses import dataclass

@dataclass(frozen=True)
class ScreenOutput:
    line1: str
    line2: str

RenderResult = ScreenOutput
