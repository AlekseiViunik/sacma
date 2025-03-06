from abstract_base_type import AbstractBaseType


class Fiancate(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def calculate(self):
        self.open_response_window({"price": 100.15, "weight": 10.5})
