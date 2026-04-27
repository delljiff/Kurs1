import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from src.services import filter_by_month, round_up_to_limit, calculate_saved, investment_bank


class TestInvestmentBank:

    def test_filter_by_month(self) -> None:
        transactions = [
            {"Дата операции": "2025-03-15 10:00:00", "Сумма операции": 100},
            {"Дата операции": "2025-02-28 10:00:00", "Сумма операции": 200},
            {"Дата операции": "31.12.2021 16:44:00", "Сумма операции": 300},
        ]

        result = filter_by_month(transactions, "2025-03")
        assert len(result) == 1
        assert result[0]["Сумма операции"] == 100

        result = filter_by_month(transactions, "2021-12")
        assert len(result) == 1
        assert result[0]["Сумма операции"] == 300

    def test_round_up_to_limit(self) -> None:
        assert round_up_to_limit(1712, 50) == 1750
        assert round_up_to_limit(340, 50) == 350
        assert round_up_to_limit(200, 50) == 200
        assert round_up_to_limit(-1712, 50) == 1750

    def test_calculate_saved(self) -> None:
        assert calculate_saved(1712, 50) == 38
        assert calculate_saved(340, 50) == 10
        assert calculate_saved(200, 50) == 0
        assert calculate_saved(-1712, 50) == 38

    def test_investment_bank(self) -> None:
        transactions = [
            {"Дата операции": "2025-03-15", "Сумма операции": 1712},
            {"Дата операции": "2025-03-20", "Сумма операции": 340},
            {"Дата операции": "2025-02-28", "Сумма операции": 500},
        ]
        result = investment_bank("2025-03", transactions, 50)
        assert result == 48

    def test_investment_bank_real_date_format(self) -> None:
        transactions = [
            {"Дата операции": "31.12.2021 16:44:00", "Сумма операции": 1712},
            {"Дата операции": "31.12.2021 16:42:04", "Сумма операции": 340},
            {"Дата операции": "30.12.2021 22:22:03", "Сумма операции": 500},
        ]
        result = investment_bank("2021-12", transactions, 50)
        assert result == 48

    def test_empty_transactions(self) -> None:
        result = investment_bank("2025-03", [], 50)
        assert result == 0
