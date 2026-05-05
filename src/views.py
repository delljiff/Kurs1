import json
from typing import List, Dict, Any
from src.utils import (
  get_greeting,
  get_stock_prices,
  get_currency_rates,
  get_top_five_transactions,
  get_card_info
)


def main_page(transactions: List[Dict[str, Any]], date: str) -> None:
    data_json = {}
    data_json["greeting"] = get_greeting()
    data_json["cards"] = get_card_info()
    data_json["top_transactions"] = get_top_five_transactions()
    data_json["currency_rates"] = get_currency_rates()
    data_json["stock_prices"] = get_stock_prices()
