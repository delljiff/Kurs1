import logging
import math
from datetime import datetime
from typing import Any, Dict, List

import openpyxl

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

Transaction = Dict[str, Any]


def filter_by_month(transactions: List[Transaction], month: str) -> List[Transaction]:
    """Фильтрует транзакции по месяцу"""
    logger.info(f"Фильтрация транзакций за месяц {month}")

    def is_same_month(transaction: Transaction) -> bool:
        date_str: str = transaction["Дата операции"][:10]

        try:
            transaction_date: datetime = datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            transaction_date = datetime.strptime(date_str, "%d.%m.%Y")

        return transaction_date.strftime("%Y-%m") == month

    filtered: List[Transaction] = list(filter(is_same_month, transactions))
    logger.info(f"Отфильтровано транзакций: {len(filtered)}")
    return filtered


def round_up_to_limit(amount: float, limit: float) -> float:
    """Округляет сумму вверх до ближайшего числа, кратного limit"""
    return math.ceil(abs(amount) / limit) * limit


def calculate_saved(amount: float, limit: float) -> float:
    """Возвращает сумму, которая попадёт в копилку с одной транзакции"""
    rounded: float = round_up_to_limit(amount, limit)
    return rounded - abs(amount)


def investment_bank(month: str, transactions: List[Transaction], limit: int) -> float:
    """Основная функция сервиса 'Инвесткопилка'"""
    logger.info(f"=== Запуск investment_bank для месяца {month} с лимитом {limit} ===")

    filtered: List[Transaction] = filter_by_month(transactions, month)
    amounts: map = map(lambda t: t["Сумма операции"], filtered)
    saved: map = map(lambda a: calculate_saved(a, limit), amounts)
    total: float = sum(saved)
    total = round(total, 2)

    logger.info(f"Итоговая сумма в копилке: {total} ₽")
    return total


def load_transactions_from_excel(filepath: str) -> List[Transaction]:
    """Загружает транзакции из Excel-файла"""
    logger.info(f"Загрузка транзакций из Excel: {filepath}")

    wb: openpyxl.Workbook = openpyxl.load_workbook(filepath, data_only=True)
    sheet = wb.active

    # mypy ругается, что sheet может быть None. Проверяем.
    if sheet is None:
        logger.error("Не удалось получить активный лист Excel")
        return []

    transactions: List[Transaction] = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        if row is None:
            continue

        date = row[0]
        amount = row[4]

        if date is not None and amount is not None:
            # Преобразуем дату в строку, сумму — во float
            date_str: str = str(date)
            amount_float: float = float(str(amount))

            transactions.append({
                "Дата операции": date_str[:10],  # сразу обрезаем до 10 символов
                "Сумма операции": amount_float
            })

    logger.info(f"Загружено {len(transactions)} транзакций")
    return transactions


if __name__ == "__main__":
    transactions: List[Transaction] = load_transactions_from_excel("data/operations.xlsx")
    result: float = investment_bank("2021-12", transactions, 50)

    print(f"\n{'=' * 40}")
    print(f"ИТОГО В КОПИЛКЕ: {result} ₽")
    print(f"{'=' * 40}")
