import asyncio
from typing import Tuple, List, Optional
from bleak import BleakScanner, BleakClient

class Scanner:
    """Class to scan BJ_LED_M devices and retrieve UUIDs of services"""


    async def scan_led(self) -> Tuple[Optional[str], Optional[object]]:
        """
        Scans for LED devices with the name 'BJ_LED_M'.

        :return: A tuple with the MAC address and the device object if found,
                 otherwise returns (None, None).
        """
        devices = await BleakScanner.discover()
        for device in devices:
            if "BJ_LED_M" in device.name:
                print(f"Found LED: {device.name} with MAC: {device.address}")
                print(f"Metadata: {device.metadata['uuids']}")
                return device.address, device
        return None, None


    async def scan_uuids(self, address: str) -> List[str]:
        """
        Scans and lists UUIDs of a device at the given MAC address.

        :param address: MAC address of the device.
        :return: List of UUIDs from the device's characteristics.
        """
        async with BleakClient(address) as client:
            services = await client.get_services()
            uuid_list = []
            for service in services:
                print(f"Service UUID: {service.uuid}")
                for char in service.characteristics:
                    print(f"Characteristic UUID: {char.uuid}")
                    uuid_list.append(char.uuid)
            return uuid_list


    async def run(self) -> Tuple[Optional[str], List[str]]:
        """
        Main function that runs both device and UUID scanning.

        :return: A tuple containing the MAC address and a list of UUIDs.
        """
        mac_address, device = await self.scan_led()
        if mac_address:
            uuids = await self.scan_uuids(mac_address)
            return mac_address, uuids
        else:
            return None, []