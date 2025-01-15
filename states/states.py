from aiogram.fsm.state import StatesGroup, State

# Состояния бота
class MainStates(StatesGroup):
    select_language = State()
    select_grammar = State()
    select_category = State()
    testing = State()