from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.db import wm
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
def get_grammar_keyboard(rules: dict) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for rule in rules.keys():
        keyboard.button(text=rule, callback_data=f"rule_{rule}")

    return keyboard


# Функция для формирования клавиатуры категорий
def get_categories_keyboard(categories: List[str]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for category in categories:
        keyboard.button(text=category, callback_data=f"category_{category}")

    keyboard.button(text="Все", callback_data="category_all")
    return keyboard

# Функция для формирования клавиатуры ответов на вопрос
def get_answers_keyboard(answers) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    buttons = [InlineKeyboardButton(text=answer, callback_data=f"answer_{answer}") for answer in answers]
    keyboard.row(*buttons, width=2)

    return keyboard
