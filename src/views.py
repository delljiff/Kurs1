import json
import pandas as pd
from typing import List, Dict, Any

from src.utils import read_excel_file
from src.utils import (
  get_greeting,
  get_stock_prices,
  get_currency_rates,
  get_top_five_transactions,
  get_card_info
)


def main_page(transactions, date: str) -> Dict[str, Any]:
    start_date = f'{date[:8]}01{date[10:]}'
    filtered_df = transactions.loc[(transactions['Дата операции'] >= start_date) & (transactions['Дата операции'])]
    data_json = {
      "greeting": get_greeting(),
      "cards": get_card_info(filtered_df),
      "top_transactions": get_top_five_transactions(filtered_df),
      "currency_rates": get_currency_rates("../user_settings.json"),
      "stock_prices": get_stock_prices("../user_settings.json")
    }

    return data_json


if __name__ == "__main__":
    data = read_excel_file("../data/operations.xlsx")
    # Вызываем функцию (передаём пустой список, так как дата пока не используется)
    result = main_page(data, "2020-05-20 12:00:00")

    # Выводим результат
    print(json.dumps(result, ensure_ascii=False, indent=2))
