from datetime import datetime, date
from decimal import Decimal

# словарь продуктов
goods = {}


def add(name: str, amount, expiration_date: str | None = None): # Добавляет продукт в словарь goods.

    name = name.strip()

    # Приводим amount к Decimal (поддерживаем разные входные типы)
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    # Обрабатываем дату
    exp_date = None
    if expiration_date is not None:
        exp_date = datetime.strptime(expiration_date.strip(), "%Y-%m-%d").date()

    # Добавляем партию
    if name not in goods:
        goods[name] = []
    goods[name].append({
        'amount': amount,
        'expiration_date': exp_date
    })


def add_by_note(note: str): # Добавляет продукт по текстовой заметке.

    parts = note.strip().split()
    if len(parts) < 2:
        raise ValueError("Заметка должна содержать хотя бы количество и название")

    amount = Decimal(parts[0])
    name = parts[1].strip()
    expiration_date = parts[2].strip() if len(parts) > 2 else None

    add(name, amount, expiration_date)


def find(query: str) -> list[str]: #  Ищет продукты, в названии которых содержится query.

    query = query.strip()
    result = []
    for name in goods:
        if query in name:
            result.append(name)
    return result


def amount(name: str) -> Decimal: # Возвращает общее количество продукта с указанным названием.

    name = name.strip()
    if name not in goods:
        return Decimal('0')

    total = Decimal('0')
    for batch in goods[name]:
        total += batch['amount']
    return total


def expire() -> list[str]: # Возвращает список названий просроченных продуктов.

    today = date.today()
    expired_products = set()

    for name, batches in goods.items():
        for batch in batches:
            exp_date = batch['expiration_date']
            if exp_date is not None and exp_date < today:
                expired_products.add(name)
                break  # достаточно одной просроченной партии

    return sorted(expired_products)
