import asyncio
from vulcan import Keystore
import json
from vulcan import Account
token = ""
symbol = ""
pin = ""
async def main():
    with open("keystore.json") as f:
        keystore = Keystore.load(f)
    account = await Account.register(keystore, token, symbol, pin)
    with open("account.json", "w") as f:
        f.write(account.as_json)
asyncio.run(main())
