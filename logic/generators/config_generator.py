from typing import Any

from logic.helpers.translator import Translator
from logic.logger import LogManager as lm
from settings import settings as sett


class ConfigGenerator:
    """
    Класс, модифицирующий конфиг. Создан для добавления ответа на окно ввода
    данных. НЕ затрагивает изменения фйла конфигурации. Только свойство класса.

    Methods
    -------
    - add_greetings_to_config(greeting, config)
        Добавляет приветствие в конфиг.

    - add_response_to_config(
        config, response, only_keys, pre_message, post_message
    )
        Добавляет ответ в конфиг.
        Если в конфиге уже есть ответ с таким же именем, то он
        перезаписывается.

    - remove_result_from_config(config)
        Удаляет ответ из конфига.
        Если в конфиге нет ответа с таким же именем, то ничего не происходит.

    - add_logo_to_config(config, place)
        Добавляет логотип в конфиг в конкретное место в списке виджетов.

    Private Methods
    ---------------
    - __add_new_layout_to_config(config, new_layout_config, place)
        Добавляет конфиг нового контейнера в текущий конфиг на конкретное
        место среди виджетов.

    - __generate_response_config(
        response, only_keys, pre_message, post_message
    )
        Генерирует конфиг для контейнера содержащего лейблы ответов.

    - disable_fields(config)
        Добавляет в конфиг атрибут "disabled: 1" для всех полей ввода и выбора.
        Таким образом блокирует все поля ввода и выбора.

    - __enable_fields(config)
        Удаляет из конфига атрибут "disabled: 1" для всех полей ввода и выбора.
        Таким образом разблокирует все поля ввода и выбора.

    - __change_button(config, new_name, new_method)
        Меняет в конфиге кнопку "Invia" на "Avanti" и наоборот. Также меняет
        метод, который вызывается при нажатии на кнопку.

    - __generate_logo_config()
        Просто возвращает конфиг контейнера с логотипом.
    """

    def add_greetings_to_config(
        self,
        greeting: str,
        config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Добавляет приветствие в конфиг.

        Parameters
        ----------
        - greeting : str
            Приветствие, которое нужно добавить в конфиг.

        - config : dict[str, Any]
            Конфиг, в который нужно добавить приветствие.

        Returns
        -------
        - config : dict[str, Any]
            Конфиг, в который добавлено приветствие.
        """

        lm.log_method_call()
        greeting_config = {
            sett.LAYOUT: {
                sett.TYPE: sett.LAYOUT_TYPE_HORIZONTAL,
                sett.NAME: sett.GREETING,
                sett.WIDGETS: [
                    {
                        sett.TYPE: sett.LABEL,
                        sett.TEXT: greeting,
                        sett.TEXT_SIZE: sett.SPECIAL_FONT_SIZE,
                        sett.ALIGN: sett.ALIGN_LEFT,
                        sett.ALIGNV: sett.ALIGN_CENTER
                    },
                    {
                        sett.TYPE: sett.BUTTON,
                        sett.TEXT: sett.MY_PROFILE,
                        sett.CALLBACK: sett.HANDLE_OPEN_MY_PROFILE_METHOD,
                        sett.ALIGN: sett.ALIGN_RIGHT,
                        sett.HEIGHT: sett.NON_STANDART_BUTTON_HEIGHT,
                        sett.WIDTH: sett.NON_STANDART_BUTTON_WIDTH
                    },
                    {
                        sett.TYPE: sett.BUTTON,
                        sett.TEXT: sett.LOGOUT,
                        sett.CALLBACK: sett.HANDLE_LOGOUT_METHOD,
                        sett.ALIGN: sett.ALIGN_RIGHT,
                        sett.HEIGHT: sett.NON_STANDART_BUTTON_HEIGHT,
                        sett.WIDTH: sett.NON_STANDART_BUTTON_WIDTH
                    }
                ]
            }
        }
        config[sett.LAYOUT][sett.WIDGETS].insert(
            sett.SET_TO_ZERO,
            greeting_config
        )

        return config

    def add_response_to_config(
        self,
        config: dict[str, Any],
        response: dict[str, Any],
        only_keys: list[str] | None,
        pre_message: str,
        post_mssage: str,
    ) -> dict[str, Any]:
        """
        Добавляет ответ в конфиг и блокирует все поля для ввода и выбора.
        Меняет кнопку "Invia" на "Avanti".

        Parameters
        ----------
        - config : dict[str, Any]
            Конфиг, в который нужно добавить ответ.

        - response : dict[str, Any]
            Ответ, который нужно добавить в конфиг.

        - only_keys : list[str] | None
            Список ключей словаря ответов, которые нужно добавить в конфиг.
            Если None, то добавляются все ключи.

        - pre_message : str
            Сообщение, которое нужно добавить перед ответом.

        - post_message : str | None
            Сообщение, которое нужно добавить после ответа.
            Если None, то сообщение не добавляется.

        Returns
        -------
        - config : dict[str, Any]
            Конфиг, в который добавлен ответ.
        """

        lm.log_info(sett.GENERATE_RESPONSE)
        config_to_add = self.__generate_response_config(
            response, only_keys, pre_message, post_mssage
        )
        config_where_to_add: list = config[sett.LAYOUT][sett.WIDGETS]
        config_where_to_add.insert(sett.MINUS_TWO, config_to_add)

        lm.log_info(sett.DISABLE_FIELDS)
        self.__disable_fields(config)

        lm.log_info(sett.CHANGE_BUTTON)
        self.__change_button(
            config, sett.FORWARD_IT, sett.HANDLE_FORWARD_BUTTON_METHOD
        )
        return config

    def remove_result_from_config(
        self,
        config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Удаляет ответ из конфига. Разблокирует все поля для ввода и выбора.
        Меняет кнопку "Avanti" на "Invia".

        Parameters
        ----------
        - config : dict[str, Any]
            Конфиг, из которого нужно удалить ответ.

        Returns
        -------
        - config : dict[str, Any]
            Конфиг, из которого удален ответ.
        """

        lm.log_info(sett.REMOVE_RESULT_FROM_CONFIG)
        widgets: list[dict[str, dict]] = config[sett.LAYOUT][sett.WIDGETS]
        if widgets:
            for i in range(len(widgets)):
                if (
                    widgets[i].get(sett.LAYOUT) and
                    widgets[i][sett.LAYOUT].get(sett.NAME) == sett.RESPONSE
                ):
                    widgets.pop(i)
                    break

        lm.log_info(sett.ENABLE_FIELDS)
        self.__enable_fields(config)

        lm.log_info(sett.CHANGE_BUTTON)
        self.__change_button(
            config, sett.START_IT, sett.HANDLE_START_BUTTON_METHOD
        )

        return config

    def add_logo_to_config(
        self,
        config: dict[str, Any],
        place: int = sett.DEFAULT_PLACE_TO_PASTE
    ) -> dict[str, Any]:
        """
        Добавляет логотип в конкретное место конфига.

        Parameters
        ----------
        - config : dict[str, Any]
            Конфиг, в который нужно добавить логотип.

        - place : int
            Default = -100\n
            Позиция, на которую нужно добавить логотип.
            По умолчанию -100, что означает добавление в конец списка.

        Returns
        -------
        - config : dict[str, Any]
            Конфиг, в который добавлен логотип.
        """

        lm.log_info(sett.GENERATE_LOGO_CONFIG)
        logo_config = self.__generate_logo_config()
        return self.__add_new_layout_to_config(
            config, logo_config, place
        )

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
    def __add_new_layout_to_config(
        self,
        config: dict[str, Any],
        new_layout_config: dict[str, Any],
        place: int = sett.DEFAULT_PLACE_TO_PASTE
    ):
        """
        Добавляет конфиг нового контейнера в текущий конфиг на конкретное
        место среди виджетов.

        Parameters
        ----------
        - config : dict[str, Any]
            Конфиг, в который нужно добавить новый контейнер.

        - new_layout_config : dict[str, Any]
            Конфиг нового контейнера.

        - place : int
            Default = -100\n
            Позиция, на которую нужно добавить новый контейнер.
            Если -1, то добавляет в конец списка.
        """

        lm.log_info(sett.INSERT_NEW_LAYOUT_TO_CONFIG)
        if place == sett.DEFAULT_PLACE_TO_PASTE:
            config[sett.LAYOUT][sett.WIDGETS].append(new_layout_config)
        else:
            config[sett.LAYOUT][sett.WIDGETS].insert(place, new_layout_config)
        return config

    def __generate_response_config(
            self,
            response: dict[str, Any],
            only_keys: list[str] | None,
            pre_message: str,
            post_message: str | None,
    ):
        """
        Генерирует конфиг для контейнера содержащего лейблы ответов.

        Parameters
        ----------
        - response : dict[str, Any]
            Ответ, который нужно добавить в конфиг.

        - only_keys : list[str] | None
            Список ключей словаря ответов, которые нужно добавить в конфиг.
            Если None, то добавляются все ключи.

        - pre_message : str
            Сообщение, которое нужно добавить перед ответом.

        - post_message : str | None
            Сообщение, которое нужно добавить после ответа.
            Если None, то сообщение не добавляется.

        Returns
        -------
        - config : dict[str, Any]
            Обновленный конфиг.
        """

        lm.log_method_call()
        config = {
            sett.LAYOUT: {
                sett.TYPE: sett.LAYOUT_TYPE_VERTICAL,
                sett.NAME: sett.RESPONSE,
                sett.WIDGETS: []
            }
        }

        widgets: list = config[sett.LAYOUT][sett.WIDGETS]

        if pre_message:
            widgets.append(
                {
                    sett.TYPE: sett.LABEL,
                    sett.TEXT: pre_message,
                    sett.TEXT_SIZE: sett.SPECIAL_FONT_SIZE,
                    sett.BOLD: sett.SET_TO_ONE,
                    sett.ALIGN: sett.ALIGN_CENTER
                }
            )

        if only_keys:
            filtered_values = {
                k: v for k, v in response.items() if k in only_keys
            }
            filtered_values = Translator.translate_dict(filtered_values)

        response_layout = {
            sett.LAYOUT: {
                sett.TYPE: sett.LAYOUT_TYPE_GRID,
                sett.COLUMNS: sett.SET_TO_TWO,
                sett.NAME: sett.RESPONSE_LABELS,
                sett.WIDGETS: []
            }
        }
        response_widgets: list = response_layout[sett.LAYOUT][sett.WIDGETS]

        for title, value in filtered_values.items():
            if (
                (title == sett.PRICE_IT and value) or
                (title == sett.PREPARATION_IT and value)
            ):
                value = sett.CONCAT_TWO_MSGS.format(
                    str(value),
                    sett.EURO_SYMBOL
                )
            elif title == sett.WEIGHT_IT and value:
                value = sett.CONCAT_TWO_MSGS.format(
                    str(value),
                    sett.KILO_SYMBOL
                )
            elif title == sett.DEVELOPMENT_IT and value:
                value = sett.CONCAT_TWO_MSGS.format(
                    str(value),
                    sett.METERS_SYMBOL
                )
            elif (
                title == sett.PRICE_IT or title == sett.WEIGHT_IT
            ) and not value:
                value = sett.NOT_FOUND_IT

            title = sett.ADD_COLON.format(title)

            response_widgets.append(
                {
                    sett.TYPE: sett.LABEL,
                    sett.TEXT: title,
                    sett.ALIGN: sett.ALIGN_RIGHT,
                    sett.TEXT_SIZE: sett.SPECIAL_FONT_SIZE,
                    sett.COLUMN: sett.WIDGET_POS_FIRST,
                }
            )
            response_widgets.append(
                {
                    sett.TYPE: sett.LABEL,
                    sett.TEXT: str(value),
                    sett.ALIGN: sett.ALIGN_LEFT,
                    sett.TEXT_SIZE: sett.SPECIAL_FONT_SIZE,
                    sett.COLUMN: sett.WIDGET_POS_CURRENT
                }
            )
        widgets.append(response_layout)

        if post_message:
            widgets.append(
                {
                    sett.TYPE: sett.LABEL,
                    sett.TEXT: post_message,
                    sett.TEXT_SIZE: sett.SPECIAL_FONT_SIZE,
                    sett.ALIGN: sett.ALIGN_CENTER
                }
            )
        return config

    def __disable_fields(self, config: dict) -> None:
        """
        Добавляет в конфиг атрибут "disabled: 1" для всех полей ввода и выбора.

        Parameters
        ----------
        - config : dict
            Конфиг, в котором нужно добавить атрибут "disabled: 1".

        Returns
        -------
        - config : dict
            Обновленный конфиг.
        """

        if config.get(sett.LAYOUT):
            self.__disable_fields(config[sett.LAYOUT])

        if config.get(sett.WIDGETS):
            for widget in config[sett.WIDGETS]:
                if widget.get(sett.LAYOUT):
                    self.__disable_fields(widget[sett.LAYOUT])
                elif (
                    widget.get(sett.TYPE) == sett.DROPDOWN or
                    widget.get(sett.TYPE) == sett.INPUT
                ):
                    widget[sett.DISABLED] = sett.SET_TO_ONE

    def __enable_fields(self, config: dict) -> None:
        """
        Удаляет из конфига атрибут "disabled: 1" для всех полей ввода и выбора.

        Parameters
        ----------
        - config : dict
            Конфиг, в котором нужно удалить атрибут "disabled: 1".

        Returns
        -------
        - config : dict
            Обновленный конфиг.
        """

        if config.get(sett.LAYOUT):
            self.__enable_fields(config[sett.LAYOUT])

        if config.get(sett.WIDGETS):
            for widget in config[sett.WIDGETS]:
                if widget.get(sett.LAYOUT):
                    self.__enable_fields(widget[sett.LAYOUT])
                elif (
                    widget.get(sett.TYPE) == sett.DROPDOWN or
                    widget.get(sett.TYPE) == sett.INPUT
                ):
                    widget.pop(sett.DISABLED, None)

    def __change_button(
        self,
        config: dict,
        new_name: str,
        new_method: str
    ) -> None:
        """
        Меняет в конфиге кнопку "Invia" на "Avanti" и наоборот. Также меняет
        метод, который вызывается при нажатии на кнопку.

        Parameters
        ----------
        - config : dict
            Конфиг, в котором нужно поменять кнопку.

        - new_name : str
            Новое имя кнопки.

        - new_method : str
            Новый метод, который вызывается при нажатии на кнопку.
        """

        widgets: list[dict[str, dict]] = config[sett.LAYOUT][sett.WIDGETS]

        for widget in widgets:
            if (
                widget.get(sett.LAYOUT) and
                widget[sett.LAYOUT].get(sett.NAME) == sett.BOTTOM_LAYOUT
            ):
                bottom_widgets: list[dict] = widget[sett.LAYOUT][sett.WIDGETS]
                for bottom_widget in bottom_widgets:
                    if (
                        bottom_widget.get(sett.TYPE) == sett.BUTTON
                    ):
                        bottom_widget[sett.TEXT] = new_name
                        bottom_widget[sett.CALLBACK] = new_method
                        break

    def __generate_logo_config(self) -> dict:
        """
        Просто возвращает конфиг контейнера с логотипом.

        Returns
        -------
        - config : dict
            Конфиг контейнера с логотипом.
        """

        return {
            sett.LAYOUT: {
                sett.TYPE: sett.LAYOUT_TYPE_VERTICAL,
                sett.NAME: sett.LOGO,
                sett.ALIGN: sett.ALIGN_CENTER,
                sett.SETSPACING: sett.SET_TO_ZERO,
                sett.WIDGETS: [
                    {
                        sett.TYPE: sett.IMAGE,
                        sett.PATH: sett.LOGO_PATH,
                        sett.ALIGN: sett.ALIGN_CENTER
                    }
                ]
            }
        }
