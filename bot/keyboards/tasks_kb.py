from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.tasks_callback import TaskCallback

def task_keyboard(task_id: int, is_done: bool) -> InlineKeyboardMarkup:

    text = "Mark done" if not is_done else "Mark undone"

    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=text,
            callback_data=TaskCallback(action='toggle', task_id=task_id).pack(),
                    )   
                ],
                [InlineKeyboardButton(
            text="🗑 Delete",
            callback_data=TaskCallback(action='delete', task_id=task_id).pack(),
                    )   
                ]
            ]
        )