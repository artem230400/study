import json
from collections import defaultdict


def analyze_orders(file_path):
    try:
        with open(file_path, "r") as file:
            orders = json.load(file)
    except FileNotFoundError:
        print(f"Ошибка: Файл '{file_path}' не найден.")
        return
    except json.JSONDecodeError:
        print("Ошибка: Файл содержит некорректные JSON-данные.")
        return

    if not isinstance(orders, dict):
        print("Ошибка: Данные в файле не являются словарём.")
        return

    max_price = 0
    max_price_order = None
    max_quantity = 0
    max_quantity_order = None
    orders_per_day = defaultdict(int)
    orders_per_user = defaultdict(int)
    total_price_per_user = defaultdict(float)
    total_orders_price = 0
    total_orders_count = len(orders)

    for order_num, order_data in orders.items():
        try:
            price = float(order_data.get('price', 0))
            quantity = int(order_data.get('quantity', 0))
            date = order_data.get('date', '')
            user_id = order_data.get('user_id', '')

            if price > max_price:
                max_price = price
                max_price_order = order_num

            if quantity > max_quantity:
                max_quantity = quantity
                max_quantity_order = order_num

            if date:
                orders_per_day[date] += 1

            if user_id:
                orders_per_user[user_id] += 1

            if user_id:
                total_price_per_user[user_id] += price

            total_orders_price += price

        except (ValueError, TypeError) as e:
            print(f"Ошибка при обработке заказа {order_num}: {e}")
            continue

    if not orders:
        print("Нет данных о заказах.")
        return

    busiest_day = max(orders_per_day, key=orders_per_day.get) if orders_per_day else "Нет данных"

    most_active_user = max(orders_per_user, key=orders_per_user.get) if orders_per_user else "Нет данных"

    biggest_spender = max(total_price_per_user, key=total_price_per_user.get) if total_price_per_user else "Нет данных"

    average_order_price = total_orders_price / total_orders_count if total_orders_count else 0

    print("\nРезультаты анализа заказов:")
    print("=" * 40)
    print(f"1. Номер самого дорогого заказа: {max_price_order or 'Нет данных'} (Стоимость: {max_price:.2f})")
    print(
        f"2. Номер заказа с самым большим количеством товаров: {max_quantity_order or 'Нет данных'} (Количество: {max_quantity})")
    print(
        f"3. День с наибольшим количеством заказов: {busiest_day} (Количество заказов: {orders_per_day.get(busiest_day, 0)})")
    print(
        f"4. Пользователь с наибольшим количеством заказов: {most_active_user} (Количество заказов: {orders_per_user.get(most_active_user, 0)})")
    print(
        f"5. Пользователь с самой большой суммарной стоимостью заказов: {biggest_spender} (Сумма: {total_price_per_user.get(biggest_spender, 0):.2f})")
    print(f"6. Средняя стоимость заказа: {average_order_price:.2f}")
    print("=" * 40)

analyze_orders("orders.json")