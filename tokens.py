from dataclasses import dataclass
@dataclass
class Token:
    type: str
    value: object
    line: int
    column: int
    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, {self.line}:{self.column})"
