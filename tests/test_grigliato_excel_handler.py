from decimal import Decimal
from logic.calculator import Calculator


def test_grigliato_excel_calculation_1():
    data = {
        'type': 'Grigliato',
        'thickness': '1.5',
        'base': '250x50',
        'length': '3600'
    }

    choices = {'type': 'Grigliato'}
    el_type = 'Grigliato'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('37.69'), 'weight': Decimal('15.70')}
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


def test_grigliato_excel_calculation_2():
    data = {
        'type': 'Grigliato',
        'thickness': '1.2',
        'base': '270x50',
        'length': '680'
    }

    choices = {'type': 'Grigliato'}
    el_type = 'Grigliato'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('6.17'), 'weight': Decimal('2.50')}
    expected_post_message = 'N.B.! Solo grandi quantitativi. Contatare sede!'

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


def test_grigliato_excel_calculation_3():
    data = {
        'type': 'Grigliato',
        'thickness': '2.0',
        'base': '270x40',
        'length': '6000'
    }

    choices = {'type': 'Grigliato'}
    el_type = 'Grigliato'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'ATTENZIONE! Per la base 270x40 contatare sede!'

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


def test_grigliato_wrong_data_passed():
    data = {
        'type': 'Grigliato',
        'thickness': '1.5',
        'base': '250x50',
        'length': '6100'
    }

    choices = {'type': 'Grigliato'}
    el_type = 'Grigliato'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'Lunghezza should be less than 6000. You have 6100'

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
