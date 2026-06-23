import logging
from aiogram import Bot, Router , F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import Router
from database.models.habits import Habit
from services.habit_service import HabitService
from services.schaduler_service import SchedulerService
from states.habit_state import HabitSG
from bot.keyboards.habits_kb import habit_keyboard
from bot.callbacks.habits_callback import HabitCallback

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

    SchedulerService.add_habit_job(
        bot=bot,
        habit=habit
    )

    await message.answer(
        f"✅ Привычка {habit.title} создана\n"
        f"⏰ Время: {habit.reminder_time}"
    )

    await state.clear()

@habit_router.message(Command(commands='list_habits'))
async def list_habits(message: Message, habit_service: HabitService) -> None:

    habits = await habit_service.get_habit_by_user(user_id=message.from_user.id)

    if not habits:

        await message.answer(
            "No habits"
        )
        return
    
    for habit in habits:

        await message.answer(
            f"🔔 {habit.title}\n"
            f"⏰ {habit.reminder_time}",
            reply_markup=habit_keyboard(habit_id=habit.id)
        )

@habit_router.callback_query(HabitCallback.filter(F.action == 'delete'))
async def process_delete_habit(callback: CallbackQuery, callback_data: HabitCallback, habit_service: HabitService) -> None:

    deleted = await habit_service.delete_habit(habit_id=callback_data.habit_id)

    if deleted:

        SchedulerService.delete_job(habit_id=callback_data.habit_id)

        await callback.message.delete()

    await callback.answer()

