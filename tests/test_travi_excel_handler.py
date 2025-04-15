from decimal import Decimal
from logic.calculator import Calculator


def test_travi_tg_excel_calculation(excel_handler):
    data = {
        'type': 'TG',
        'height': '130',
        'base': '50',
        'thickness': '1.5',
        'hook_special': 'Sì',
        'amount': '<=1000',
        'length': '3600'
    }

    choices = {
        'type': 'TG'
    }

    el_type = 'Travi'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    expected_data = {'price': Decimal('71.03'), 'weight': Decimal('21.00')}

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_travi_tg_wrong_data_passed(excel_handler):
    data = {
        'type': 'TG',
        'height': '130',
        'base': '50',
        'thickness': '1.5',
        'hook_special': 'Sì',
        'amount': '<=1000',
        'length': '900'
    }

    choices = {
        'type': 'TG'
    }

    el_type = 'Travi'

    expected_data = {
        'price': None,
        'weight': None,
    }

    expected_post_message = 'Lunghezza should be more than 1200. You have 900'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_travi_sat_excel_calculation(excel_handler):
    data = {
        'type': 'SAT',
        'height': '100',
        'support': 'Sì',
        'thickness': '3.0',
        'hook_special': 'Sì',
        'amount': '<=1000',
        'length': '3000'
    }

    choices = {
        'type': 'SAT'
    }

    el_type = 'Travi'

    expected_data = {'price': Decimal('59.26'), 'weight': Decimal('13.25')}

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_travi_sat_wrong_data_passed(excel_handler):
    data = {
        'type': 'SAT',
        'height': '100',
        'support': 'Sì',
        'thickness': '3.0',
        'hook_special': 'Sì',
        'amount': '<=1000',
        'length': 'abc'
    }

    choices = {
        'type': 'SAT'
    }

    el_type = 'Travi'

    expected_data = {
        'price': None,
        'weight': None
    }

    expected_post_message = 'Lunghezza should be numeric. You have abc'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_travi_aperte_excel_calculation(excel_handler):
    data = {
        'type': 'APERTE',
        'height': '70',
        'thickness': '2.0',
        'hook_special': 'No',
        'amount': '>=1001',
        'base': '45',
        'length': '1200'
    }

    choices = {
        'type': 'APERTE'
    }

    el_type = 'Travi'

    expected_data = {'price': Decimal('15.84'), 'weight': Decimal('4.86')}

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_travi_aperte_wrong_data_passed(excel_handler):
    data = {
        'type': 'APERTE',
        'height': '70',
        'thickness': '2.0',
        'hook_special': 'No',
        'amount': '>=1001',
        'base': '45',
        'length': '1000'
    }

    choices = {
        'type': 'APERTE'
    }

    el_type = 'Travi'

    expected_data = {
        'price': None,
        'weight': None
    }

    expected_post_message = 'Lunghezza should be more than 1200. You have 1000'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_travi_porta_skid_excel_calculation(excel_handler):
    data = {
        'type': 'PORTA SKID',
        'height': '40',
        'base': '40',
        'thickness': '2.0',
        'length': '2000'
    }

    choices = {
        'type': 'PORTA SKID'
    }

    el_type = 'Travi'

    expected_data = {'price': Decimal('15.74'), 'weight': Decimal('4.76')}

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_data), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_data)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_data['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_data['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_data['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_travi_porta_skid_wrong_data_passed(excel_handler):

    choices = {
        'type': 'PORTA SKID'
    }

    el_type = 'Travi'

    calculator = Calculator({}, el_type, choices, excel_handler)

    expected_data = [
        {
            'price': None,
            'weight': None
        },
        {
            'price': None,
            'weight': None
        }
    ]

    expected_post_messages = [
        'Lunghezza field should not be empty',
        'Lunghezza should be numeric. You have abc'
    ]

    lunghezze = ['', 'abc']
    for i in range(len(lunghezze)):
        data = {
            'Tipo': 'PORTA SKID',
            'Altezza': '40',
            'Base': '40',
            'Spessore': '2.0',
            'Lunghezza': lunghezze[i]
        }

        calculator.data = data
        data_to_check, post_message = calculator.calc_data()

        assert data_to_check, (
            "Метод initiate_process() вернул пустой результат или None"
        )

        assert len(data_to_check) == len(expected_data[i]), (
            f"Количество данных не совпадает.\n"
            f"Ожидалось: {len(expected_data)}\n"
            f"Нашлось: {len(data_to_check)}"
        )

        assert data_to_check['price'] == expected_data[i]['price'], (
            f"Цена не совпадает.\n"
            f"Ожидалось: {expected_data[i]['price']}\n"
            f"Нашлось: {data_to_check['price']}"
        )

        assert data_to_check['weight'] == expected_data[i]['weight'], (
            f"Вес не совпадает.\n"
            f"Ожидалось: {expected_data[i]['weight']}\n"
            f"Нашлось: {data_to_check['weight']}"
        )

        assert post_message == expected_post_messages[i], (
            f"Сообщение не совпадает.\n"
            f"Ожидалось: {expected_post_messages[i]}\n"
            f"Нашлось: {post_message}"
        )
