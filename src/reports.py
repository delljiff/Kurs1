import json
import logging
from datetime import datetime
from typing import Optional, Any, Callable
import pandas as pd

# Явный импорт сервисов для mypy
from src import services

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def report_to_file(filename: Optional[str] = None) -> Callable:
    """Декоратор для сохранения результата функции в JSON-файл"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result: Any = func(*args, **kwargs)
            out_file: str = filename if filename else f"report_{func.__name__}.json"

            if isinstance(result, pd.DataFrame):
                result.to_json(out_file, force_ascii=False, indent=2, orient='records', date_format='iso')
            else:
                with open(out_file, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)

            logger.info(f"Отчёт сохранён в {out_file}")
            return result
        return wrapper
    return decorator


@report_to_file()
def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца.

    Параметры:
    - transactions: DataFrame с колонками 'Дата операции', 'Категория', 'Сумма операции'
    - category: название категории
    - date: опционально, дата в формате 'YYYY-MM-DD' или 'DD.MM.YYYY'
    """
    # Определяем целевую дату
    if date is None:
        target_date: datetime = datetime.now()
    else:
        try:
            target_date = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            target_date = datetime.strptime(date, "%d.%m.%Y")

    # Работаем с копией
    df: pd.DataFrame = transactions.copy()

    # Парсим даты
    df['date_parsed'] = pd.to_datetime(df['Дата операции'], dayfirst=True, errors='coerce')

    # Дата 3 месяца назад
    three_months_ago: pd.Timestamp = target_date - pd.DateOffset(days=90)

    # Маски для фильтрации
    mask_category: pd.Series = df['Категория'] == category
    mask_date: pd.Series = (df['date_parsed'] >= three_months_ago) & (df['date_parsed'] <= target_date)

    # Применяем фильтры
    result: pd.DataFrame = df[mask_category & mask_date]
    result = result.drop(columns=['date_parsed'])

    logger.info(f"Найдено {len(result)} трат по категории '{category}' за последние 3 месяца")
    return result


if __name__ == "__main__":
    transactions_raw = services.load_transactions_from_excel("data/operations.xlsx")
    df: pd.DataFrame = pd.DataFrame(transactions_raw)
    result: pd.DataFrame = spending_by_category(df, "Супермаркеты", "31.12.2021")
    print(result.head())
