import pandas as pd

from src.reports import spending_by_category


def test_spending_by_category_with_date(sample_transactions: pd.DataFrame) -> None:
    """Тест: фильтрация по категории с указанной датой"""
    result = spending_by_category(sample_transactions, "Супермаркеты", date="31.12.2021")

    assert isinstance(result, pd.DataFrame)
    assert len(result) >= 1
    assert all(result["Категория"] == "Супермаркеты")
    assert all(result["Сумма операции"] < 0)


def test_spending_by_category_no_date(sample_transactions: pd.DataFrame) -> None:
    """Тест: без указания даты (используется текущая)"""
    # Мокаем или просто проверяем что функция работает
    result = spending_by_category(sample_transactions, "Супермаркеты")
    assert isinstance(result, pd.DataFrame)


def test_spending_by_category_empty_result(sample_transactions: pd.DataFrame) -> None:
    """Тест: категория, которой нет в данных"""
    result = spending_by_category(sample_transactions, "Несуществующая категория", date="31.12.2021")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0


def test_spending_by_category_wrong_date(sample_transactions: pd.DataFrame) -> None:
    """Тест: дата вне диапазона данных"""
    result = spending_by_category(sample_transactions, "Супермаркеты", date="01.01.2020")
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 0
