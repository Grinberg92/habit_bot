import logging
from aiogram import Router , F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.tasks_state import TaskSG
from services.task_service import TaskService
from bot.keyboards.tasks_kb import task_keyboard
from bot.keyboards.pagination_kb import pagination_kb
from aiogram.exceptions import TelegramBadRequest
from bot.callbacks.tasks_callback import TaskCallback
from bot.callbacks.pagination_callback import PaginationCallback

logger = logging.getLogger(__name__)

tasks_router = Router()

@tasks_router.message(Command(commands='add_task'))
async def cmd_add_task(message: Message, state:FSMContext) -> None:
    await message.answer('Input task name:')

    await state.set_state(TaskSG.input_task)

@tasks_router.message(StateFilter(TaskSG.input_task))
async def process_add_task(message: Message, state: FSMContext, task_service: TaskService) -> None:

    try:
        task_text = message.text

        if not task_text.strip():
            await message.answer(f"Task title can't be empty")
            return 

        task= await task_service.create_task(user_id=message.from_user.id, title=task_text)

        if task:
            await message.answer(f"Task '{task.title}' created")
        else:
            await message.answer(f"Task not created")

    except Exception as e:

        logger.exception(
            "Error processing adding task"
        )

    finally:
        await state.clear()

@tasks_router.message(Command(commands='list_tasks'))
async def process_list_tasks_cmd(message: Message, task_service: TaskService) -> None:

    page = 1

    tasks= await task_service.get_tasks_by_user(user_id=message.from_user.id, page=page)

    if not tasks:
        await message.answer(f"No tasks")
        return

    text = "\n".join([f"☐{task.title}" for task in tasks])

    await message.answer(text=text,
                         reply_markup=pagination_kb(page=page))

    

@tasks_router.callback_query(PaginationCallback.filter())
async def process_pagination(callback: CallbackQuery, callback_data: PaginationCallback, task_service: TaskService) -> None:


    page = callback_data.page

    if page <= 0:
        await callback.answer("First page")

    tasks = await task_service.get_tasks_by_user(user_id=callback.from_user.id, page=page)

    if not tasks:
        await callback.answer(f"No more tasks")
        return

    text = "\n".join([f"☐{task.title}" for task in tasks])

    await callback.message.edit_text(text=text,
                         reply_markup=pagination_kb(page=page))
    
    await callback.answer()


@tasks_router.callback_query(TaskCallback.filter(F.action == 'toggle'))
async def process_toggle_task(callback: CallbackQuery, task_service: TaskService, callback_data: TaskCallback) -> None:

    task_id = callback_data.task_id

    task = await task_service.get_task_by_id(task_id=task_id)

    new_status = not task.is_done

    await task_service.mark_done(task_id=task.id, is_done=new_status)

    try:

        status = "☑" if new_status else "☐"
        await callback.message.edit_text(f"{status} {task.title}", reply_markup=task_keyboard(task_id=task.id, is_done=new_status))

        await callback.answer()

    except TelegramBadRequest:
        await callback.answer()


@tasks_router.callback_query(TaskCallback.filter(F.action == 'delete'))
async def process_delete_task(callback: CallbackQuery, callback_data: TaskCallback, task_service: TaskService) -> None:

    task_id = callback_data.task_id

    deleted = await task_service.delete_task(task_id=task_id)

    if deleted:

        await callback.message.delete()

    await callback.answer()

