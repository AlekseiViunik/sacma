from decimal import Decimal
from logic.calculator import Calculator


def test_pianetti_excel_calculation_1(excel_handler):
    data = {'thickness': '0.6', 'depth': '100', 'length': '1000'}

    choices = {}
    el_type = 'Pianetti'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, _ = calculator.calc_data()

    expected_result = {'price': Decimal('2.79'), 'weight': Decimal('1.05')}

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


def test_pianetti_excel_calculation_2(excel_handler):
    data = {'thickness': '0.9', 'depth': '300', 'length': '400'}

    choices = {}
    el_type = 'Pianetti'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, _ = calculator.calc_data()

    expected_result = {'price': Decimal('3.23'), 'weight': Decimal('1.31')}

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


def test_pianetti_wrong_data_passed(excel_handler):
    data = {'thickness': '0.9', 'depth': '300', 'length': '300'}

    choices = {}
    el_type = 'Pianetti'

    calculator = Calculator(data, el_type, choices, excel_handler)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = 'Lunghezza should be more than 400. You have 300'

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
