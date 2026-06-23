from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.habits_callback import HabitCallback

def habit_keyboard(habit_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=HabitCallback(action='delete', habit_id=habit_id).pack()
                )
            ]
        ]
    )