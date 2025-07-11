class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidDataException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)
