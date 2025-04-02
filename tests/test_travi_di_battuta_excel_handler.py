from decimal import Decimal
from logic.calculator import Calculator


def test_travi_di_battuta_excel_calculation_1():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'Sì',
        'amount': '<=500',
        'fold': 'Sì',
        'length': '2000'
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('35.50'), 'weight': None}
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

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_travi_di_battuta_excel_calculation_2():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'No',
        'amount': '>=501',
        'fold': 'Sì',
        'length': '3500'
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'N.B.! Per lunghezza > 3300 contattare sede.'

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


def test_travi_di_battuta_excel_calculation_3():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'No',
        'amount': '>=501',
        'fold': 'Sì',
        'length': '3300'
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('42.50'), 'weight': None}
    expected_post_message = 'N.B.! Per lunghezza > 3300 contattare sede.'

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


def test_travi_di_battuta_excel_validation_1():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'No',
        'amount': '>=501',
        'fold': 'Sì',
        'length': ''
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
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


def test_travi_di_battuta_excel_validation_2():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'No',
        'amount': '>=501',
        'fold': 'Sì',
        'length': 'abc'
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
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


def test_travi_di_battuta_excel_validation_3():
    data = {
        'type': 'Tubolare 60x40x2',
        'standart_hook': 'No',
        'amount': '>=501',
        'fold': 'Sì',
        'length': '1111'
    }

    choices = {}
    el_type = 'Travi di Battuta'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'Lunghezza should be multiple of 10. You have 1111'

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
