from fridge import add, add_by_note, find, amount, expire


def main():
    while True:
        print("\n=== Холодильник ===")
        print("1. Добавить продукт вручную")
        print("2. Добавить продукт по заметке")
        print("3. Найти продукт по названию")
        print("4. Узнать количество продукта")
        print("5. Показать просроченные продукты")
        print("0. Выйти")

        choice = input("\nВыберите действие (0-5): ").strip()

        if choice == "1":
            name = input("Название продукта: ")
            amount_val = input("Количество: ")
            exp_date = input("Срок годности (ГГГГ-ММ-ДД) или оставьте пустым: ") or None
            add(name, float(amount_val), exp_date)
            print("Продукт добавлен!")

        elif choice == "2":
            note = input("Введите заметку (пример: 2 молоко 2024-06-10): ")
            add_by_note(note)
            print("Продукт добавлен")

        elif choice == "3":
            query = input("Что найти? ")
            results = find(query)
            if results:
                print("Найдено:", ", ".join(results))
            else:
                print("Ничего не найдено")

        elif choice == "4":
            name = input("Название продукта: ")
            total = amount(name)
            print(f"Всего {name}: {total}")

        elif choice == "5":
            expired = expire()
            if expired:
                print("Просрочено:", ", ".join(expired))
            else:
                print("Нет просроченных продуктов")

        elif choice == "0":
            print("Пока")
            break

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
