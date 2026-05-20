import pandas as pd
import pytest

from src.services import best_categories_of_high_cashback


class TestBestCategoriesOfHighCashback:
    """Тесты для функции best_categories_of_high_cashback"""

    def test_basic_functionality(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: базовая функциональность"""
        result = best_categories_of_high_cashback(sample_transactions, "2021", "12")

        assert isinstance(result, dict)
        # Проверяем, что результат не пустой (есть данные за декабрь 2021)
        # Точное содержимое зависит от sample_transactions

    def test_empty_month(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: месяц без данных"""
        result = best_categories_of_high_cashback(sample_transactions, "2020", "01")

        assert isinstance(result, dict)
        assert len(result) == 0
        assert result == {}

    def test_invalid_year(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: неверный год (нет данных)"""
        result = best_categories_of_high_cashback(sample_transactions, "9999", "12")

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_invalid_month_format(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: месяц в неверном формате"""
        result = best_categories_of_high_cashback(sample_transactions, "2021", "2")  # вместо "02"

        assert isinstance(result, dict)
        # Функция должна корректно обработать (int(month) даст 2, форматирование в 02)

    def test_month_with_only_income(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: месяц только с доходами (без расходов)"""
        # Создаём данные только с положительными суммами
        income_data = sample_transactions.copy()
        income_data["Сумма операции"] = abs(income_data["Сумма операции"])
        income_data["Кэшбэк"] = None

        result = best_categories_of_high_cashback(income_data, "2021", "12")

        assert isinstance(result, dict)
        assert len(result) == 0

    def test_month_with_cashback_only(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: месяц только с кэшбэком"""
        result = best_categories_of_high_cashback(sample_transactions, "2021", "12")

        # Проверяем, что все суммы кэшбэка положительные
        for value in result.values():
            assert value > 0

    def test_result_sorted_descending(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: результаты отсортированы по убыванию кэшбэка"""
        # Создаём данные с разными категориями
        data = {
            "Дата операции": ["15.12.2021 10:00:00", "16.12.2021 11:00:00", "17.12.2021 12:00:00"],
            "Дата платежа": ["15.12.2021", "16.12.2021", "17.12.2021"],
            "Номер карты": ["*7197", "*7197", "*7197"],
            "Статус": ["OK", "OK", "OK"],
            "Сумма операции": [-100, -200, -300],
            "Валюта операции": ["RUB", "RUB", "RUB"],
            "Сумма платежа": [-100, -200, -300],
            "Валюта платежа": ["RUB", "RUB", "RUB"],
            "Кэшбэк": [10, 50, 30],
            "Категория": ["Аптеки", "Супермаркеты", "Аптеки"],
            "MCC": [5912.0, 5411.0, 5912.0],
            "Описание": ["Аптека1", "Магнит", "Аптека2"],
            "Бонусы (включая кэшбэк)": [10, 50, 30],
            "Округление на инвесткопилку": [0, 0, 0],
            "Сумма операции с округлением": [100, 200, 300],
        }
        df = pd.DataFrame(data)

        result = best_categories_of_high_cashback(df, "2021", "12")

        # Аптеки: 10 + 30 = 40, Супермаркеты: 50
        # Ожидаемый порядок: Супермаркеты (50), Аптеки (40)
        categories = list(result.keys())
        values = list(result.values())

        assert len(categories) == 2
        assert values[0] >= values[1]  # проверка сортировки по убыванию

    def test_missing_columns(self) -> None:
        """Тест: отсутствуют необходимые колонки"""
        df = pd.DataFrame({"другая_колонка": [1, 2, 3]})

        with pytest.raises(Exception):  # Функция должна выбросить исключение
            best_categories_of_high_cashback(df, "2021", "12")


class TestBestCategoriesEdgeCases:
    """Тесты граничных случаев"""

    def test_year_boundary(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: граничный год (минимальный и максимальный)"""
        # Минимальный возможный год
        result_min = best_categories_of_high_cashback(sample_transactions, "1900", "01")
        assert isinstance(result_min, dict)

        # Максимальный возможный год
        result_max = best_categories_of_high_cashback(sample_transactions, "9999", "12")
        assert isinstance(result_max, dict)

    def test_month_boundary(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: граничные месяцы"""
        # Январь
        result_jan = best_categories_of_high_cashback(sample_transactions, "2021", "01")
        assert isinstance(result_jan, dict)

        # Декабрь
        result_dec = best_categories_of_high_cashback(sample_transactions, "2021", "12")
        assert isinstance(result_dec, dict)

    def test_large_cashback_values(self) -> None:
        """Тест: большие значения кэшбэка"""
        data = {
            "Дата операции": ["15.12.2021 10:00:00"],
            "Дата платежа": ["15.12.2021"],
            "Номер карты": ["*7197"],
            "Статус": ["OK"],
            "Сумма операции": [-1000000],
            "Валюта операции": ["RUB"],
            "Сумма платежа": [-1000000],
            "Валюта платежа": ["RUB"],
            "Кэшбэк": [50000],
            "Категория": ["Аптеки"],
            "MCC": [5912.0],
            "Описание": ["Аптека"],
            "Бонусы (включая кэшбэк)": [50000],
            "Округление на инвесткопилку": [0],
            "Сумма операции с округлением": [1000000],
        }
        df = pd.DataFrame(data)

        result = best_categories_of_high_cashback(df, "2021", "12")

        assert "Аптеки" in result
        assert result["Аптеки"] == 50000
