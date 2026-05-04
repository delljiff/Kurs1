import datetime
import pandas as pd
from typing import List, Dict, Any


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


# def get_greeting() -> str:
#     """Возвращает приветствие в зависимости от времени суток"""
#     current_hour = datetime.datetime.now().hour
#     if 5 <= current_hour < 12:
#         return "Доброе утро"
#     elif 12 <= current_hour < 18:
#         return "Добрый день"
#     elif 18 <= current_hour < 23:
#         return "Добрый вечер"
#     else:
#         return "Доброй ночи"


def get_card_info(file_path: str) -> List[Dict[str, Any]]:
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
    df = read_excel_file(file_path)
    df = df[(df["Статус"] == "OK") & (df["Сумма операции"] < 0)]
    df = df[df['Номер карты'].notna()]
    df['last_digits'] = df['Номер карты'].str.replace('*', '')
    card_totals = df.groupby('last_digits')['Сумма операции'].sum().abs()

    result: List[Dict[str, Any]] = []
    for card, spent in card_totals.items():
        result.append({
            "last_digits": card,
            "total_spent": round(spent, 2),
            "cashback": round(spent / 100, 2)
        })

    return result

