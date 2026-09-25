import asyncio
from connector import create_tables
from services import (register,login, add_category, show_categories, update_category,delete_category,
    add_dish, show_dishes, update_dish, delete_dish,
    create_order,show_orders,update_order,delete_order
)

async def category_menu():
    while True:
        print("""
===== CATEGORY =====

1. Добавить категорию
2. Показать категории
3. Изменить категорию
4. Удалить категорию
0. Назад
""")
        choice = input(
            "Выберите: "
        )
        if choice == "1":
            await add_category()
        elif choice == "2":
            await show_categories()
        elif choice == "3":
            await update_category()
        elif choice == "4":
            await delete_category()
        elif choice == "0":
            break
        else:
            print("Неправильный выбор")

async def dish_menu():
    while True:
        print("""
===== DISHES =====

1. Добавить блюдо
2. Показать блюда
3. Изменить блюдо
4. Удалить блюдо
0. Назад
""")
        choice = input(
            "Выберите: "
        )
        if choice == "1":
            await add_dish()
        elif choice == "2":
            await show_dishes()
        elif choice == "3":
            await update_dish()
        elif choice == "4":
            await delete_dish()
        elif choice == "0":
            break
        else:
            print("Неправильный выбор")

async def order_menu(user):
    while True:
        print("""
===== ORDERS =====

1. Сделать заказ
2. Показать мои заказы
3. Изменить заказ
4. Удалить заказ
0. Назад
""")
        choice = input(
            "Выберите: "
        )
        if choice == "1":
            await create_order(user)
        elif choice == "2":
            await show_orders(user)
        elif choice == "3":
            await update_order(user)
        elif choice == "4":
            await delete_order(user)
        elif choice == "0":
            break
        else:
            print("Неправильный выбор")

async def main_menu(user):
    while True:

        print(f"""
============================
          MENU
============================

Пользователь: {user['username']}

1. Categories
2. Dishes
3. Orders
4. Logout

============================
""")

        choice = input(
            "Выберите: "
        )
        if choice == "1":
            await category_menu()
        elif choice == "2":
            await dish_menu()
        elif choice == "3":
            await order_menu(user)
        elif choice == "4":
            print("Вы вышли из аккаунта")
            break
        else:
            print("Неправильный выбор")

async def main():
    await create_tables()
    while True:
        print("""
============================
      MENU PROJECT
============================

1. Регистрация
2. Войти
0. Выход

============================
""")
        choice = input(
            "Выберите: "
        )
        if choice == "1":
            user = await register()
            if user:
                await main_menu(user)
        elif choice == "2":
            user = await login()
            if user:
                await main_menu(user)
        elif choice == "0":
            print("Программа завершена")
            break
        else:
            print("Неправильный выбор")

asyncio.run(main())