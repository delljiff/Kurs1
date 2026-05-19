from pathlib import Path
from unittest.mock import Mock, patch

import pandas as pd

from src.utils import (get_card_info, get_currency_rates, get_greeting, get_stock_prices, get_top_five_transactions,
                       read_excel_file)


class TestReadExcelFile:
    """Тесты для read_excel_file"""

    def test_read_excel_file_creates_dataframe(self, tmp_path: Path) -> None:
        """Тест: чтение Excel возвращает DataFrame"""
        # Создаём тестовый Excel файл
        test_df = pd.DataFrame({"A": [1, 2, 3], "B": ["x", "y", "z"]})
        file_path = tmp_path / "test.xlsx"
        test_df.to_excel(file_path, index=False)

        result = read_excel_file(str(file_path))

        assert isinstance(result, pd.DataFrame)
        assert len(result) == 3
        assert list(result.columns) == ["A", "B"]


class TestGetGreeting:
    """Тесты для get_greeting"""

    def test_get_greeting_returns_string(self) -> None:
        """Тест: возвращает строку"""
        result = get_greeting()
        assert isinstance(result, str)
        assert result in ["Доброе утро", "Добрый день", "Добрый вечер", "Доброй ночи"]


class TestGetCardInfo:
    """Тесты для get_card_info"""

    def test_get_card_info_returns_list(self, sample_transactions):
        """Тест: возвращает список"""
        result = get_card_info(sample_transactions)
        assert isinstance(result, list)

    def test_get_card_info_has_required_keys(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: каждый элемент имеет нужные ключи"""
        result = get_card_info(sample_transactions)
        if result:
            for card in result:
                assert "last_digits" in card
                assert "total_spent" in card
                assert "cashback" in card

    def test_get_card_info_ignores_income(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: игнорирует доходы (положительные суммы)"""
        result = get_card_info(sample_transactions)
        # Все суммы должны быть положительными (abs)
        for card in result:
            assert card["total_spent"] >= 0


class TestGetTopFiveTransactions:
    """Тесты для get_top_five_transactions"""

    def test_get_top_five_returns_list(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: возвращает список"""
        result = get_top_five_transactions(sample_transactions)
        assert isinstance(result, list)

    def test_get_top_five_returns_at_most_five(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: возвращает не более 5 транзакций"""
        result = get_top_five_transactions(sample_transactions)
        assert len(result) <= 5

    def test_get_top_five_has_required_keys(self, sample_transactions: pd.DataFrame) -> None:
        """Тест: каждая транзакция имеет нужные ключи"""
        result = get_top_five_transactions(sample_transactions)
        for tx in result:
            assert "date" in tx
            assert "amount" in tx
            assert "category" in tx
            assert "description" in tx
            assert tx["amount"] > 0


class TestGetCurrencyRates:
    """Тесты для get_currency_rates"""

    def test_get_currency_rates_returns_list(self, sample_user_settings: str) -> None:
        """Тест: возвращает список"""
        result = get_currency_rates(sample_user_settings)
        assert isinstance(result, list)

    def test_get_currency_rates_contains_rub(self, sample_user_settings: str) -> None:
        """Тест: всегда содержит RUB с курсом 1.0"""
        result = get_currency_rates(sample_user_settings)
        rub_item = next((r for r in result if r.get("currency") == "RUB"), None)
        assert rub_item is not None
        assert rub_item.get("rate") == 1.0

    @patch("src.utils.requests.get")
    def test_get_currency_rates_handles_api_error(self, mock_get: Mock, sample_user_settings: str) -> None:
        """Тест: обработка ошибки API"""
        mock_get.side_effect = Exception("API недоступен")

        result = get_currency_rates(sample_user_settings)

        # Должен быть fallback с ошибками
        assert isinstance(result, list)
        # Проверяем, что есть хотя бы RUB
        assert any(r.get("currency") == "RUB" for r in result)


class TestGetStockPrices:
    """Тесты для get_stock_prices"""

    def test_get_stock_prices_returns_list(self, sample_user_settings: str) -> None:
        """Тест: возвращает список"""
        result = get_stock_prices(sample_user_settings)
        assert isinstance(result, list)

    def test_get_stock_prices_has_required_keys(self, sample_user_settings: str) -> None:
        """Тест: каждый элемент имеет ключи stock и price или error"""
        result = get_stock_prices(sample_user_settings)
        for stock in result:
            assert "stock" in stock
            # Должен быть либо price, либо error
            assert "price" in stock or "error" in stock

    @patch("src.utils.requests.get")
    def test_get_stock_prices_handles_http_error(self, mock_get: Mock, sample_user_settings: str) -> None:
        """Тест: обработка HTTP ошибки"""
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        result = get_stock_prices(sample_user_settings)

        assert isinstance(result, list)
        # Проверяем, что ошибка записана
        for item in result:
            if "error" in item:
                assert "HTTP" in item["error"] or "не найдена" in item["error"]
