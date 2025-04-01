from decimal import Decimal
from logic.calculator import Calculator


def test_automha_excel_calculation():
    datas = [
        {'type': 'AUTOMHA', 'element': "Profilo a 'Z' 50x190x60x2"},
        {'type': 'AUTOMHA', 'element': "Profilo a 'Z' 50x190x60x2.5"},
        {'type': 'AUTOMHA', 'element': "Profilo a 'Z' 50x190x60x3"},
        {'type': 'AUTOMHA', 'element': "Profilo a 'Z' 50x190x60x3.5"}
    ]

    expected_results = [
        {
            'price': Decimal('16.37'),
            'weight': None,
            'preparation': Decimal('600.00')
        },
        {
            'price': Decimal('19.10'),
            'weight': None,
            'preparation': Decimal('600.00')
        },
        {
            'price': Decimal('21.85'),
            'weight': None,
            'preparation': Decimal('600.00')
        },
        {'price': None, 'weight': None}
    ]

    expected_post_messages = [
        'ATTENZIONE! Il prezzo è per metro lineare!',
        'ATTENZIONE! Il prezzo è per metro lineare!',
        'ATTENZIONE! Il prezzo è per metro lineare!',
        'Il prezzo è ancora inesistente'
    ]

    choices = {'type': 'AUTOMHA'}
    el_type = 'Satellitare'

    for i in range(len(datas)):

        calculator = Calculator(datas[i], el_type, choices)
        data_to_check, post_message = calculator.calc_data()

        assert data_to_check, (
            "Метод initiate_process() вернул пустой результат или None"
        )

        assert len(data_to_check) == len(expected_results[i]), (
            f"Количество данных не совпадает.\n"
            f"Ожидалось: {len(expected_results[i])}\n"
            f"Нашлось: {len(data_to_check)}"
        )

        assert data_to_check['price'] == expected_results[i]['price'], (
            f"Цена не совпадает.\n"
            f"Ожидалось: {expected_results[i]['price']}\n"
            f"Нашлось: {data_to_check['price']}"
        )

        assert data_to_check['weight'] == expected_results[i]['weight'], (
            f"Вес не совпадает.\n"
            f"Ожидалось: {expected_results[i]['weight']}\n"
            f"Нашлось: {data_to_check['weight']}"
        )

        assert (
            data_to_check.get('preparation') ==
            expected_results[i].get('preparation')
        ), (
            f"Стоимость подготовки не совпадает.\n"
            f"Ожидалось: {expected_results[i].get('preparation')}\n"
            f"Нашлось: {data_to_check.get('preparation')}"
        )

        assert post_message == expected_post_messages[i], (
            f"Сообщение не совпадает.\n"
            f"Ожидалось: {expected_post_messages[i]}\n"
            f"Нашлось: {post_message}"
        )


def test_other_excel_calculation_2():
    datas = [
        {
            'type': 'Altro',
            'element': "Battute posteriori per pallet e satellite"
        },
        {'type': 'Altro', 'element': "Battute posteriori solo pallet"},
        {'type': 'Altro', 'element': "Angolare zincato di fissaggio 'Z'"},
        {'type': 'Altro', 'element': "Mensola di ingresso"},
        {'type': 'Altro', 'element': "Giunti"},
        {'type': 'Altro', 'element': "Inviti satellitare"},
        {'type': 'Altro', 'element': "DISTANZIALI L=1368mm"}
    ]

    expected_results = [
        {
            'price': Decimal('7.00'),
            'weight': None,
            'preparation': Decimal('91.00')
        },
        {'price': Decimal('2.50'), 'weight': None},
        {'price': Decimal('2.44'), 'weight': None},
        {
            'price': Decimal('21.36'),
            'weight': None,
            'preparation': Decimal('91.00')
        },
        {'price': Decimal('4.25'), 'weight': None},
        {'price': Decimal('17.77'), 'weight': None},
        {
            'price': Decimal('5.12'),
            'weight': None,
            'preparation': Decimal('35.00')
        }
    ]

    expected_post_messages = [
        None,
        None,
        'Bulloni 10x25 (2/cad) + bulloni 10x20 TT (2/cad) non inclusi',
        'Bulloni 10x25 (1/cad) + bulloni 10x20 TT (2/cad) non inclusi',
        'Bulloni 10x25 (2/cad) + bulloni 10x20 TT (2/cad) non inclusi',
        None,
        None
    ]

    choices = {'type': 'Altro'}
    el_type = 'Satellitare'

    for i in range(len(datas)):

        calculator = Calculator(datas[i], el_type, choices)
        data_to_check, post_message = calculator.calc_data()

        assert data_to_check, (
            "Метод initiate_process() вернул пустой результат или None"
        )

        assert len(data_to_check) == len(expected_results[i]), (
            f"Количество данных не совпадает.\n"
            f"Ожидалось: {len(expected_results[i])}\n"
            f"Нашлось: {len(data_to_check)}"
        )

        assert data_to_check['price'] == expected_results[i]['price'], (
            f"Цена не совпадает.\n"
            f"Ожидалось: {expected_results[i]['price']}\n"
            f"Нашлось: {data_to_check['price']}"
        )

        assert data_to_check['weight'] == expected_results[i]['weight'], (
            f"Вес не совпадает.\n"
            f"Ожидалось: {expected_results[i]['weight']}\n"
            f"Нашлось: {data_to_check['weight']}"
        )

        assert (
            data_to_check.get('preparation') ==
            expected_results[i].get('preparation')
        ), (
            f"Стоимость подготовки не совпадает.\n"
            f"Ожидалось: {expected_results[i].get('preparation')}\n"
            f"Нашлось: {data_to_check.get('preparation')}"
        )

        assert post_message == expected_post_messages[i], (
            f"Сообщение не совпадает.\n"
            f"Ожидалось: {expected_post_messages[i]}\n"
            f"Нашлось: {post_message}"
        )
