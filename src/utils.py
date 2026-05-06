import datetime
import json
from typing import Any, Dict, List

import pandas as pd
import requests


def read_excel_file(file_path: str) -> pd.DataFrame:
    """
    Читает Excel файл и возвращает таблицу (DataFrame)

    Аргументы:
        file_path: путь к файлу (например: "data.xlsx" или "C:/folder/data.xlsx")

    Возвращает:
        DataFrame - таблицу с данными из файла
    """
    df = pd.read_excel(file_path)
    return df


def get_greeting() -> str:
    """Возвращает приветствие в зависимости от времени суток"""
    current_hour = datetime.datetime.now().hour
    if 5 <= current_hour < 12:
        return "Доброе утро"
    elif 12 <= current_hour < 18:
        return "Добрый день"
    elif 18 <= current_hour < 23:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_info(transactions: pd.DataFrame) -> List[Dict[str, Any]]:
    """
    Анализирует транзакции по картам

    Args:
        file_path: путь к Excel файлу

    Returns:
        List[Dict[str, Any]]: список словарей с ключами:
            - last_digits: последние 4 цифры карты
            - total_spent: общая сумма расходов
            - cashback: сумма кешбэка
    """
    df = transactions[(transactions["Статус"] == "OK") & (transactions["Сумма операции"] < 0)]
    df = df[df["Номер карты"].notna()]
    df["last_digits"] = df["Номер карты"].str.replace("*", "")
    card_totals = df.groupby("last_digits")["Сумма операции"].sum().abs()

    result: List[Dict[str, Any]] = []
    for card, spent in card_totals.items():
        result.append({"last_digits": card, "total_spent": round(spent, 2), "cashback": round(spent / 100, 2)})

    return result


def get_top_five_transactions(transactions) -> List[Dict[str, Any]]:
    """Возвращает топ-5 транзакций по сумме платежа"""

    df = transactions[transactions["Статус"] == "OK"]
    df["abs_sum"] = df["Сумма операции"].abs()
    top_5 = df.sort_values("abs_sum", ascending=False).head(5)

    result = []
    for _, row in top_5.iterrows():
        result.append(
            {
                "date": row["Дата операции"],
                "amount": abs(row["Сумма операции"]),
                "category": row["Категория"],
                "description": row["Описание"],
            }
        )

    return result


def get_currency_rates(file_path: str) -> List[Dict[str, Any]]:
    """Получает курсы валют из файла настроек"""
    with open(file_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    user_currencies = settings["user_currencies"]
    result = []

    for currency in user_currencies:
        if currency == "RUB":
            result.append({"currency": currency, "rate": 1.0})
        else:
            url = f"https://api.exchangerate-api.com/v4/latest/{currency}"
            response = requests.get(url)
            data = response.json()
            rub_rate = data["rates"]["RUB"]
            result.append({"currency": currency, "rate": round(rub_rate, 2)})

    return result


def get_stock_prices(file_path: str) -> List[Dict[str, Any]]:
    """
    Получает текущие цены акций из файла user_settings.json через Alpha Vantage API

    Args:
        file_path: путь к файлу user_settings.json

    Returns:
        List[Dict[str, Any]]: список словарей с ценами акций
    """
    with open(file_path, "r", encoding="utf-8") as file:
        settings = json.load(file)

    user_stocks = settings.get("user_stocks", [])
    result = []

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    for stock in user_stocks:
        try:
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}"
            response = requests.get(url, headers=headers)

            if response.status_code != 200:
                result.append({"stock": stock, "price": None, "error": f"Ошибка HTTP {response.status_code}"})
                continue

            data = response.json()

            if data["chart"]["result"] is None:
                result.append({"stock": stock, "price": None, "error": f"Данные для {stock} не найдены"})
                continue

            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            result.append({"stock": stock, "price": round(price, 2)})

        except Exception as e:
            result.append({"stock": stock, "price": None, "error": f"Ошибка: {str(e)}"})

    return result
