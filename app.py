import cv2
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from drowsiness_processor.main import DrowsinessDetectionSystem


app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    drowsiness_detection_system = DrowsinessDetectionSystem()

    await websocket.accept()
    try:
        while True:
            # read data
            data = await websocket.receive_text()

            # decode data
            original_image, sketch, json_report = drowsiness_detection_system.run(data)

            _, buffer_sketch = cv2.imencode('.jpg', sketch)
            sketch_base64 = base64.b64encode(buffer_sketch).decode('utf-8')

            _, buffer_original_image = cv2.imencode('.jpg', original_image)
            original_image_base64 = base64.b64encode(buffer_original_image).decode('utf-8')

            # send answer
            await websocket.send_json({
                "json_report": json_report,
                "sketch_image": sketch_base64,
                "original_image": original_image_base64,
            })

    except WebSocketDisconnect:
        print("disconnect client")

