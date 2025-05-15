import string
import asyncio

characters = string.digits + string.ascii_uppercase + string.ascii_lowercase
base = len(characters)

async def encode_base62(num: int) -> str:
    if num == 0:
        return characters[0]
    encoded = []
    while num:
        num, rem = divmod(num, base)
        encoded.append(characters[rem])
        await asyncio.sleep(0)
    return ''.join(reversed(encoded))

async def decode_base62(encoded: str) -> int:
    decoded = 0
    for char in encoded:
        decoded = decoded * base + characters.index(char)
        await asyncio.sleep(0) 
    return decoded
