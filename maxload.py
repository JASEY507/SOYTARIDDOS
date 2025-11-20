import aiohttp
import asyncio
from fake_useragent import UserAgent

ua = UserAgent()

TARGET = ""   # Boş. Saldırı yok. Sadece gizlilik testi.
CONNECTIONS = 200
DELAY = 0.01

async def worker(session):
    while True:
        if TARGET == "":
            print("[!] TARGET boş. Hiçbir siteye bağlanılmıyor.")
            await asyncio.sleep(1)
            continue
        
        try:
            headers = {"User-Agent": ua.random}
            async with session.get(TARGET, headers=headers, timeout=10) as r:
                print(f"[OK] {r.status}")
        except:
            print("[X] Timeout / Drop")
        await asyncio.sleep(DELAY)

async def main():
    connector = aiohttp.TCPConnector(limit=0, ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = [asyncio.create_task(worker(session)) for _ in range(CONNECTIONS)]
        await asyncio.gather(*tasks)

asyncio.run(main())
