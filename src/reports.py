import json
from datetime import datetime
from typing import Optional
from functools import wraps
import pandas as pd


def report_decorator(func):
    """Декоратор для функций-отчетов, сохраняет результат в JSON-файл с именем по умолчанию"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{func.__name__}_{timestamp}.json"

        if isinstance(result, pd.DataFrame):
            data_to_save = result.to_dict(orient='records')
        else:
            data_to_save = result

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2, default=str)

        return result

    return wrapper


@report_decorator
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца.
    """
    df = transactions.copy()
    df['Дата'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')

    if date is None:
        end_date = datetime.now()
    else:
        end_date = pd.to_datetime(date)

    start_date = end_date - pd.DateOffset(months=3)

    date_filtered = df[(df['Дата'] >= start_date) & (df['Дата'] <= end_date)]

    result = date_filtered[
        (date_filtered['Категория'] == category) &
        (date_filtered['Сумма операции'] < 0)
        ]

    return result


# Проверка
if __name__ == "__main__":
    from utils import read_excel_file

    df = read_excel_file("data/operations.xlsx")

    # Проверяем для категории "Супермаркеты"
    result = spending_by_category(df, "Супермаркеты", "2021-12-31")
    print(f"Найдено транзакций: {len(result)}")
    print(f"Общая сумма трат: {abs(result['Сумма операции'].sum()):.2f}")
    print(result.head())