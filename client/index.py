import cv2
import asyncio
import websockets
from io import BytesIO
from PIL import Image
import numpy as np


def bytes_to_numpy_image(byte_data):
    buffer = BytesIO(byte_data)
    image = Image.open(buffer)
    return np.array(image)


async def connect_to_server():
    uri = "ws://127.0.0.1:5000/ws"  # Адрес WebSocket сервера
    async with websockets.connect(uri) as websocket:

        # Открываем видеофайл
        cap = cv2.VideoCapture('videos_dir/output_video.mp4')

        if not cap.isOpened():
            print("Ошибка: не удалось открыть видеофайл")
            exit()

        while True:
            # Считываем кадр
            ret, frame = cap.read()

            # Проверяем, успешно ли считался кадр
            if not ret:
                print("Ошибка: не удалось считать кадр")
                break

            _, img_encoded = cv2.imencode('.jpg', frame)
            img_bytes = img_encoded.tobytes()  # Преобразуем в байты

            await websocket.send(img_bytes)
            await asyncio.sleep(5)

            # # Отображаем кадр
            cv2.imshow('Video', frame)

            # Выходим из цикла, если нажата клавиша 'q'
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
        cap.release()
        cv2.destroyAllWindows()

# Запуск клиента
asyncio.run(connect_to_server())
