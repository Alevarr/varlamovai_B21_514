import csv
from profiles import LETTERS

if __name__ == '__main__':
    with open('data.csv', 'r', encoding='utf-8') as csv_file:
        reader = csv.reader(csv_file)
        with open('README.MD', 'w', encoding='utf-8') as file:
            next(reader)
            file.write("# Лабораторная работа №5. Выделение признаков символов.")
            for (i, letter), row in zip(enumerate(LETTERS), reader):
                file.write(
                    f"""
## Буква {letter}

<img src="1.13/inverse_spanish_lowercase_letters/{letter}.png" width="100"> <img src="profiles/x/{letter}.png" width="300"> <img src="profiles/y/{letter}.png" width="300">
"""
                )

                file.write(
                    f"""
Признаки:
- Вес чёрного = {row[1]}
- Нормированный вес чёрного = {row[2]}
- Центр масс = {row[3]}
- Нормированный центр масс = {row[4]}
- Моменты инерции = {row[5]}
- Нормированные моменты инерции = {row[6]}
"""
                )