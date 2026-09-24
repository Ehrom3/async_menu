from connector import get_connection

async def add_category():
    name = input("Название категории: ")
    connection = await get_connection()
    try:
        await connection.execute(
            """
            INSERT INTO categories(name)
            VALUES($1)
            """,
            name
        )
        print("Категория добавлена")
    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()


async def show_categories():
    connection = await get_connection()

    try:
        categories = await connection.fetch(
            """
            SELECT *
            FROM categories
            ORDER BY id
            """
        )

        if not categories:
            print("Категорий нет")
            return

        print("\n--- Категории ---")

        for category in categories:
            print(
                category["id"],
                category["name"]
            )

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def update_category():
    await show_categories()

    category_id = int(
        input("ID категории: ")
    )

    name = input(
        "Новое название: "
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            UPDATE categories
            SET name = $1
            WHERE id = $2
            """,
            name,
            category_id
        )

        print("Категория изменена")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def delete_category():
    await show_categories()

    category_id = int(
        input("ID категории: ")
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            DELETE FROM categories
            WHERE id = $1
            """,
            category_id
        )

        print("Категория удалена")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()

async def add_dish():
    name = input(
        "Название блюда: "
    )

    price = float(
        input("Цена блюда: ")
    )

    await show_categories()

    category_id = int(
        input("ID категории: ")
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            INSERT INTO dishes(
                name,
                price,
                category_id
            )
            VALUES($1, $2, $3)
            """,
            name,
            price,
            category_id
        )

        print("Блюдо добавлено")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def show_dishes():
    connection = await get_connection()

    try:
        dishes = await connection.fetch(
            """
            SELECT
                dishes.id,
                dishes.name,
                dishes.price,
                categories.name AS category
            FROM dishes
            LEFT JOIN categories
            ON dishes.category_id = categories.id
            ORDER BY dishes.id
            """
        )

        if not dishes:
            print("Блюд нет")
            return

        print("\n--- Блюда ---")

        for dish in dishes:
            print(
                "ID:", dish["id"],
                "| Название:", dish["name"],
                "| Цена:", dish["price"],
                "| Категория:", dish["category"]
            )

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def update_dish():
    await show_dishes()

    dish_id = int(
        input("ID блюда: ")
    )

    name = input(
        "Новое название блюда: "
    )

    price = float(
        input("Новая цена: ")
    )
    await show_categories()

    category_id = int(
        input("Новый ID категории: ")
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            UPDATE dishes
            SET
                name = $1,
                price = $2,
                category_id = $3
            WHERE id = $4
            """,
            name,
            price,
            category_id,
            dish_id
        )

        print("Блюдо изменено")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def delete_dish():
    await show_dishes()

    dish_id = int(
        input("ID блюда: ")
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            DELETE FROM dishes
            WHERE id = $1
            """,
            dish_id
        )

        print("Блюдо удалено")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()

async def create_order():
    customer_name = input(
        "Имя клиента: "
    )

    await show_dishes()

    dish_id = int(
        input("ID блюда: ")
    )

    quantity = int(
        input("Количество: ")
    )

    connection = await get_connection()

    try:
        dish = await connection.fetchrow(
            """
            SELECT *
            FROM dishes
            WHERE id = $1
            """,
            dish_id
        )

        if not dish:
            print("Такого блюда нет")
            return

        total_price = (
            dish["price"] * quantity
        )

        await connection.execute(
            """
            INSERT INTO orders(
                customer_name,
                dish_id,
                quantity,
                total_price
            )
            VALUES($1, $2, $3, $4)
            """,
            customer_name,
            dish_id,
            quantity,
            total_price
        )

        print("Заказ создан")
        print("Итоговая цена:", total_price)

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def show_orders():
    connection = await get_connection()

    try:
        orders = await connection.fetch(
            """
            SELECT
                orders.id,
                orders.customer_name,
                dishes.name AS dish,
                orders.quantity,
                orders.total_price,
                orders.created_at
            FROM orders
            LEFT JOIN dishes
            ON orders.dish_id = dishes.id
            ORDER BY orders.id
            """
        )

        if not orders:
            print("Заказов нет")
            return

        print("\n--- Заказы ---")

        for order in orders:
            print(
                "ID:", order["id"],
                "| Клиент:", order["customer_name"],
                "| Блюдо:", order["dish"],
                "| Количество:", order["quantity"],
                "| Цена:", order["total_price"],
                "| Дата:", order["created_at"]
            )

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def update_order():
    await show_orders()

    order_id = int(
        input("ID заказа: ")
    )

    customer_name = input(
        "Новое имя клиента: "
    )

    await show_dishes()

    dish_id = int(
        input("Новый ID блюда: ")
    )

    quantity = int(
        input("Новое количество: ")
    )

    connection = await get_connection()

    try:
        dish = await connection.fetchrow(
            """
            SELECT *
            FROM dishes
            WHERE id = $1
            """,
            dish_id
        )

        if not dish:
            print("Такого блюда нет")
            return

        total_price = (
            dish["price"] * quantity
        )

        await connection.execute("""
            UPDATE orders
            SET
                customer_name = $1,
                dish_id = $2,
                quantity = $3,
                total_price = $4
            WHERE id = $5
            """,
            customer_name,
            dish_id,
            quantity,
            total_price,
            order_id
        )

        print("Заказ изменён")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def delete_order():
    await show_orders()

    order_id = int(
        input("ID заказа: ")
    )

    connection = await get_connection()

    try:
        await connection.execute(
            """
            DELETE FROM orders
            WHERE id = $1
            """,
            order_id
        )

        print("Заказ удалён")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()