from connector import get_connection

async def register():
    print("\n===== РЕГИСТРАЦИЯ =====")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    if not username:
        print("Username не может быть пустым")
        return None
    if not password:
        print("Password не может быть пустым")
        return None
    connection = await get_connection()
    try:
        user = await connection.fetchrow("""
            SELECT * FROM users WHERE username = $1
            """,username)
        if user:
            print("Такой пользователь уже существует")
            return None
        new_user = await connection.fetchrow("""
            INSERT INTO users(username, password)
            VALUES($1, $2) RETURNING id, username
            """, username, password)

        print("Регистрация прошла успешно")
        print("Добро пожаловать,", new_user["username"])
        return new_user

    except Exception as error:
        print("Ошибка:", error)
        return None

    finally:
        await connection.close()

async def login():
    print("\n===== ВХОД =====")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    connection = await get_connection()
    try:
        user = await connection.fetchrow("""
            SELECT id, username FROM users
            WHERE username = $1 AND password = $2
            """, username, password)
        if not user:
            print("Неправильный username или password")
            return None
        print("Добро пожаловать,", user["username"])
        return user

    except Exception as error:
        print("Ошибка:", error)
        return None

    finally:
        await connection.close()

async def add_category():
    name = input("Название категории: ").strip()
    if not name:
        print("Название не может быть пустым")
        return
    connection = await get_connection()

    try:
        await connection.execute("""
            INSERT INTO categories(name) VALUES($1)
            """, name)
        print("Категория добавлена")

    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()

async def show_categories():
    connection = await get_connection()
    try:
        categories = await connection.fetch("""
            SELECT * FROM categories
            ORDER BY id """)

        if not categories:
            print("Категорий нет")
            return
        print("\n===== КАТЕГОРИИ =====")
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
    try:
        category_id = int(input("ID категории: "))
    except ValueError:
        print("ID должен быть числом")
        return

    name = input("Новое название: ").strip()

    if not name:
        print("Название не может быть пустым")
        return
    connection = await get_connection()
    try:
        result = await connection.execute("""
            UPDATE categories SET name = $1 WHERE id = $2
            """,name, category_id
        )

        if result == "UPDATE 0":
            print("Категория не найдена")
        else:
            print("Категория изменена")
    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()

async def delete_category():
    await show_categories()
    try:
        category_id = int(input("ID категории: "))
    except ValueError:
        print("ID должен быть числом")
        return

    connection = await get_connection()
    try:
        result = await connection.execute("""
            DELETE FROM categories WHERE id = $1 
            """, category_id
        )
        if result == "DELETE 0":
            print("Категория не найдена")
        else:
            print("Категория удалена")

    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()


async def add_dish():
    name = input("Название блюда: ").strip()
    if not name:
        print("Название не может быть пустым")
        return
    try:
        price = float(input("Цена блюда: "))
    except ValueError:
        print("Цена должна быть числом")
        return
    await show_categories()
    try:
        category_id = int(input("ID категории: "))
    except ValueError:
        print("ID должен быть числом")
        return

    connection = await get_connection()
    try:
        category = await connection.fetchrow("""
            SELECT * FROM categories WHERE id = $1
            """, category_id
        )

        if not category:
            print("Такой категории нет")
            return

        await connection.execute("""
            INSERT INTO dishes(name, price, category_id)
            VALUES($1, $2, $3)
            """, name, price, category_id
        )
        print("Блюдо добавлено")

    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()

async def show_dishes():
    connection = await get_connection()
    try:
        dishes = await connection.fetch("""
            SELECT dishes.id, dishes.name, dishes.price, categories.name AS category
            FROM dishes LEFT JOIN categories
            ON dishes.category_id = categories.id
            ORDER BY dishes.id
            """)

        if not dishes:
            print("Блюд нет")
            return

        print("\n===== БЛЮДА =====")
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

    try:
        dish_id = int(input("ID блюда: "))
    except ValueError:
        print("ID должен быть числом")
        return

    name = input("Новое название: ").strip()
    try:
        price = float(input("Новая цена: "))
    except ValueError:
        print("Цена должна быть числом")
        return
    await show_categories()

    try:
        category_id = int(input("ID категории: "))
    except ValueError:
        print("ID должен быть числом")
        return

    connection = await get_connection()
    try:
        category = await connection.fetchrow("""
            SELECT * FROM categories
            WHERE id = $1
            """, category_id
        )
        if not category:
            print("Категория не найдена")
            return

        result = await connection.execute("""
            UPDATE dishes SET name = $1,
            price = $2, category_id = $3
            WHERE id = $4
            """, name, price, category_id, dish_id
        )
        if result == "UPDATE 0":
            print("Блюдо не найдено")
        else:
            print("Блюдо изменено")

    except Exception as error:
        print("Ошибка:", error)
        
    finally:
        await connection.close()

