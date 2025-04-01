from decimal import Decimal
from handlers.excel_handler import ExcelHandler as EH


def test_travi_tg_excel_calculation():
    data = {
        'Tipo': 'TG',
        'Altezza': '130',
        'Base': '50',
        'Spessore': '1.5',
        'Staffa speciale': 'Sì',
        'Quantità': '<=1000',
        'Lunghezza': '3600'
    }

    rules = {
        'Altezza': {'min': 70, 'max': 170},
        'Lunghezza': {'exists': 1, 'numeric': 1, 'min': 1200, 'max': 3600}
    }

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B4',
        'Base': 'B6',
        'Spessore': 'B8',
        'Lunghezza': 'B12',
        'Staffa speciale': 'B14',
        'Quantità': 'B16'
    }

    cells_output = {'price': 'E4', 'weight': 'E6'}

    expected_data = {'price': Decimal('71.03'), 'weight': Decimal('21.00')}

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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


def test_travi_tg_wrong_data_passed():
    data = {
        'Tipo': 'TG',
        'Altezza': '130',
        'Base': '50',
        'Spessore': '1.5',
        'Staffa speciale': 'Sì',
        'Quantità': '<=1000',
        'Lunghezza': '900'
    }

    rules = {
        'Altezza': {'min': 70, 'max': 170},
        'Lunghezza': {'exists': 1, 'numeric': 1, 'min': 1200, 'max': 3600}
    }

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B4',
        'Base': 'B6',
        'Spessore': 'B8',
        'Lunghezza': 'B12',
        'Staffa speciale': 'B14',
        'Quantità': 'B16'
    }

    cells_output = {'price': 'E4', 'weight': 'E6'}

    expected_data = {
        'price': None,
        'weight': None,
        'error': 'Lunghezza should be more than 1200. You have 900'
    }

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

    print(data_to_check)
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


def test_travi_sat_excel_calculation():
    data = {
        'Tipo': 'SAT',
        'Altezza': '100',
        'Appoggio': 'Sì',
        'Spessore': '3.0',
        'Staffa speciale': 'Sì',
        'Quantità': '<=1000',
        'Lunghezza': '3000'
    }

    rules = {'Lunghezza': {'exists': 1, 'numeric': 1}}

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B21',
        'Spessore': 'B23',
        'Appoggio': 'B27',
        'Lunghezza': 'B29',
        'Staffa speciale': 'B31',
        'Quantità': 'B33'
    }

    cells_output = {'price': 'E21', 'weight': 'E23'}

    expected_data = {'price': Decimal('59.26'), 'weight': Decimal('13.25')}

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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


def test_travi_sat_wrong_data_passed():
    data = {
        'Tipo': 'SAT',
        'Altezza': '100',
        'Appoggio': 'Sì',
        'Spessore': '3.0',
        'Staffa speciale': 'Sì',
        'Quantità': '<=1000',
        'Lunghezza': 'abc'
    }

    rules = {'Lunghezza': {'exists': 1, 'numeric': 1}}

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B21',
        'Spessore': 'B23',
        'Appoggio': 'B27',
        'Lunghezza': 'B29',
        'Staffa speciale': 'B31',
        'Quantità': 'B33'
    }

    cells_output = {'price': 'E21', 'weight': 'E23'}

    expected_data = {
        'price': None,
        'weight': None,
        'error': 'Lunghezza should be numeric. You have abc'
    }

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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

    assert data_to_check['error'] == expected_data['error'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['error']}\n"
        f"Нашлось: {data_to_check['error']}"
    )


def test_travi_aperte_excel_calculation():
    data = {
        'Tipo': 'APERTE',
        'Altezza': '70',
        'Spessore': '2.0',
        'Staffa speciale': 'No',
        'Quantità': '>=1001',
        'Base': '45',
        'Lunghezza': '1200'
    }

    rules = {
        'Altezza': {'min': 70, 'max': 170},
        'Lunghezza': {'exists': 1, 'numeric': 1, 'min': 1200, 'max': 3600}
    }

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B37',
        'Base': 'B39',
        'Spessore': 'B41',
        'Lunghezza': 'B45',
        'Staffa speciale': 'B47',
        'Quantità': 'B49'
    }

    cells_output = {'price': 'E37', 'weight': 'E39'}

    expected_data = {'price': Decimal('15.84'), 'weight': Decimal('4.86')}

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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


def test_travi_aperte_wrong_data_passed():
    data = {
        'Tipo': 'APERTE',
        'Altezza': '70',
        'Spessore': '2.0',
        'Staffa speciale': 'No',
        'Quantità': '>=1001',
        'Base': '45',
        'Lunghezza': '1000'
    }

    rules = {
        'Altezza': {'min': 70, 'max': 170},
        'Lunghezza': {'exists': 1, 'numeric': 1, 'min': 1200, 'max': 3600}
    }

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B37',
        'Base': 'B39',
        'Spessore': 'B41',
        'Lunghezza': 'B45',
        'Staffa speciale': 'B47',
        'Quantità': 'B49'
    }

    cells_output = {'price': 'E37', 'weight': 'E39'}

    expected_data = {
        'price': None,
        'weight': None,
        'error': 'Lunghezza should be more than 1200. You have 1000'
    }

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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

    assert data_to_check['error'] == expected_data['error'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_data['error']}\n"
        f"Нашлось: {data_to_check['error']}"
    )


def test_travi_porta_skid_excel_calculation():
    data = {
        'Tipo': 'PORTA SKID',
        'Altezza': '40',
        'Base': '40',
        'Spessore': '2.0',
        'Lunghezza': '2000'
    }

    rules = {'Lunghezza': {'exists': 1, 'numeric': 1}}

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B53', 'Base': 'B55', 'Spessore': 'B57', 'Lunghezza': 'B61'
    }

    cells_output = {'price': 'E53', 'weight': 'E55'}

    expected_data = {'price': Decimal('15.74'), 'weight': Decimal('4.76')}

    handler = EH(data, rules, worksheet, cells_input, cells_output)
    data_to_check = handler.initiate_process()

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


def test_travi_porta_skid_wrong_data_passed():

    rules = {'Lunghezza': {'exists': 1, 'numeric': 1}}

    worksheet = 'Listino travi'

    cells_input = {
        'Altezza': 'B53', 'Base': 'B55', 'Spessore': 'B57', 'Lunghezza': 'B61'
    }

    cells_output = {'price': 'E53', 'weight': 'E55'}

    expected_data = [
        {
            'price': None,
            'weight': None,
            'error': 'Lunghezza field should not be empty'
        },
        {
            'price': None,
            'weight': None,
            'error': 'Lunghezza should be numeric. You have abc'
        }
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

        handler = EH(data, rules, worksheet, cells_input, cells_output)
        data_to_check = handler.initiate_process()

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

        assert data_to_check['error'] == expected_data[i]['error'], (
            f"Ошибка не совпадает.\n"
            f"Ожидалось: {expected_data[i]['error']}\n"
            f"Нашлось: {data_to_check['error']}"
        )
