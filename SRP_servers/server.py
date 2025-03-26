from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import asyncio

app = FastAPI()
connected_clients = set()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """Handles new websocket connections."""
    await websocket.accept()
    connected_clients.add(websocket)
    print(f"New client connected: {websocket.client}")

    try:
        while True:
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        print(f"Client disconnected: {websocket.client}")
        connected_clients.remove(websocket)


async def send_alert(alert_name: str):
    """Broadcasts and aler to all connect clients."""
    if connected_clients:
        print(f"Sending alert: {alert_name}")
        for client in connected_clients:
            await client.send_text(f"ALERT: {alert_name}")
    else:
        print("No clients connected.")


@app.get("/trigger/{alert_name}")
async def trigger_alert(alert_name: str):
    """HTTP endpoint to manually trigger an alert(useful for testing)"""
    await send_alert(alert_name)
    return {"message": f"Alert {alert_name} sent!"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
