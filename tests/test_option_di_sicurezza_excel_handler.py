from decimal import Decimal
from logic.calculator import Calculator


el_type = 'Option di sicurezza'
calculator = Calculator({}, el_type, {})


def test_option_di_sicurezza_excel_calculation_1():
    calculator.data = {
        'type': 'PARACOLPI', 'element_type': 'Frontale per montante serie 80'
    }
    calculator.choices = {'type': 'PARACOLPI'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('24.31'), 'weight': Decimal('4.90')}
    expected_post_message = 'N.B.! 4 tasselli non inclusi'

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


def test_option_di_sicurezza_excel_calculation_2():
    calculator.data = {
        'type': 'PARACOLPI', 'element_type': 'Frontale per montante serie 100'
    }
    calculator.choices = {'type': 'PARACOLPI'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('30.84'), 'weight': Decimal('5.50')}
    expected_post_message = 'N.B.! 4 tasselli non inclusi'

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


def test_option_di_sicurezza_excel_calculation_3():
    calculator.data = {
        'type': 'PARACOLPI',
        'element_type': 'Angolare per monttante serie 80/100 H=400mm'
    }
    calculator.choices = {'type': 'PARACOLPI'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('32.99'), 'weight': Decimal('6.40')}
    expected_post_message = 'N.B.! 3 tasselli non inclusi'

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


def test_option_di_sicurezza_excel_calculation_4():
    calculator.data = {
        'type': 'PARACOLPI',
        'element_type': 'Angolare frontale tipo Metelli'
    }
    calculator.choices = {'type': 'PARACOLPI'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('50.09'), 'weight': Decimal('10.99')}
    expected_post_message = 'N.B.! 4 tasselli non inclusi'

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


def test_option_di_sicurezza_excel_calculation_5():
    calculator.data = {
        'type': 'GUARDRAIL',
        'element_type': 'Bifronte (2 paracolpi + Sigma 255x3)'
    }
    calculator.choices = {'type': 'GUARDRAIL'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('129.65'), 'weight': Decimal('38.00')}
    expected_post_message = 'N.B.! 6 tasselli + 4 bulloni 10MAx25 non inclusi'

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


def test_option_di_sicurezza_excel_calculation_6():
    calculator.data = {
        'type': 'GUARDRAIL',
        'element_type': 'Monofronte (2 paracolpi + Sigma 255x3)'
    }
    calculator.choices = {'type': 'GUARDRAIL'}

    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('94.92'), 'weight': Decimal('24.00')}
    expected_post_message = 'N.B.! 6 tasselli + 4 bulloni 10MAx25 non inclusi'

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
