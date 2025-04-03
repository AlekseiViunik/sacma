from typing import Any

from logic.translator import Translator
from settings import settings as sett


class ConfigGenerator:
    """
    Класс, модифицирующий конфиг. Создан для добавления ответа на окно ввода
    данных. НЕ затрагивает изменения фйла конфигурации. Только свойство класса.

    Methods
    -------
    - add_response_to_config(
        config, response, only_keys, pre_message, post_message
    )
        Добавляет ответ в конфиг.
        Если в конфиге уже есть ответ с таким же именем, то он
        перезаписывается.

    - remove_result_from_config(config)
        Удаляет ответ из конфига.
        Если в конфиге нет ответа с таким же именем, то ничего не происходит.

    Private Methods
    ---------------
    - __generate_response_config(
        response, only_keys, pre_message, post_message
    )
        Генерирует конфиг для контейнера содержащего лейблы ответов.
    """

    def add_response_to_config(
        self,
        config: dict[str, Any],
        response: dict[str, Any],
        only_keys: list[str] | None,
        pre_message: str,
        post_mssage: str,
    ) -> None:
        """
        Добавляет ответ в конфиг.
        Если в конфиге уже есть ответ с таким же именем, то он
        перезаписывается.

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

        config_to_add = self.__generate_response_config(
            response, only_keys, pre_message, post_mssage
        )
        config_where_to_add: list = config[sett.LAYOUT][sett.WIDGETS]
        config_where_to_add.insert(sett.MINUS_ONE, config_to_add)
        return config

    def remove_result_from_config(
        self,
        config: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Удаляет ответ из конфига.
        Если в конфиге нет ответа с таким же именем, то ничего не происходит.

        Parameters
        ----------
        - config : dict[str, Any]
            Конфиг, из которого нужно удалить ответ.

        Returns
        -------
        - config : dict[str, Any]
            Конфиг, из которого удален ответ.
        """
        widgets: list[dict[str, dict]] = config[sett.LAYOUT][sett.WIDGETS]
        if widgets:
            for i in range(len(widgets)):
                if (
                    widgets[i].get(sett.LAYOUT) and
                    widgets[i][sett.LAYOUT].get(sett.NAME) == sett.RESPONSE
                ):
                    widgets.pop(i)
                    break
        return config

    # ============================ Private Methods ============================
    # -------------------------------------------------------------------------
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
                value = f"{str(value)} {sett.EURO_SYMBOL}"
            elif title == sett.WEIGHT_IT and value:
                value = f"{str(value)} {sett.KILO_SYMBOL}"
            elif title == sett.DEVELOPMENT_IT and value:
                value = f"{str(value)} {sett.METERS_SYMBOL}"
            elif (
                title == sett.PRICE_IT or title == sett.WEIGHT_IT
            ) and not value:
                value = sett.NOT_FOUND_IT

            title = f"{title}: "

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
