import csv
from py_nuban import get_possible_banks

with open("dataset.csv", "r") as f:
    reader = csv.reader(f)
    success_matches = 0
    failed_matches = 0
    failed_data = set()
    for idx,row in enumerate(reader):
        if idx == 0: # Skips over the first row as it should be the header
            continue
        account_number = row[0]
        bank_code = row[1]
        possible_banks = get_possible_banks(account_number)
        # shape of possible_banks -> [(bank_code,bank_name)]
        found = False
        for possible_bank in possible_banks:
            if possible_bank[0] == bank_code: # Looking for a match
                success_matches += 1
                found = True
                break
        if found:
            continue
        failed_matches += 1
        failed_data.add((account_number,bank_code)) # Aggregate account numbers that failed to find a match

    # REPORT GENERATION  
    print(f"Total number of demo data: {success_matches+failed_matches}")
    print(f"Number of successful matches: {success_matches}")
    print(f"Number of failed matches: {failed_matches}")
    if failed_data:
        print("Bank code and account numbers that didn't produce a match")
        print(failed_data)