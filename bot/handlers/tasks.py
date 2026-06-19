import logging
from aiogram import Router , F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from states.tasks_state import TaskSG
from services.task_service import TaskService
from bot.keyboards.tasks_kb import task_keyboard
from aiogram.exceptions import TelegramBadRequest

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

    tasks= await task_service.get_tasks(user_id=message.from_user.id)

    if not tasks:
        await message.answer(f"No tasks")
    else:
        for task in tasks:
            status = "☑" if not task.is_done else "☐"
            await message.answer(f"{status} {task.title}", reply_markup=task_keyboard(task_id=task.id, is_done=task.is_done))

@tasks_router.callback_query(F.data.startswith('toggle:'))
async def process_toggle_task(callback: CallbackQuery, task_service: TaskService):

    task_id = int(callback.data.split(':')[1])

    task = await task_service.get_task_by_id(task_id=task_id)

    new_status = not task.is_done

    await task_service.mark_done(task_id=task.id, is_done=new_status)

    try:

        status = "☑" if not new_status else "☐"
        await callback.message.edit_text(f"{status} {task.title}", reply_markup=task_keyboard(task_id=task.id, is_done=new_status))

        await callback.answer()

    except TelegramBadRequest:
        await callback.answer()

