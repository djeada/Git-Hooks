from dataclasses import dataclass


@dataclass(order=True)
class ErrorData:
    line_number: int
    error_message: str

    def __str__(self):
        return f"Line {self.line_number}: {self.error_message}"
