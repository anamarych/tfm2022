# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
import os
import asyncio
import random
import logging
import json

from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.aio import ProvisioningDeviceClient
from azure.iot.device import Message, MethodResponse
from datetime import timedelta, datetime

logging.basicConfig(level=logging.ERROR)

# The device "Thermostat" that is getting implemented using the above interfaces.
# This id can change according to the company the user is from
# and the name user wants to call this Plug and Play device
CONNECTION_STRING = os.getenv("IOTHUB_DEVICE_CONNECTION_STRING")
model_id = "dtmi:com:example:siotcom;1"

#####################################################
# TELEMETRY TASKS

async def send_data_from_device(device_client, telemetry_msg):
    msg = Message(json.dumps(telemetry_msg))
    msg.content_encoding = "utf-8"
    msg.content_type = "application/json"
    print("Sent message")
    await device_client.send_message(msg)

def stdin_listener():
    """
    Listener for quitting the sample
    """
    while True:
        selection = input("Press Q to quit\n")
        if selection == "Q" or selection == "q":
            print("Quitting...")
            break

# END KEYBOARD INPUT LISTENER
#####################################################


#####################################################
# MAIN STARTS
async def main():
    device_client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING, product_info=model_id)

    # Connect the client.
    await device_client.connect()

    ################################################
    # Send telemetry (current temperature)

    async def send_data():
        temperature_msg1 = {
            "time": "2022-06-22T17:09:44.782574",
            "class": "4405",
            "hub": "000FF001",
            "node": "131334",
            "data": {"humidity": 24.3,
                     "room_temp": 25.4,
                     "luminosity": 90.83,
                     "add_temp": 25.71,
                     "surf_temp": 25.43}}
        await send_data_from_device(device_client, temperature_msg1)

    send_data_task = asyncio.create_task(send_data())

    # Run the stdin listener in the event loop
    loop = asyncio.get_running_loop()
    user_finished = loop.run_in_executor(None, stdin_listener)
    # # Wait for user to indicate they are done listening for method calls
    await user_finished

    send_telemetry_task.cancel()

    # Finally, shut down the client
    await device_client.shutdown()

# EXECUTE MAIN
if __name__ == "__main__":
    asyncio.run(main())
