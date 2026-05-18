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
    """Анализирует транзакции по картам"""
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
    """Получает курсы валют из API ЦБ РФ"""
    with open(file_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    user_currencies = settings["user_currencies"]
    result = [{"currency": "RUB", "rate": 1.0}]

    try:
        url = "https://www.cbr.ru/scripts/XML_daily.asp"
        response = requests.get(url, timeout=10)
        response.encoding = "windows-1251"

        import xml.etree.ElementTree as ET

        root = ET.fromstring(response.text)

        for valute in root.findall("Valute"):
            char_code = valute.find("CharCode").text
            if char_code in user_currencies and char_code != "RUB":
                value = valute.find("Value").text.replace(",", ".")
                nominal = valute.find("Nominal").text
                rate = float(value) / int(nominal)
                result.append({"currency": char_code, "rate": round(rate, 4)})

    except Exception as e:
        print(f"Ошибка получения курсов: {e}")
        # fallback
        for currency in user_currencies:
            if currency != "RUB" and not any(r["currency"] == currency for r in result):
                result.append({"currency": currency, "rate": None, "error": str(e)})

    return result


def get_stock_prices(file_path: str) -> List[Dict[str, Any]]:
    """Получает текущие цены акций из API Московской биржи"""
    with open(file_path, "r", encoding="utf-8") as file:
        settings = json.load(file)

    user_stocks = settings.get("user_stocks", [])
    result = []

    for stock in user_stocks:
        try:
            # MOEX API
            url = f"https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{stock}.json"
            response = requests.get(url, timeout=10)

            if response.status_code == 200:
                data = response.json()
                marketdata = data.get("marketdata", {}).get("data", [])
                if marketdata and len(marketdata[0]) > 12:
                    price = marketdata[0][12]
                    if price is not None:
                        result.append({"stock": stock, "price": round(float(price), 2)})
                    else:
                        result.append({"stock": stock, "price": None, "error": "Цена не найдена"})
                else:
                    result.append({"stock": stock, "price": None, "error": "Нет данных"})
            else:
                result.append({"stock": stock, "price": None, "error": f"HTTP {response.status_code}"})

        except Exception as e:
            result.append({"stock": stock, "price": None, "error": str(e)})

    return result
