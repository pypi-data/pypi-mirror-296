import asyncio
from bleak import BleakScanner


async def find_led_device():
    devices = await BleakScanner.discover()
    for device in devices:
        if "BJ_LED_M" in device.name:
            print(f"Found LED: {device.name} with MAC {device.address}")
            print(f'Metadata: {device.metadata['uuids']}')
            return device.address, device
    return None, None