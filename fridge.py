import datetime
from decimal import Decimal


def add(items, title, amount, expiration_date=None):
    """
    Добавляет продукт в словарь items.
    :param items: Словарь с продуктами.
    :param title: Название продукта.
    :param amount: Количество продукта (Decimal).
    :param expiration_date: Срок годности (строка в формате 'ГГГГ-ММ-ДД' или None).
    """
    if title not in items:
        items[title] = []

    exp_date = None
    if expiration_date is not None:
        exp_date = datetime.datetime.strptime(expiration_date, '%Y-%m-%d').date()

    new_batch = {
        'amount': amount,
        'expiration_date': exp_date
    }

    items[title].append(new_batch)


def add_by_note(items, note):
    """
    Добавляет продукт в словарь items, распарсив строку note.
    :param items: Словарь с продуктами.
    :param note: Строка в формате "<название> <количество> [<срок годности>]".
    """
    parts = note.split()

    if len(parts) >= 3 and parts[-1].count('-') >= 2:
        expiration_date = parts[-1]
        amount_str = parts[-2]
        title = ' '.join(parts[:-2])
    else:
        expiration_date = None
        amount_str = parts[-1]
        title = ' '.join(parts[:-1])

    amount = Decimal(amount_str)
    add(items, title, amount, expiration_date)


def find(items, needle):
    """
    Ищет продукты, в названии которых содержится строка needle (без учета регистра).
    :param items: Словарь с продуктами.
    :param needle: Искомая подстрока.
    :return: Список названий продуктов.
    """
    result = []
    needle_lower = needle.lower()

    for title in items.keys():
        if needle_lower in title.lower():
            result.append(title)

    return result


def amount(items, needle):
    """
    Возвращает общее количество продуктов, название которых содержит needle (без учета регистра).
    :param items: Словарь с продуктами.
    :param needle: Искомая подстрока.
    :return: Общее количество (Decimal).
    """
    total_amount = Decimal('0')
    needle_lower = needle.lower()

    for title, batches in items.items():
        if needle_lower in title.lower():
            for batch in batches:
                total_amount += batch['amount']

    return total_amount


def expire(items, in_advance_days=0):
    """
    Возвращает список просроченных продуктов или продуктов, которые испортятся в ближайшие in_advance_days дней.
    :param items: Словарь с продуктами.
    :param in_advance_days: Количество дней вперед для проверки срока годности.
    :return: Список кортежей вида (название_продукта, общее_количество).
    """
    result = []
    today = datetime.date.today()
    deadline = today + datetime.timedelta(days=in_advance_days)

    for title, batches in items.items():
        total_expired_amount = Decimal('0')

        for batch in batches:
            exp_date = batch['expiration_date']
            if exp_date is not None and exp_date <= deadline:
                total_expired_amount += batch['amount']

        if total_expired_amount > 0:
            result.append((title, total_expired_amount))

    return result


# ==========================
# ОСНОВНАЯ ПРОГРАММА (ДЕМОНСТРАЦИЯ РАБОТЫ)
# ==========================

if __name__ == "__main__":
    # Создаем пустой холодильник
    goods = {}

    print("1️⃣  Создаем холодильник и добавляем продукты через add()...")
    add(goods, 'Яйца', Decimal('10'), '2024-06-01')
    add(goods, 'Яйца', Decimal('3'), '2024-06-15')
    add(goods, 'Вода', Decimal('2.5'))
    print("✅ Добавлено: Яйца (10 шт, 3 шт), Вода (2.5 кг)\n")

    print("2️⃣  Добавляем продукты через add_by_note()...")
    add_by_note(goods, 'Молоко 1.5 2024-05-25')
    add_by_note(goods, 'Сыр моцарелла 0.3')
    print("✅ Добавлено: Молоко (1.5 кг), Сыр моцарелла (0.3 кг)\n")

    print("3️⃣  Текущее содержимое холодильника:")
    for product, batches in goods.items():
        print(f"  {product}:")
        for i, batch in enumerate(batches, 1):
            exp = batch['expiration_date'] or "Бессрочно"
            print(f"    Партия {i}: {batch['amount']} кг/шт, срок: {exp}")
    print()

    print("4️⃣  Поиск продуктов по слову 'яйц':")
    found = find(goods, 'яйц')
    print("   Найдено:", found)
    print()

    print("5️⃣  Общее количество по запросу 'яйца':")
    total = amount(goods, 'яйца')
    print(f"   Всего: {total} шт/кг")
    print()

    print("6️⃣  Проверка просроченных продуктов (на сегодня):")
    expired = expire(goods, 0)
    if expired:
        for product, qty in expired:
            print(f"   ❗ {product}: {qty} шт/кг")
    else:
        print("   ✅ Ничего не испортилось!")
    print()

    print("7️⃣  Что испортится в ближайшие 10 дней:")
    expiring = expire(goods, 10)
    if expiring:
        for product, qty in expiring:
            print(f"   ⚠️  {product}: {qty} шт/кг")
    else:
        print("   ✅ Ничего не испортится в ближайшие 10 дней.")
    print()

