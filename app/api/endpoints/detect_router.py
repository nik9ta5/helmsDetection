from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from PIL import Image
from io import BytesIO
import numpy as np
import uuid
import asyncio


# Импортируем сервисы
from services.detection_service import detectImages
from services.analises_service import analysDetectResult
from services.notification_service import notificationSend
from services.tgbot_service import *



router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    # await send_message_to_user(1969744434, f"Подключился кто-то")
    try:
        client_uuid = str(uuid.uuid4())
        while True:
            # Получаем изображение от клиента
            img_bytes = await websocket.receive_bytes()
            img = Image.open(BytesIO(img_bytes))
            img_tensor = np.array(img)

            # Выполняем обработку изображения
            result_detect = detectImages(img_tensor)
            mode, pick = analysDetectResult(result_detect, client_uuid)

            # Отправляем уведомление клиенту, если оно требуется
            # bytes_array = notificationSend(mode, pick, client_uuid)
            print(mode)
            if mode:
                print(pick)
                #Идем по всем chat_id
                for chat_id in CHAT_IDS_ALL_USERS_BOT:
                    print(chat_id)
                    await send_photo_to_user(chat_id, pick)
                    # await send_message_to_user(chat_id, f"img, cl_id: {client_uuid}")
                # await websocket.send(bytes_array)

    except WebSocketDisconnect:
        print("Клиент отключился")
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        await websocket.send_text(f"Ошибка: {str(e)}")