async def delete_dish():
    await show_dishes()
    try:
        dish_id = int(input("ID блюда: "))
    except ValueError:
        print("ID должен быть числом")
        return

    connection = await get_connection()
    try:
        result = await connection.execute("""
            DELETE FROM dishes WHERE id = $1
            """, dish_id
        )

        if result == "DELETE 0":
            print("Блюдо не найдено")
        else:
            print("Блюдо удалено")

    except Exception as error:
        print("Ошибка:", error)
    finally:
        await connection.close()

async def create_order(user):
    await show_dishes()
    try:
        dish_id = int(input("ID блюда: "))
        quantity = int(input("Количество: "))
    except ValueError:
        print("Введите число")
        return
    if quantity <= 0:
        print("Количество должно быть больше 0")
        return

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

        total_price = float(dish["price"]) * quantity

        await connection.execute(
            """
            INSERT INTO orders(
                customer_name,
                dish_id,
                quantity,
                total_price,
                user_id
            )
            VALUES($1, $2, $3, $4, $5)
            """,
            user["username"],
            dish_id,
            quantity,
            total_price,
            user["id"]
        )

        print("Заказ успешно создан")
        print("Блюдо:", dish["name"])
        print("Количество:", quantity)
        print("Итого:", total_price, "сомони")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def show_orders(user):
    connection = await get_connection()

    try:
        orders = await connection.fetch(
            """
            SELECT
                orders.id,
                dishes.name AS dish,
                orders.quantity,
                orders.total_price,
                orders.created_at

            FROM orders

            LEFT JOIN dishes
            ON orders.dish_id = dishes.id

            WHERE orders.user_id = $1

            ORDER BY orders.id
            """,
            user["id"]
        )

        if not orders:
            print("У вас пока нет заказов")
            return

        print("\n===== МОИ ЗАКАЗЫ =====")

        for order in orders:
            print(
                "ID:", order["id"],
                "| Блюдо:", order["dish"],
                "| Количество:", order["quantity"],
                "| Цена:", order["total_price"],
                "| Дата:", order["created_at"]
            )

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def update_order(user):
    await show_orders(user)

    try:
        order_id = int(input("ID заказа: "))
    except ValueError:
        print("ID должен быть числом")
        return

    await show_dishes()

    try:
        dish_id = int(input("Новый ID блюда: "))
        quantity = int(input("Новое количество: "))
    except ValueError:
        print("Введите число")
        return

    if quantity <= 0:
        print("Количество должно быть больше 0")
        return

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
            print("Блюдо не найдено")
            return

        total_price = float(dish["price"]) * quantity

        result = await connection.execute(
            """
            UPDATE orders
            SET dish_id = $1,
                quantity = $2,
                total_price = $3
            WHERE id = $4
            AND user_id = $5
            """,
            dish_id,
            quantity,
            total_price,
            order_id,
            user["id"]
        )

        if result == "UPDATE 0":
            print("Заказ не найден")
        else:
            print("Заказ изменён")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()


async def delete_order(user):
    await show_orders(user)

    try:
        order_id = int(input("ID заказа: "))
    except ValueError:
        print("ID должен быть числом")
        return

    connection = await get_connection()

    try:
        result = await connection.execute("""
            DELETE FROM orders
            WHERE id = $1
            AND user_id = $2
            """,
            order_id,
            user["id"]
        )

        if result == "DELETE 0":
            print("Заказ не найден")
        else:
            print("Заказ удалён")

    except Exception as error:
        print("Ошибка:", error)

    finally:
        await connection.close()