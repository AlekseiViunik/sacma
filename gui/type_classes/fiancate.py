from abstract_base_type import AbstractBaseType


class Fiancate(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self):
        self.open_response_window(100.15, 10.5)
