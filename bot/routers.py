from aiogram import Router
from bot.handlers.start import start_router

def setup_routers() -> Router:
    
    router = Router()
    
    router.include_routers(start_router)
    
    return router