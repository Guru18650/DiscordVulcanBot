import asyncio
from vulcan import Keystore
import json
async def main():
    keystore = Keystore.create(device_model="VulcanBot")
    with open("keystore.json", "w") as f:
        f.write(keystore.as_json)
asyncio.run(main())
