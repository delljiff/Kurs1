import logging
from typing import Any, Dict

import pandas as pd

logger = logging.getLogger(__name__)


def best_categories_of_high_cashback(data: pd.DataFrame, year: str, month: str) -> Dict[str, Any]:
    """Анализирует выгодные категории для повышенного кешбэка"""
    logger.info(f"Начинаем анализ кешбэка за {year}-{month}")

    df = data.copy()

    df["Год-Месяц"] = pd.to_datetime(df["Дата операции"], dayfirst=True, errors="coerce").dt.strftime("%Y-%m")

    target = f"{year}-{int(month):02d}"
    logger.info(f"Фильтруем данные за {target}")

    month_data = df[df["Год-Месяц"] == target]
    logger.debug(f"Найдено {len(month_data)} записей")

    expenses_with_cashback = month_data[
        (month_data["Сумма операции"] < 0) & (month_data["Кэшбэк"].notna()) & (month_data["Категория"].notna())
    ]

    logger.info(f"Найдено {len(expenses_with_cashback)} транзакций с кешбэком")

    result = expenses_with_cashback.groupby("Категория")["Кэшбэк"].sum().to_dict()

    result = dict(sorted(result.items(), key=lambda x: x[1], reverse=True))
    logger.info(f"Получили {len(result)} категорий с кешбэком")

    return result
