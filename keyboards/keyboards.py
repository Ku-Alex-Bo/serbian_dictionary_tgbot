from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import wm, gm
from typing import List

# Главная клавиатура
button_1 = KeyboardButton(text='Граматика')
button_2 = KeyboardButton(text='Начать тестирование')
button_3 = KeyboardButton(text='Выбрать язык слов')

main_kb = ReplyKeyboardMarkup(
    keyboard= [
        [button_1],
        [button_2],
        [button_3],
    ],
    resize_keyboard=True
)

# Клавиатура выбора языка
pick_language_kb = InlineKeyboardMarkup(inline_keyboard=
    [
        [InlineKeyboardButton(text="Сербский", callback_data="language_serbian")],
        [InlineKeyboardButton(text="Русский", callback_data="language_russian")],
    ]
)

# Функция для формирования клавиатуры выбора граматики
def get_grammar_keyboard(rules: tuple) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for rule in rules:
        keyboard.button(text=rule, callback_data=f"rule_{rule}")
    return keyboard

#Функция для получения категорий слов с пагинацией
def get_categories_keyboard(categories: List[str], page: int = 1) -> InlineKeyboardBuilder:
    MAX_BUTTONS_PER_PAGE = 8
    BUTTONS_PER_ROW = 2

    start_index = (page - 1) * MAX_BUTTONS_PER_PAGE
    end_index = start_index + MAX_BUTTONS_PER_PAGE
    page_categories = categories[start_index:end_index]

    keyboard = InlineKeyboardBuilder()

    # Создаем кнопки для категорий
    for i in range(0, len(page_categories), BUTTONS_PER_ROW):
        row_buttons = [
            InlineKeyboardButton(text=category, callback_data=f"category_{category}")
            for category in page_categories[i:i + BUTTONS_PER_ROW]
        ]
        keyboard.row(*row_buttons)

    # Добавляем кнопку "Все" только в том случае, если это последняя страница
    if page * MAX_BUTTONS_PER_PAGE >= len(categories):
        keyboard.add(InlineKeyboardButton(text="Все", callback_data="category_all"))

    # Пагинация
    total_pages = (len(categories) + MAX_BUTTONS_PER_PAGE - 1) // MAX_BUTTONS_PER_PAGE
    if total_pages > 1:
        pagination_buttons = []
        if page > 1:
            pagination_buttons.append(
                InlineKeyboardButton(text="⬅️ Назад", callback_data=f"page_{page - 1}")
            )
        if page < total_pages:
            pagination_buttons.append(
                InlineKeyboardButton(text="Вперед ➡️", callback_data=f"page_{page + 1}")
            )
        keyboard.row(*pagination_buttons)

    return keyboard


# Функция для формирования клавиатуры ответов на вопрос
def get_answers_keyboard(answers) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=answer, callback_data=f"answer_{answer}") for answer in answers]
    keyboard.row(*buttons, width=2)

    return keyboard
