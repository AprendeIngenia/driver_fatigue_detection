import cv2
import base64
import asyncio
import websockets
import json
import numpy as np


async def send_video():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # code frame: JPEG & base64
            _, buffer = cv2.imencode('.jpg', frame)
            frame_base64 = base64.b64encode(buffer).decode('utf-8')

            # send frame to server
            await websocket.send(frame_base64)

            # receiving frame from server
            response = await websocket.recv()
            response_data = json.loads(response)

            json_report = response_data.get('json_report')
            sketch_base64 = response_data.get('sketch_image')

            sketch_data = base64.b64decode(sketch_base64)
            nparr = np.frombuffer(sketch_data, np.uint8)
            sketch_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            cv2.imshow('Drowsiness Detection', sketch_image)
            print(json_report)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

asyncio.run(send_video())
