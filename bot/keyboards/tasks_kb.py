from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def task_keyboard(task_id: int, is_done: bool) -> InlineKeyboardMarkup:

    text = "Mark done" if is_done else "Mark undone"

    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=text,
            callback_data=f"toggle:{task_id}",
                    )   
                ]
            ]
        )