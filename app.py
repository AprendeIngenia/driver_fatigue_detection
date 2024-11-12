import cv2
import base64
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from drowsiness_processor.main import DrowsinessDetectionSystem


app = FastAPI()
drowsiness_detection_system = DrowsinessDetectionSystem()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # read data
            data = await websocket.receive_text()

            # decode data
            original_image, sketch, json_report = drowsiness_detection_system.run(data)

            _, buffer = cv2.imencode('.jpg', sketch)
            sketch_base64 = base64.b64encode(buffer).decode('utf-8')

            # send answer
            await websocket.send_json({
                "json_report": json_report,
                "sketch_image": sketch_base64
            })

    except WebSocketDisconnect:
        print("disconnect client")

