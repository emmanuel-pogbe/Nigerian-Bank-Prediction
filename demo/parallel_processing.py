from dotenv import load_dotenv
import os
import requests
import asyncio
import time

import test_algorithm

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
    account_number = input("Enter account number: ")
    start_time = time.perf_counter()
    possible = test_algorithm.get_possible_banks(account_number) #shape -> [(code,[name,popularity])]
    tasks = []
    for code,_ in possible:
        payload = {"account": account_number, "bank": code}
        tasks.append(resolve_account(payload))

    results = await asyncio.gather(*tasks, return_exceptions=True)
    calls = 0
    for res in results:
        if isinstance(res, Exception):
            continue
        else:
            bank_data = res.get("data")
            calls +=1
            print(f"\nBank name: {bank_data['bank_name']} | Bank code: {bank_data['bank_code']} | Bank name: {bank_data['account_name']}\n")
    if calls ==0:
        print("No bank was found")
    print("Number of API calls made: ",len(results))

    elapsed_time = time.perf_counter() - start_time
    print(f"Execution time: {elapsed_time:.2f} seconds")

if __name__ == "__main__": 
    asyncio.run(main())