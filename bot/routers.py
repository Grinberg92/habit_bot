from aiogram import Router
from bot.handlers.start import start_router
from bot.handlers.tasks import tasks_router

def setup_routers() -> Router:
    
    router = Router()
    
    router.include_routers(start_router, tasks_router)
    
    return router