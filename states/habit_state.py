from aiogram.fsm.state import State, StatesGroup


class HabitSG(StatesGroup):
    waiting_text = State()
    waiting_time = State()