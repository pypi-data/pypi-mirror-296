import asyncio
from bleak import BleakClient

address = "64:15:a8:00:6b:a6"

async def discover_services(address):
    async with BleakClient(address) as client:
        services = await client.get_services()
        for service in services:
            print(f"Servicio: {service.uuid}")
            for char in service.characteristics:
                print(f"  Característica: {char.uuid}")

asyncio.run(discover_services(address))
