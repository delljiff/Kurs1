import logging
import pandas as pd
from src.services import best_categories_of_high_cashback
from src.reports import spending_by_category
from src.views import main_page

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('coursework.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def load_data(file_path: str) -> pd.DataFrame:
    """Загрузка данных из Excel файла"""
    logger.info(f"Загрузка данных из файла: {file_path}")
    try:
        df = pd.read_excel(file_path)
        logger.info(f"Данные загружены. Строк: {len(df)}, колонок: {len(df.columns)}")
        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        raise


def main():
    """Главная функция программы"""
    logger.info("=" * 50)
    logger.info("ЗАПУСК ПРОГРАММЫ")
    logger.info("=" * 50)

    try:
        # 1. Загружаем данные
        df = load_data("../data/operations.xlsx")

        # 2. Пример вызова функции из services
        logger.info("Вызов services.best_categories_of_high_cashback")
        cashback_result = best_categories_of_high_cashback(df, "2020", "12")
        print(cashback_result)
        logger.info(f"Результат: {cashback_result}")


        # 3. Пример вызова функции из reports
        logger.info("Вызов reports.spending_by_category")
        report_result = spending_by_category(df, "Супермаркеты", date="31.12.2021")
        print(report_result)
        logger.info(f"Найдено трат: {len(report_result)}")

        # 4. Пример вызова функции из views
        logger.info("Вызов views.main_page")
        page_data = main_page(df, "31.12.2021")
        print("DEBUG", page_data)
        logger.info(f"Сформирована главная страница: {list(page_data.keys())}")

        logger.info("=" * 50)
        logger.info("ПРОГРАММА УСПЕШНО ЗАВЕРШЕНА")
        logger.info("=" * 50)

    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())