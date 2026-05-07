from dotenv import load_dotenv
import os
import requests
import asyncio
import time

load_dotenv()

KORA_ACCOUNT_RESOLVE_URL = os.getenv("KORA_ACCOUNT_RESOLVE_URL")
def _sync_resolve_account(payload: dict):
    response = requests.post(
        KORA_ACCOUNT_RESOLVE_URL,
        data=payload,
    )
    response.raise_for_status()
    return response.json()

async def resolve_account(payload: dict):
    return await asyncio.to_thread(_sync_resolve_account, payload)

async def main():
    payload1 = {"account": "1901880678", "bank": "044"}
    payload2 = {"account": "0667563242", "bank": "058"}

    tasks = [
        asyncio.create_task(resolve_account(payload1)),
        asyncio.create_task(resolve_account(payload2)),
    ]

    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, res in enumerate(results, start=1):
        if isinstance(res, Exception):
            print(f"payload{i} error:", res)
        else:
            print(f"payload{i} result:", res)


if __name__ == "__main__": 
    start_time = time.perf_counter()
    asyncio.run(main())
    elapsed_time = time.perf_counter() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")
    


 