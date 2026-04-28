import sys
from pathlib import Path
from typing import Any

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from src.reports import spending_by_category
from src.services import load_transactions_from_excel


class TestReports:
    import sys
    from pathlib import Path
    from typing import Any

    import pandas as pd
    import pytest

    sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

    from reports import spending_by_category
    from services import load_transactions_from_excel

    class TestReports:
        @pytest.fixture
        def df(self) -> pd.DataFrame:
            """Загружает реальные транзакции из Excel и возвращает DataFrame"""
            transactions: list[dict[str, Any]] = load_transactions_from_excel("data/operations.xlsx")
            return pd.DataFrame(transactions)

        def test_spending_by_category_returns_df(self, df: pd.DataFrame) -> None:
            """Проверяет, что функция возвращает DataFrame"""
            result: pd.DataFrame = spending_by_category(df, "Супермаркеты")
            assert isinstance(result, pd.DataFrame)

        def test_spending_by_category_filters_correct_category(self, df: pd.DataFrame) -> None:
            """Проверяет, что возвращаются только транзакции с нужной категорией"""
            result: pd.DataFrame = spending_by_category(df, "Супермаркеты")
            assert all(result["Категория"] == "Супермаркеты")

        def test_spending_by_category_respects_date(self, df: pd.DataFrame) -> None:
            """Проверяет, что дата ограничивает период"""
            result: pd.DataFrame = spending_by_category(df, "Супермаркеты", "31.12.2021")
            dates: pd.Series = pd.to_datetime(result["Дата операции"], dayfirst=True, errors="coerce")
            assert (dates >= pd.Timestamp("2021-10-01")).all()
            assert (dates <= pd.Timestamp("2021-12-31")).all()

        def test_spending_by_category_empty_for_unknown_category(self, df: pd.DataFrame) -> None:
            """Если категории нет — возвращается пустой DataFrame"""
            result: pd.DataFrame = spending_by_category(df, "ЭТОЙ_КАТЕГОРИИ_НЕТ")
            assert len(result) == 0

        def test_spending_by_category_works_without_date(self, df: pd.DataFrame) -> None:
            """Без передачи даты — не падает"""
            result: pd.DataFrame = spending_by_category(df, "Супермаркеты")
            assert isinstance(result, pd.DataFrame)
