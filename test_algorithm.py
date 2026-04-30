import banks
import os
from dotenv import load_dotenv

load_dotenv()
def get_possible_banks(account_no):
    print("Account number for check: ",account_no)
    banks_names = []
    if len(account_no) != 10:
        print("Number must be 10 digits")
        return None
    check_digit = account_no[-1]
    serial_number = account_no[:-1]
    possible_codes =get_list_of_possible_codes(serial_number, check_digit)
    for code in possible_codes:
        banks_names.append(get_bank_name_from_code(code))
    print("**********POSSIBLE BANKS**********")
    for name in banks_names:
        print(name)

    print("Number of banks found: ",len(banks_names))

def get_bank_name_from_code(code):
    for bank in banks.banks:
        if code == bank["code"]:
            return bank["name"]

def get_list_of_possible_codes(serial_number, check_digit):
    list_of_possible_codes = []
    weights = [3,7,3,3,7,3,3,7,3,3,7,3,3,7,3]
    codes_list = get_all_normalized_bank_codes()
    for code_dict in codes_list:
        sum = 0
        full_check = list(code_dict["normalized"]+serial_number)
        if len(full_check) != 15:
            print("The full check is not 15 digits")
            raise Exception
        for idx,weight in enumerate(weights):
            sum = weight*int(full_check[idx]) + sum
        if sum%10 == 0:
            modul = 0
        else:
            modul = 10 - sum%10
        
        if str(modul) == check_digit:
            list_of_possible_codes.append(code_dict["code"])
    return list_of_possible_codes

def get_all_normalized_bank_codes():
    list_of_all_codes = []
    for bank in banks.banks:
        if len(bank["code"]) == 3:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": "000"+bank["code"]
                }
            )
        elif len(bank["code"]) == 5:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": "9"+bank["code"]
                }
            )
        elif len(bank["code"]) == 6:
            list_of_all_codes.append(
                {
                "code":bank["code"],
                "normalized": bank["code"]
                }
            )
        else:
            print("Not a valid bank code")

    return list_of_all_codes


TEST_ACCOUNT_NUMBERS = os.getenv("TEST_ACCOUNT_NUMBERS","1901880678").split(",")

for account_no in TEST_ACCOUNT_NUMBERS:
    get_possible_banks(account_no.strip())
    print("\n\n\n\n\n\n")

print("Amount of work done: ",len(TEST_ACCOUNT_NUMBERS))
