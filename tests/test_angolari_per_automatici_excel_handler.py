from decimal import Decimal
from logic.calculator import Calculator


el_type = 'Angolari per automatici'
calculator = Calculator({}, el_type, {})


def test_angolari_excel_calculation_1(excel_handler):
    data = {'section': '50x90', 'thickness': '2.0', 'length': '2000'}

    calculator.data = data
    calculator.excel_handler = excel_handler

    data_to_check, post_message = calculator.calc_data()

    expected_result = {
        'price': Decimal('13.39'),
        'weight': Decimal('4.48'),
        'development': Decimal('0.139')
    }
    expected_post_message = None

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_result), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_result)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_result['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_result['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_result['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_result['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert data_to_check['development'] == expected_result['development'], (
        f"Развертка не совпадает.\n"
        f"Ожидалось: {expected_result['development']}\n"
        f"Нашлось: {data_to_check['development']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_angolari_excel_calculation_2(excel_handler):
    data = {'section': '50x65', 'thickness': '3.0', 'length': '1500'}

    calculator.data = data
    calculator.excel_handler = excel_handler

    data_to_check, post_message = calculator.calc_data()

    expected_result = {
        'price': Decimal('12.06'),
        'weight': Decimal('4.13'),
        'development': Decimal('0.113')
    }
    expected_post_message = None

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_result), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_result)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_result['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_result['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_result['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_result['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert data_to_check['development'] == expected_result['development'], (
        f"Развертка не совпадает.\n"
        f"Ожидалось: {expected_result['development']}\n"
        f"Нашлось: {data_to_check['development']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_angolari_excel_calculation_3(excel_handler):
    data = {'section': '50x78', 'thickness': '1.5', 'length': '4100'}

    calculator.data = data
    calculator.excel_handler = excel_handler

    data_to_check, post_message = calculator.calc_data()

    expected_result = {
        'price': Decimal('19.79'),
        'weight': Decimal('6.12'),
        'development': Decimal('0.125')
    }
    expected_post_message = None

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_result), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_result)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_result['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_result['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_result['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_result['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert data_to_check['development'] == expected_result['development'], (
        f"Развертка не совпадает.\n"
        f"Ожидалось: {expected_result['development']}\n"
        f"Нашлось: {data_to_check['development']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_angolari_excel_validation_1(excel_handler):
    data = {'section': '50x78', 'thickness': '1.5', 'length': ''}

    calculator.data = data
    calculator.excel_handler = excel_handler

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'Lunghezza field should not be empty'

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_result), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_result)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_result['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_result['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_result['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_result['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_angolari_excel_validation_2(excel_handler):
    data = {'section': '50x78', 'thickness': '1.5', 'length': 'abc'}

    calculator.data = data
    calculator.excel_handler = excel_handler

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'Lunghezza should be numeric. You have abc'

    assert data_to_check, (
        "Метод initiate_process() вернул пустой результат или None"
    )

    assert len(data_to_check) == len(expected_result), (
        f"Количество данных не совпадает.\n"
        f"Ожидалось: {len(expected_result)}\n"
        f"Нашлось: {len(data_to_check)}"
    )

    assert data_to_check['price'] == expected_result['price'], (
        f"Цена не совпадает.\n"
        f"Ожидалось: {expected_result['price']}\n"
        f"Нашлось: {data_to_check['price']}"
    )

    assert data_to_check['weight'] == expected_result['weight'], (
        f"Вес не совпадает.\n"
        f"Ожидалось: {expected_result['weight']}\n"
        f"Нашлось: {data_to_check['weight']}"
    )

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )
