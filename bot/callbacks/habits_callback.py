from aiogram.filters.callback_data import CallbackData

class HabitCallback(CallbackData, prefix='habit'):
    action: str
    habit_id: int
