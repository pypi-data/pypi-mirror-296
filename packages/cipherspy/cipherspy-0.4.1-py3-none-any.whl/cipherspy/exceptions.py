class NegativeNumberException(Exception):
    def __init__(self, number: int) -> None:
        super().__init__(f"Invalid number {number}, must be greater than 0")
