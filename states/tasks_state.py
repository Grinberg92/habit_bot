from aiogram.fsm.state import State, StatesGroup

class TaskSG(StatesGroup):
    
    input_task = State()