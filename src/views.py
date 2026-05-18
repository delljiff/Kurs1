from typing import Any, Dict
import pandas as pd
import logging
from src.utils import get_card_info, get_currency_rates, get_greeting, get_stock_prices, get_top_five_transactions

logger = logging.getLogger(__name__)


def main_page(transactions: pd.DataFrame, date: str) -> Dict[str, Any]:
    """
    Функция главной страницы, включающая набор функций.
    Принимает на вход  строку с датой и временем в формате YYYY-MM-DD HH:MM:SS и возвращает JSON-ответ.
    """
    logger.info(f"Формирование главной страницы для даты: {date}")

    start_date = f"01{date[2:]}"
    end_date = date

    logger.debug(f"Период фильтрации: с {start_date} по {end_date}")

    filtered_df = transactions[transactions['Дата операции'].between(start_date, end_date)]
    logger.debug(f"Отфильтровано {len(filtered_df)} транзакций")

    data_json = {
        "greeting": get_greeting(),
        "cards": get_card_info(filtered_df),
        "top_transactions": get_top_five_transactions(filtered_df),
        "currency_rates": get_currency_rates("../user_settings.json"),
        "stock_prices": get_stock_prices("../user_settings.json"),
    }

    logger.info(f"Сформировано {len(data_json)} блоков данных для главной страницы")
    logger.debug(f"Ключи данных: {list(data_json.keys())}")

    return data_json
