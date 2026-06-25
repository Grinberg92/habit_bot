import logging
import re
from aiogram import Bot, Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from services.habit_service import HabitService
from services.habit_completions_service import HabitCompletionService
from services.schaduler_service import SchedulerService
from states.habit_state import HabitSG
from bot.keyboards.habits_kb import habit_keyboard, edit_habit_keyboard, accept_delete_keyboard
from bot.callbacks.habits_callback import HabitCallback

logger = logging.getLogger(__name__)

habit_router = Router()

_TIME_RE = re.compile(r'^([01]\d|2[0-3]):([0-5]\d)$')


@habit_router.message(Command(commands='cancel'), StateFilter(HabitSG.waiting_text, HabitSG.waiting_time))
async def process_cancel_cmd(message: Message, state: FSMContext, bot: Bot) -> None:

    data = await state.get_data()

    await bot.delete_message(message_id=data['message_id'], chat_id=data['chat_id'])

    if data.get('title_message_id') or data.get('title_chat_id'):

        await bot.delete_message(message_id=data['title_message_id'], chat_id=data['title_chat_id'])

    await state.clear()

    await message.answer("Operation was canceled")

@habit_router.message(Command(commands='add_habit'))
async def process_remind_cmd(message: Message, state: FSMContext) -> None:
    sent_message = await message.answer(
        "Input title:"
    )
    await state.set_state(HabitSG.waiting_text)

    await state.update_data(message_id=sent_message.message_id, chat_id=sent_message.chat.id)

@habit_router.message(StateFilter(HabitSG.waiting_text))
async def process_waiting_text_state(message: Message, state: FSMContext) -> None:

    title_message_id = message.message_id

    title_chat_id = message.chat.id

    await state.update_data(text=message.text)

    sent_message = await message.answer(
        "Input time (HH:MM):"
    )

    await state.set_state(HabitSG.waiting_time)

    await state.update_data(message_id=sent_message.message_id, chat_id=sent_message.chat.id, 
                            title_message_id=title_message_id, title_chat_id=title_chat_id)

@habit_router.message(StateFilter(HabitSG.waiting_time))
async def process_waiting_min_state(message: Message, state: FSMContext, bot: Bot, habit_service: HabitService) -> None:

    time = message.text.strip()

    if not _TIME_RE.match(time):
        await message.answer(
            "Неверный формат времени. Введите время в формате HH:MM (например, 09:30):"
        )
        return

    data = await state.get_data()

    habit = await habit_service.create_habit(user_id=message.from_user.id, title=data['text'], reminder_time=time)

    if habit is not None:
        logger.info(
            f"Habit {habit.title} created"
        )    

        SchedulerService.add_habit_job(
            bot=bot,
            habit=habit,
            habit_service=habit_service
        )

        logger.info(
            f"Habit job {habit.title} created"
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
            f"⏰ {habit.reminder_time}\n"
            f"Status: {'Active ✅' if habit.is_active else 'No active ❌'}",
            reply_markup=habit_keyboard(habit_id=habit.id, is_active=habit.is_active)
        )

        logger.info(f"Got habit {habit.id}")

@habit_router.callback_query(HabitCallback.filter(F.action == 'delete'))
async def process_delete_habit_cmd(callback: CallbackQuery, callback_data: HabitCallback, habit_service: HabitService, state: FSMContext) -> None:

    await state.set_state(HabitSG.delete)

    habit = await habit_service.get_habit_by_id(habit_id=callback_data.habit_id)

    if habit is not None:

        await state.update_data(habit_id=habit.id)

        await callback.message.edit_reply_markup(reply_markup=accept_delete_keyboard(habit_id=habit.id))

        await callback.answer()

@habit_router.callback_query(HabitCallback.filter(F.action.in_({'yes_delete', 'no_delete'})), StateFilter(HabitSG.delete))
async def process_delete_habit(callback: CallbackQuery, habit_service: HabitService, callback_data: HabitCallback, state: FSMContext) -> None:

    data = await state.get_data()

    habit_id = data['habit_id']

    if callback_data.action == 'yes_delete':

        deleted = await habit_service.delete_habit(habit_id=habit_id)

        if deleted:

            SchedulerService.delete_job(habit_id=habit_id)

            logger.info(f"Habit {habit_id} deleted")

            await callback.message.delete()

        await state.clear()

        await callback.answer()

    else:

        habit = await habit_service.get_habit_by_id(habit_id=habit_id)
        
        if habit is not None:

            await callback.message.edit_reply_markup(reply_markup=habit_keyboard(habit_id=habit.id, is_active=habit.is_active))

            await state.clear()

            await callback.answer()

