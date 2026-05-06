import json
from utils import read_excel_file
from services import best_categories_of_high_cashback
from views import main_page

# Читаем файл
df = read_excel_file('data/operations.xlsx')

# Анализируем декабрь 2021 года
result = best_categories_of_high_cashback(df, '2019', '09')

print(result)

if __name__ == "__main__":
    data = read_excel_file("data/operations.xlsx")
    # Вызываем функцию (передаём пустой список, так как дата пока не используется)
    result = main_page(data, "2020-05-20 12:00:00")

    # Выводим результат
    print(json.dumps(result, ensure_ascii=False, indent=2))