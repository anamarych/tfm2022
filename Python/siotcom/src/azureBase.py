#Local imports

#External imports
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message, MethodResponse
from datetime import timedelta, datetime
# from azure.iot.device.aio import ProvisioningDeviceClient

import json
import os

#Global Config
 DEVICE_ID = "concentrador"
 CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING") #connection string is an env

async def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    await device_client.connect()

    # Send a single message
    print("Sending message...")
    await device_client.send_message("This is a message that is being sent")
    print("Message successfully sent!")
    await device_client.shutdown()

if __name__ == "__main__":
    asyncio.run(main())