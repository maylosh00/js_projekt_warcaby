class incorrectDataException(Exception):
    def __init__(self, info):
        super().__init__(info)

class incorrectCoordinatesException(incorrectDataException):
    def __init__(self, info):
        super().__init__(info)

class incorrectColorValueException(incorrectDataException):
    def __init__(self, info):
        super().__init__(info)

class incorrectBoardSize(incorrectDataException):
    def __init__(self, info):
        super().__init__(info)