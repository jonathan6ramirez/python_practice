import pyodbc
import logging
import time

# import pypyodbc
import asyncio
import websockets

# SQL Server Connection
DB_SERVER = "JZNTC-SQL"
DB_NAME = "StrohTestDB"
DB_USER = "StrohTestDev"
# DB_PASSWORD = "YOUR_PASSWORD"

# WebSocket Server Port
WS_PORT = 8764

# WebSocket clients list
connected_clients = set()


def connect_to_database():
    """Try to connect to the SQL Server database."""
    try:
        conn = pyodbc.connect(
            DRIVER="{ODBC Driver 18 for SQL Server}",
            server=DB_SERVER,
            database=DB_NAME,
            trustservercertificate="yes",
            encrypt="yes",
            trusted_connection="yes",
        )
        logging.info("Connected to the SQL Server database successfully.")
        return conn

    except pyodbc.Error as e:
        logging.error(f"Failed to connect to the SQL Server database: {e}")
        return None


async def send_alerts(websocket):
    """Listens for new alerts and sends them to WebSocket clients in real-time."""
    connected_clients.add(websocket)
    logging.info("📡 WebSocket Client Connected!")

    conn = None

    # Attempt to connect to the database
    while conn is None:
        conn = connect_to_database()  # Try to connect to the database
        if conn is None:
            logging.info("Retrying to connect to the database...")
            # print("Retrying to connect to the database...")
            await asyncio.sleep(5)  # Wait for 5 seconds before retrying

    cursor = conn.cursor()

    last_alert = None

    while True:
        try:
            # Receive message from the AlertQueue
            cursor.execute("RECEIVE TOP(1) message_body FROM AlertQueue;")
            row = cursor.fetchone()

            if row:
                alert_message = row[0]
                logging.info(f"📢 Sending Alert: {alert_message}")

                for client in connected_clients:
                    try:
                        await websocket.send(alert_message)  # Send alert to client
                    except websockets.exceptions.ConnectionClosed:
                        # Remove any disconnected clients.
                        connected_clients.remove(client)

                last_alert = alert_message  # Update the last sent alert

            await asyncio.sleep(1)  # Check for updates every second

        except Exception as e:
            logging.error(f"Error occurred while fetching or sending alerts: {e}")
            # print(f"Error occurred while fetching or sending alerts: {e}")
            await websocket.send("Error fetching alerts from the server.")
            break

    connected_clients.remove(websocket)


async def websocket_server():
    """Starts the WebSocket server to send alerts in real-time."""
    async with websockets.serve(send_alerts, "0.0.0.0", WS_PORT):
        print(f"🚀 WebSocket Server Running on ws://localhost:{WS_PORT}")
        await asyncio.Future()  # Keep the server running


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(websocket_server())
