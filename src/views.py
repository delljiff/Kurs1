from typing import Any, Dict

from utils import get_card_info, get_currency_rates, get_greeting, get_stock_prices, get_top_five_transactions


def main_page(transactions: pd.DataFrame, date: str) -> Dict[str, Any]:
    start_date = f"{date[:8]}01{date[10:]}"
    end_date = date
    filtered_df = transactions.loc[
        (transactions["Дата операции"] >= start_date) & (transactions["Дата операции"] <= end_date)
    ]
    data_json = {
        "greeting": get_greeting(),
        "cards": get_card_info(filtered_df),
        "top_transactions": get_top_five_transactions(filtered_df),
        "currency_rates": get_currency_rates("user_settings.json"),
        "stock_prices": get_stock_prices("user_settings.json"),
    }

    return data_json
