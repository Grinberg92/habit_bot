import logging

from aiogram import F, Router 
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from states.tasks_state import TaskSG
from services.task_service import TaskService

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

        await task_service.create_task(user_id=message.from_user.id, title=task_text)

    except Exception as e:

        await state.clear()

        logger.critical(f"Error processing adding task {e}")



