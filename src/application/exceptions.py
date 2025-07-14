class NotFoundException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class InvalidDataException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class OptimisticLockException(Exception):
    def __init__(self, message: str = "Optimistic lock failed"):
        self.message = message
        super().__init__(self.message)