@habit_router.callback_query(HabitCallback.filter(F.action == 'toggle_habit'))
async def process_toggle_habit(callback: CallbackQuery, callback_data: HabitCallback, habit_service: HabitService, bot: Bot) -> None:

    habit = await habit_service.get_habit_by_id(habit_id=callback_data.habit_id)

    new_status = not habit.is_active

    set_status = await habit_service.set_active_habit(habit_id=habit.id, is_active=new_status)

    try:
        if set_status:
            
            logger.info("Status habit %s changed to %s", habit.id, new_status)

            if new_status:
                SchedulerService.add_habit_job(bot=bot, habit=habit, habit_service=habit_service)
                logger.info(f"Habit job {habit.id} enabled")
            else:
                SchedulerService.delete_job(habit_id=habit.id)
                logger.info(f"Habit job {habit.id} disabled")

            await callback.message.edit_text(
                text=            
                f"🔔 {habit.title}\n"
                f"⏰ {habit.reminder_time}\n"
                f"Status: {'Active ✅' if new_status else 'No active ❌'}",
                reply_markup=habit_keyboard(habit_id=habit.id, is_active=new_status)
            )

    except Exception:
        logger.exception("Failed to edit habit message")

    finally:
        await callback.answer()

@habit_router.callback_query(HabitCallback.filter(F.action == 'edit'))
async def process_edit_habit_state(callback: CallbackQuery, callback_data: HabitCallback) -> None:

    await callback.message.edit_reply_markup(
        reply_markup=edit_habit_keyboard(
            habit_id=callback_data.habit_id
        )
    )

    await callback.answer()

@habit_router.callback_query(HabitCallback.filter(F.action == 'edit_title'))
async def process_edit_title_state(callback: CallbackQuery, callback_data: HabitCallback, state: FSMContext, habit_service: HabitService) -> None:

    await state.update_data(habit_id=callback_data.habit_id, message_id=callback.message.message_id)

    await callback.message.answer(f"Input new title:")

    await state.set_state(HabitSG.editing_title)

    await callback.answer()

@habit_router.message(StateFilter(HabitSG.editing_title))
async def process_new_title(message: Message, state: FSMContext, habit_service: HabitService, bot: Bot):

    data = await state.get_data()

    habit = await habit_service.get_habit_by_id(habit_id=data['habit_id'])

    if habit is not None:
        
        success = await habit_service.update_habit_title(habit_id=habit.id, title=message.text)

        if success:

            upd_habit = await habit_service.get_habit_by_id(habit_id=data['habit_id'])

            SchedulerService.reschedule_job(bot=bot, habit=upd_habit, habit_service=habit_service)

            await bot.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=data["message_id"],
                            text=(
                                f"🔔 {upd_habit.title}\n"
                                f"⏰ {upd_habit.reminder_time}\n"
                                f"Status: {'Active ✅' if upd_habit.is_active else 'No active ❌'}"
                            ),
                            reply_markup=habit_keyboard(
                                habit_id=upd_habit.id,
                                is_active=upd_habit.is_active
                            )
                        )

            await message.answer(
                "✅ Title updated"
            )
    
    await state.clear()

@habit_router.callback_query(HabitCallback.filter(F.action == 'edit_time'))
async def process_edit_time_state(callback: CallbackQuery, callback_data: HabitCallback, state: FSMContext) -> None:

    await state.update_data(habit_id=callback_data.habit_id, message_id=callback.message.message_id)

    await callback.message.answer(f"Input new time:")

    await state.set_state(HabitSG.editing_time)

    await callback.answer()

@habit_router.message(StateFilter(HabitSG.editing_time))
async def process_new_time(message: Message, state: FSMContext, habit_service: HabitService, bot: Bot) -> None:

    time= message.text.strip()

    if not _TIME_RE.match(time):
        await message.answer(
            "Неверный формат времени. Введите время в формате HH:MM (например, 09:30):"
        )
        return

    data = await state.get_data()

    habit = await habit_service.get_habit_by_id(habit_id=data['habit_id'])

    if habit is not None:
        
        success = await habit_service.update_habit_time(habit_id=habit.id, time=time)

        if success:

            upd_habit = await habit_service.get_habit_by_id(habit_id=data['habit_id'])

            SchedulerService.reschedule_job(bot=bot, habit=upd_habit, habit_service=habit_service)

            await bot.edit_message_text(
                            chat_id=message.chat.id,
                            message_id=data["message_id"],
                            text=(
                                f"🔔 {upd_habit.title}\n"
                                f"⏰ {upd_habit.reminder_time}\n"
                                f"Status: {'Active ✅' if upd_habit.is_active else 'No active ❌'}"
                            ),
                            reply_markup=habit_keyboard(
                                habit_id=upd_habit.id,
                                is_active=upd_habit.is_active
                            )
                        )

            await message.answer(
                "✅ Time updated"
            )
    
    await state.clear()

@habit_router.callback_query(HabitCallback.filter(F.action == 'back'))
async def process_back(callback: CallbackQuery, callback_data: HabitCallback, habit_service: HabitService) -> None:

    habit = await habit_service.get_habit_by_id(habit_id=callback_data.habit_id)

    await callback.message.edit_reply_markup(
        reply_markup=habit_keyboard(
            habit_id=habit.id,
            is_active=habit.is_active
        )
    )

    await callback.answer()
    
@habit_router.callback_query(HabitCallback.filter(F.action == 'done'))
async def process_done_habit(callback: CallbackQuery, callback_data: HabitCallback, habit_completion_service: HabitCompletionService) -> None:

    created = await habit_completion_service.done_habit(habit_id=callback_data.habit_id)

    if created is not None:

        await callback.message.edit_text(
            text=callback.message.text + "\n\n✅ Done"
        )

        await callback.answer("Done")

    else:

        await callback.answer("Already done today")
