import json
import logging
import os
from datetime import datetime
from functools import wraps
from typing import Optional

import pandas as pd

logger = logging.getLogger(__name__)


def report_decorator(func):
    """Декоратор для функций-отчетов, сохраняет результат в JSON-файл с именем по умолчанию"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"Запуск функции-отчета: {func.__name__}")

        result = func(*args, **kwargs)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        filename = os.path.join(project_root, f"report_{func.__name__}_{timestamp}.json")

        logger.info(f"Сохранение отчета в файл: {filename}")

        if isinstance(result, pd.DataFrame):
            data_to_save = result.to_dict(orient="records")
            logger.debug(f"Сохранено {len(result)} записей из DataFrame")
        else:
            data_to_save = result
            logger.debug(f"Сохранен результат типа {type(result)}")

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=2, default=str)

        logger.info(f"Отчет {func.__name__} успешно сохранен")

        return result

    return wrapper


@report_decorator
def spending_by_category(transactions: pd.DataFrame, category: str, date: Optional[str] = None) -> pd.DataFrame:
    """
    Возвращает траты по заданной категории за последние 3 месяца.
    """
    logger.info(f"Анализ трат по категории: {category}")

    df = transactions.copy()
    print(df)
    df["Дата"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce")
    print(df)

    if date is None:
        end_date = datetime.now()
        logger.info(f"Дата не указана, используем текущую: {end_date.date()}")
    else:
        end_date = pd.to_datetime(date, dayfirst=True)
        logger.info(f"Используем указанную дату: {end_date.date()}")

    start_date = end_date - pd.DateOffset(months=3)
    logger.info(f"Период анализа: с {start_date.date()} по {end_date.date()}")

    date_filtered = df[(df["Дата"] >= start_date) & (df["Дата"] <= end_date)]
    print(date_filtered)

    result = date_filtered[(date_filtered["Категория"] == category) & (date_filtered["Сумма операции"] < 0)]

    return result
