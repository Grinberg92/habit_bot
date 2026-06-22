import logging
from aiogram import Bot, Router , F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router
from database.models.habits import Habit
from services.habit_service import HabitService
from states.habit_state import HabitSG
from scheduler.jobs import send_reminder


logger = logging.getLogger(__name__)

habit_router = Router()


@habit_router.message(Command(commands='add_habit'))
async def process_remind_cmd(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Введите название привычки:"
    )
    await state.set_state(HabitSG.waiting_text)

@habit_router.message(StateFilter(HabitSG.waiting_text))
async def process_waiting_text_state(message: Message, state: FSMContext) -> None:

    await state.update_data(text=message.text)

    await message.answer(
        "Введите время (HH:MM):"
    )

    await state.set_state(HabitSG.waiting_time)

@habit_router.message(StateFilter(HabitSG.waiting_time))
async def process_waiting_min_state(message: Message, state: FSMContext, bot: Bot, habit_service: HabitService) -> None:


    data = await state.get_data()

    habit = await habit_service.create_habit(user_id=message.from_user.id, title=data['text'], reminder_time=message.text)

    await message.answer(
        f"✅ Привычка {habit.title} создана\n"
        f"⏰ Время: {habit.reminder_time}"
    )

    await state.clear()


