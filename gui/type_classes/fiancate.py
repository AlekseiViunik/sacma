from gui.helper import Helper
from gui.widget_creator import WidgetCreator
from settings import settings as set
from abstract_base_type import AbstractBaseType


class Fiancate(AbstractBaseType):
    def __init__(self, root, type):
        super().__init__(root, type)

    def create_components(self):
        select_options, input_options, always_on = (
            (
                self.get_default_options("non-sismoresistente", option) for
                option in ["select", "input", "always_on"]
            )
        )

        creator = WidgetCreator(
            self.window,
            select_options,
            input_options,
            always_on,
        )
        creator.create_ui()
        self.entries = creator.entries

        creator.create_invia_button(self.calculate)

        self.window.protocol(
            set.ON_CLOSING_WINDOW,
            lambda: Helper(self.root).on_close(self.window)
        )

    def calculate(self):
        self.open_response_window(100.15, 10.5)
