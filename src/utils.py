import json
import os.path
from datetime import datetime

PATH_DATA = os.path.abspath('../data')
OPERATIONS_FILE_PATH = os.path.join(PATH_DATA, 'operations.json')

def read_operations(path: str = OPERATIONS_FILE_PATH) -> list:
    """
    Чтение данных из JSON-файла.

    :rtype: object
    :param path: путь к файлу с данными (по умолчанию берется OPERATIONS_FILE_PATH).
    :return: список объектов операций.
    """
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    return data

def last_n_operations(data: list, n: int = 5, state: str = 'EXECUTED') -> list:
    """
    Получение n последних выполненных операций.

    :param data: список объектов операций.
    :param n: количество операций (по умолчанию 5).
    :param state: состояние операций (по умолчанию 'EXECUTED').
    :return: список выполненных операций.
    """
    executed_operations = filter(lambda x: 'state' in x and x['state'] == state, data)
    last_n_operations = sorted(executed_operations, key=lambda x: x['date'], reverse=True)[:n]
    return last_n_operations


def format_operation(operation: dict) -> str:
    """
    Форматирование строки с информацией о финансовой операции.

    :param operation: объект операции.
    :return: строка с информацией о финансовой операции.
    """
    operation_amount = operation['operationAmount']
    amount = float(operation_amount['amount'])
    currency = operation_amount['currency']['name']
    date = datetime.strptime(operation['date'], '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')
    description = operation['description']
    frm = operation.get('from')
    to = operation.get('to')

    if to and len(to) > 8:
        to = 'Счет **' + to[-4:]
    if frm and len(frm) > 8:
        if frm.split(" ")[0] == "Счет":
            frm = 'Счет **' + to[-4:]
        else:
            frm_bill_name = " ".join(frm.split(" ")[:-1])
            frm_bill_number = frm.split(" ")[-1]
            frm = f'{frm_bill_name} {frm_bill_number[:4]} {frm_bill_number[5:7]}** **** {frm_bill_number[-4:]}'
    return f"{date} {description}:\n{frm} -> {to}\n{amount:.2f} {currency}"


def print_last_n_operations(data: list, n: int = 5, state: str = 'EXECUTED') -> None:
    """
    Вывод n последних выполненных операций.

    :param data: список объектов операций.
    :param n: количество выводимых операций (по умолчанию 5).
    :param state: состояние операций (по умолчанию 'EXECUTED').
    """
    operations = last_n_operations(data, n=n, state=state)

    for operation in operations:
        formatted_operation = format_operation(operation)
        print(formatted_operation)
        print()