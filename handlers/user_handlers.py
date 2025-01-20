from aiogram import Router, F
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from lexicon.lexicon_ru import LEXICON_RU
from lexicon import tables as t
from database.db import um, wm, gm
from states.states import MainStates
from keyboards import keyboards as kb
from services import services as f
import config as conf
import random
import os

# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    user_id = message.from_user.id
    if um.get_user_by_tg_id(user_id) is None:
        um.insert_user(user_id, message.from_user.username)
    await state.clear()
    await state.update_data(  # Инициализируем данные пользователя
        language=um.get_user_by_tg_id(user_id)["language"],
        score={"correct": 0, "wrong": 0},
        answers=[]
    )
    await message.answer(text=LEXICON_RU['/start'], reply_markup=kb.main_kb)

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

#Обработчики главной клавиатуры
@router.message(F.text == "Граматика")
async def cmd_start_gramar(message: Message, state: FSMContext):
    """Изучение граматики"""
    keyboard = kb.get_grammar_keyboard(gm.get_all_names())
    await message.answer("Выберите правило: ", reply_markup=keyboard.as_markup())
    await state.set_state(MainStates.select_grammar)

@router.message(F.text == "Начать тестирование")
async def cmd_start_test(message: Message, state: FSMContext):
    """Начало тестирования. Выбор категории."""
    categories = wm.get_categories()
    keyboard = kb.get_categories_keyboard(categories)

    await message.answer(text="Выберите категорию:", reply_markup=keyboard.as_markup())
    await state.update_data(  # Инициализируем данные пользователя
        language=um.get_user_by_tg_id(message.from_user.id)["language"],
        score={"correct": 0, "wrong": 0},
        answers=[]
    )
    await state.set_state(MainStates.select_category)

@router.message(F.text == "Выбрать язык слов")
async def cmd_select_language(message: Message):
    """Выбор языка теста."""
    language_keyboard = kb.pick_language_kb
    await message.answer("Выберите язык теста:", reply_markup=language_keyboard)

#Установка выбранного языка
@router.callback_query(F.data.in_(["language_serbian", "language_russian"]))
async def set_language(callback: CallbackQuery, state: FSMContext):
    """Установка языка теста."""
    language = "serbian" if callback.data == "language_serbian" else "russian"
    um.update_user_language(callback.from_user.id, language)
    await state.update_data(language=language)
    await callback.message.edit_text(f"Язык теста установлен на {'Сербский' if language == 'serbian' else 'Русский'}.")


#Обработчик после выбранной категории
@router.callback_query(F.data.startswith("category_"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    """Сохранение выбранной категории и начало тестирования."""
    category = callback.data.split("_")[1]
    words = wm.get_all_words() if category == "all" else wm.get_words_by_category(category)

    await state.update_data(
        words=random.sample(words, min(len(words), 15)),
        current_index=0,
        score={"correct": 0, "wrong": 0},
        answers=[],
        category=category
    )

    await state.set_state(MainStates.testing)
    await send_next_question(callback.message, state)

#Отправка следующего вопроса пользователю
async def send_next_question(message: Message, state: FSMContext):
    """Отправка следующего вопроса пользователю."""
    data = await state.get_data()
    words = data["words"]
    current_index = data["current_index"]
    answers_list = wm.get_all_words() if data["category"] == "all" else wm.get_words_by_category(data["category"])

    if current_index >= len(words):
        await show_results(message, state)
        return

    word = words[current_index]
    question = word[0] if data["language"] == "serbian" else word[1]
    correct_answer = word[1] if data["language"] == "serbian" else word[0]

    answers = [correct_answer] + random.sample(
        [w[1] if data["language"] == "serbian" else w[0] for w in answers_list if w != word], 3
    )
    random.shuffle(answers)

    keyboard = kb.get_answers_keyboard(answers)
    await message.edit_text(f"Выберите перевод для: <b>{question}</b>", reply_markup=keyboard.as_markup(), parse_mode="HTML")


#Хэндлер, срабатывающий в состоянии тестирования
@router.callback_query(F.data.startswith("answer_"))
async def process_answer(callback: CallbackQuery, state: FSMContext) -> None:
    """Обработка ответа пользователя."""
    data = await state.get_data()
    current_index = data["current_index"]
    words = data["words"]

    word = words[current_index]
    correct_answer = word[1] if data["language"] == "serbian" else word[0]
    selected_answer = callback.data.split("_")[1]

    if selected_answer == correct_answer:
        data["score"]["correct"] += 1
    else:
        data["score"]["wrong"] += 1
        data["answers"].append((word[0], word[1]))

    await state.update_data(current_index=current_index + 1, score=data["score"], answers=data["answers"])
    await send_next_question(callback.message, state)

#Отправка пользователю результатов теста
async def show_results(message: Message, state: FSMContext) -> None:
    """Показ результатов теста."""
    data = await state.get_data()
    correct = data["score"]["correct"]
    wrong = data["score"]["wrong"]

    result_text = f"Тест завершен!\n\nПравильных ответов: {correct}\nНеправильных ответов: {wrong}\n"

    if data["answers"]:
        result_text += "\nОшибки:\n" + "\n".join([f"{w[0]} - {w[1]}" for w in data["answers"]])

    await message.edit_text(result_text)
    await message.answer("Тест завершен.")
    await state.clear()


#Обработка в разделе граматика
@router.callback_query(F.data.startswith("rule_"))
async def select_category(callback: CallbackQuery, state: FSMContext):
    name = callback.data.split("_")[1]
    rule = gm.get_data_by_name(name)
    desc = rule["desc"]
    if desc:
        await callback.message.answer(desc)
    if rule["image"]:
        image_path = conf.get_image_path(folder="grammar", name=rule["image"])
        await callback.message.answer_photo(FSInputFile(image_path))
    if rule["file"]:
        pass

@router.callback_query(F.data.startswith("page_"))
async def process_pagination(callback_query: CallbackQuery):
    # Извлекаем номер страницы из callback_data
    page_number = int(callback_query.data.split('_')[1])
    categories = wm.get_categories()
    keyboard = kb.get_categories_keyboard(categories, page_number)

    # Ответ на callback (перезагружаем клавиатуру с новым набором категорий)
    await callback_query.message.edit_text("Выберите категорию:", reply_markup=keyboard.as_markup())
