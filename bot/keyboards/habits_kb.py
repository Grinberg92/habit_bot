from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.habits_callback import HabitCallback

def habit_keyboard(habit_id: int, is_active: bool = False) -> InlineKeyboardMarkup:

    status_text = '💤 Disable' if is_active else '🟢 Enable'
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Edit",
                    callback_data=HabitCallback(action='edit', habit_id=habit_id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="🗑 Delete",
                    callback_data=HabitCallback(action='delete', habit_id=habit_id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text=status_text,
                    callback_data=HabitCallback(action='toggle_habit', habit_id=habit_id).pack()
                )
            ]
        ]
    )

def edit_habit_keyboard(habit_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Edit title",
                    callback_data=HabitCallback(action='edit_title', habit_id=habit_id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Edit time",
                    callback_data=HabitCallback(action='edit_time', habit_id=habit_id).pack()
                )
            ],
            [
                InlineKeyboardButton(
                    text="Back",
                    callback_data=HabitCallback(action='back', habit_id=habit_id).pack()
                )
            ]
        ]
    )

def done_habit_keyboard(habit_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Done",
                    callback_data=HabitCallback(action='done', habit_id=habit_id).pack()
                )
            ]
        ]
    )

def accept_delete_keyboard(habit_id: int) -> InlineKeyboardMarkup:

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="No",
                    callback_data=HabitCallback(action='no_delete', habit_id=habit_id).pack()
                ),
                InlineKeyboardButton(
                    text="Yes",
                    callback_data=HabitCallback(action='yes_delete', habit_id=habit_id).pack()
                )
            ]
        ]
    )
