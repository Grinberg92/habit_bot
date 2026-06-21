from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot.callbacks.pagination_callback import PaginationCallback

def pagination_kb(page: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⬅️",
                    callback_data=PaginationCallback(action='prev', page=page - 1).pack()
                )
            ,
                        
                InlineKeyboardButton(
                    text=f"{page}",
                    callback_data="ignore"
                )
            
            ,
                InlineKeyboardButton(
                    text="➡️",
                    callback_data=PaginationCallback(action='next', page=page + 1).pack()
                )
            ]
        ]
    )