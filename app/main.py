from fastapi import FastAPI
from api.endpoints import detect_router
import uvicorn
import threading

from services.tgbot_service import *

#Создаем приложение
app = FastAPI(
    title="Detect helmets",
    description="Server application for detect helmets in heads.",
    version="1.0.0"
)

#Добавляем эндпоинты    
app.include_router(detect_router.router)

#Тестовый
@app.get("/")
async def root():
    return {"message": "Helmet Detection API is running!"}


async def main():
    # # #Запуск бота в отдельном потоке
    # # loop = asyncio.get_event_loop()
    # # loop.run_in_executor(None, bot_service_run)
    
    # # #Запуск приложения FAST API
    # # uvicorn.run(app, host="127.0.0.1", port=5000)

    # bot_task = asyncio.create_task(bot_service_run())
    # # Запуск бота в отдельном потоке
    # # bot_thread = threading.Thread(target=bot_service_run)
    # # bot_thread.start()

    # # Запуск приложения FAST API
    # uvicorn.run(app, host="127.0.0.1", port=5000)


    # Запуск бота в отдельной задаче
    bot_task = asyncio.create_task(bot_service_run())

    # Запуск приложения FAST API
    config = uvicorn.Config(app, host="127.0.0.1", port=5000)
    server = uvicorn.Server(config)
    await server.serve()


if __name__ == "__main__":
    asyncio.run(main())