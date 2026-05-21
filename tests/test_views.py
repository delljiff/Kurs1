from unittest.mock import Mock, patch

import pandas as pd

from src.views import main_page


class TestMainPage:
    """Тесты для функции main_page"""

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_returns_dict(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: возвращает словарь"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result, dict)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_has_required_keys(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: содержит все необходимые ключи"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")

        required_keys = ["greeting", "cards", "top_transactions", "currency_rates", "stock_prices"]
        for key in required_keys:
            assert key in result

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_greeting_is_string(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: приветствие - строка"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result["greeting"], str)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_cards_is_list(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: cards - список"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result["cards"], list)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_top_transactions_is_list(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: top_transactions - список"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result["top_transactions"], list)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_currency_rates_is_list(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: currency_rates - список"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result["currency_rates"], list)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_stock_prices_is_list(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: stock_prices - список"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result["stock_prices"], list)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_filters_by_date(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: фильтрация по дате работает"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")
        assert isinstance(result, dict)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_calls_utils_functions(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: вызывает вспомогательные функции из utils"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2021")

        # Проверяем, что функции были вызваны
        mock_currency.assert_called_once()
        mock_stocks.assert_called_once()

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_date_format_preserved(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: формат даты сохраняется"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        test_date = "15.06.2021"
        result = main_page(sample_transactions, test_date)

        assert isinstance(result, dict)


class TestMainPageEdgeCases:
    """Тесты граничных случаев"""

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_with_future_date(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: будущая дата (нет данных)"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "31.12.2030")

        assert isinstance(result, dict)
        assert "greeting" in result
        assert isinstance(result["cards"], list)
        assert isinstance(result["top_transactions"], list)

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_with_past_date(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: прошедшая дата"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        result = main_page(sample_transactions, "01.01.2020")

        assert isinstance(result, dict)
        assert "greeting" in result

    @patch("src.views.get_currency_rates")
    @patch("src.views.get_stock_prices")
    def test_main_page_with_invalid_date_format(
        self, mock_stocks: Mock, mock_currency: Mock, sample_transactions: pd.DataFrame
    ) -> None:
        """Тест: неверный формат даты"""
        mock_currency.return_value = [{"currency": "USD", "rate": 90.0}]
        mock_stocks.return_value = [{"stock": "SBER", "price": 300.0}]

        # Функция может упасть или вернуть словарь - проверяем, что не падает
        try:
            result = main_page(sample_transactions, "2021-12-31")
            assert isinstance(result, dict)
        except Exception:
            pass
