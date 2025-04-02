from decimal import Decimal
from logic.calculator import Calculator


def test_fiancate_excel_calculation_1():
    data = {
        'type': 'Non-sismo',
        'pieces': '1',
        'section_1': '100/20',
        'welded_base_plates': 'No',
        'automatic_top': 'No',
        'depth': '1000',
        'height_1': '9000',
        'n_diagonals_1': '10'
    }
    choices = {'pieces': '1', 'type': 'Non-sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('296.63')}

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_excel_calculation_2():
    data = {
        'type': 'Non-sismo',
        'pieces': '3',
        'section_1': '80/25',
        'welded_base_plates': 'Sì',
        'automatic_top': 'Sì',
        'section_2': '80/30',
        'section_3': '80/20',
        'depth': '1300',
        'height_1': '9000',
        'n_diagonals_1': '9',
        'height_2': '6000',
        'n_diagonals_2': '6',
        'height_3': '3000',
        'n_diagonals_3': '3'
    }
    choices = {'pieces': '3', 'type': 'Non-sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('695.10')}

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_max_height_validation():
    data = {
        'type': 'Non-sismo',
        'pieces': '1',
        'section_1': '100/20',
        'welded_base_plates': 'No',
        'automatic_top': 'No',
        'depth': '1000',
        'height_1': '15000',
        'n_diagonals_1': '10'
    }
    choices = {'pieces': '1', 'type': 'Non-sismo'}
    el_type = 'FIancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = (
        'Altezza 1 should be less than 13500. You have 15000'
    )

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_multiple_validation():
    data = {
        'type': 'Non-sismo',
        'pieces': '1',
        'section_1': '100/20',
        'welded_base_plates': 'No',
        'automatic_top': 'No',
        'depth': '1000',
        'height_1': '10000',
        'n_diagonals_1': '10'
    }
    choices = {'pieces': '1', 'type': 'Non-sismo'}
    el_type = 'FIancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = (
        'Altezza 1 should be multiple of 75. You have 10000'
    )

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message == expected_post_message, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: {expected_post_message}\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_sismo_calculation_1():
    data = {
        'type': 'Sismo',
        'pieces': '1',
        'section_1': '100/20',
        'automatic_top': 'Sì',
        'diagonals_1_1': '20/10',
        'diagonals_1_2': '15/10',
        'diagonals_1_3': '10/10',
        'traverse_1_1': '10/10',
        'traverse_1_2': '15/10',
        'typology_pb': 'Speciale',
        'base_thickness': '12',
        'depth': '1300',
        'height_1': '9000',
        'n_diagonals_1_1': '4',
        'n_diagonals_1_2': '5',
        'n_diagonals_1_3': '',
        'n_traverse_1_1': '7',
        'n_traverse_1_2': '3',
        'boot_height': '500',
        'base_length': '320',
        'base_depth': '200',
        'n_holes': '4'
    }

    choices = {'pieces': '1', 'type': 'Sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('461.67'), 'weight': Decimal('166.83')}

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_sismo_calculation_2():
    data = {
        'type': 'Sismo',
        'pieces': '2',
        'section_1': '100/20',
        'automatic_top': 'Sì',
        'diagonals_1_1': '15/10',
        'diagonals_1_2': '20/10',
        'diagonals_1_3': '25/10',
        'traverse_1_1': '15/10',
        'traverse_1_2': '20/10',
        'typology_pb': 'Speciale',
        'base_thickness': '20',
        'section_2': '100/30',
        'diagonals_2_1': '10/10',
        'diagonals_2_2': '15/10',
        'diagonals_2_3': '20/10',
        'traverse_2_1': '10/10',
        'traverse_2_2': '15/10',
        'depth': '1200',
        'height_1': '9000',
        'n_diagonals_1_1': '2',
        'n_diagonals_1_2': '3',
        'n_diagonals_1_3': '4',
        'n_traverse_1_1': '5',
        'n_traverse_1_2': '5',
        'boot_height': '1000',
        'base_length': '300',
        'base_depth': '200',
        'n_holes': '6',
        'height_2': '6000',
        'n_diagonals_2_1': '3',
        'n_diagonals_2_2': '2',
        'n_diagonals_2_3': '1',
        'n_traverse_2_1': '3',
        'n_traverse_2_2': '4'
    }

    choices = {'pieces': '2', 'type': 'Sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': Decimal('851.11'), 'weight': Decimal('317.53')}

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_sismo_calculation_3():
    data = {
        'type': 'Sismo',
        'pieces': '3',
        'section_1': '120x110/20',
        'automatic_top': 'Sì',
        'diagonals_1_1': '10/10',
        'diagonals_1_2': '15/10',
        'diagonals_1_3': '20/10',
        'traverse_1_1': '15/10',
        'traverse_1_2': '20/10',
        'typology_pb': 'Standard',
        'base_thickness': '7',
        'section_2': '120x110/30',
        'diagonals_2_1': '15/10',
        'diagonals_2_2': '10/10',
        'diagonals_2_3': '10/10',
        'traverse_2_1': '10/10',
        'traverse_2_2': '10/10',
        'section_3': '120x110/25',
        'diagonals_3_1': '10/10',
        'diagonals_3_2': '20/10',
        'diagonals_3_3': '25/10',
        'traverse_3_1': '10/10',
        'traverse_3_2': '20/10',
        'depth': '1250',
        'height_1': '12000',
        'n_diagonals_1_1': '3',
        'n_diagonals_1_2': '4',
        'n_diagonals_1_3': '5',
        'n_traverse_1_1': '6',
        'n_traverse_1_2': '7',
        'boot_height': '',
        'base_length': '',
        'base_depth': '',
        'n_holes': '',
        'height_2': '8400',
        'n_diagonals_2_1': '7',
        'n_diagonals_2_2': '',
        'n_diagonals_2_3': '',
        'n_traverse_2_1': '8',
        'n_traverse_2_2': '',
        'height_3': '6450',
        'n_diagonals_3_1': '1',
        'n_diagonals_3_2': '2',
        'n_diagonals_3_3': '3',
        'n_traverse_3_1': '3',
        'n_traverse_3_2': '4'
    }

    choices = {'pieces': '3', 'type': 'Sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {
        'price': Decimal('1738.93'), 'weight': Decimal('663.61')
    }

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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

    assert post_message is None, (
        f"Сообщение не совпадает.\n"
        f"Ожидалось: None\n"
        f"Нашлось: {post_message}"
    )


def test_fiancate_diagonals_validation():
    data = {
        'type': 'Sismo',
        'pieces': '3',
        'section_1': '120x110/20',
        'automatic_top': 'Sì',
        'diagonals_1_1': '10/10',
        'diagonals_1_2': '15/10',
        'diagonals_1_3': '20/10',
        'traverse_1_1': '15/10',
        'traverse_1_2': '20/10',
        'typology_pb': 'Standard',
        'base_thickness': '7',
        'section_2': '120x110/30',
        'diagonals_2_1': '15/10',
        'diagonals_2_2': '10/10',
        'diagonals_2_3': '10/10',
        'traverse_2_1': '10/10',
        'traverse_2_2': '10/10',
        'section_3': '120x110/25',
        'diagonals_3_1': '10/10',
        'diagonals_3_2': '20/10',
        'diagonals_3_3': '25/10',
        'traverse_3_1': '10/10',
        'traverse_3_2': '20/10',
        'depth': '1250',
        'height_1': '12000',
        'n_diagonals_1_1': '3',
        'n_diagonals_1_2': '4',
        'n_diagonals_1_3': '5',
        'n_traverse_1_1': '6',
        'n_traverse_1_2': '7',
        'boot_height': '',
        'base_length': '',
        'base_depth': '',
        'n_holes': '',
        'height_2': '8400',
        'n_diagonals_2_1': '7',
        'n_diagonals_2_2': '',
        'n_diagonals_2_3': '',
        'n_traverse_2_1': '10',
        'n_traverse_2_2': '',
        'height_3': '6450',
        'n_diagonals_3_1': '1',
        'n_diagonals_3_2': '2',
        'n_diagonals_3_3': '3',
        'n_traverse_3_1': '3',
        'n_traverse_3_2': '4'
    }

    choices = {'pieces': '3', 'type': 'Sismo'}
    el_type = 'Fiancate'

    calculator = Calculator(data, el_type, choices)
    data_to_check, post_message = calculator.calc_data()

    expected_result = {'price': None, 'weight': None}
    expected_post_message = (
        'Error! Check diagonals and traverses amount!'
    )

    assert data_to_check, (
        "Метод calc_data() вернул пустой результат или None"
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
