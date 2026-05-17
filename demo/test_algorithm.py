import banks
import os
from dotenv import load_dotenv
import helpers

load_dotenv()
def get_possible_banks(account_no):
    print("Account number for check: ",account_no)
    banks_names = []
    if len(account_no) != 10:
        print("Number must be 10 digits")
        return None
    # Check if account number looks like a phone number
    check_digit = account_no[-1]
    serial_number = account_no[:-1]
    possible_codes = get_set_of_possible_codes(serial_number, check_digit)
    
    # I suck at python - what is this logic
    if looks_like_phone_number(account_no):
        possible_codes.add("305") # Opay
        possible_codes.add("100033") # Palmpay
        possible_codes.add("090405") # Moniepoint 
    if not looks_like_phone_number(account_no):
        possible_codes.discard("305")
        possible_codes.discard("100033")
        possible_codes.discard("090405")

    if looks_like_moniepoint_number(account_no):
        possible_codes.add("090405")

    for code in possible_codes:
        bank_name_and_popularity = get_bank_name_and_popularity_from_code(code)
        popularity = int(bank_name_and_popularity[1])
        if popularity>8:
            banks_names.append((code,bank_name_and_popularity))
    banks_names.sort(key=sort_func,reverse=True)
    banks_names = banks_names[:6]
    return banks_names # ->shape -> [(code,[name,popularity])]

def sort_func(bank_code_and_name_and_popularity):
    return int(bank_code_and_name_and_popularity[1][1])

def get_bank_name_and_popularity_from_code(code):
    for bank in banks.banks:
        if code == bank["code"]:
            return [bank["name"],bank["popularity"]]

def looks_like_phone_number(account_no):
    starts = ["80","81","70","71","90","91"]
    return str(account_no[:2]) in starts

def looks_like_moniepoint_number(account_no):
    # I can't believe this is a separate function
    starts = ["4","5","6","8","9"]
    return str(account_no[:1]) in starts

def get_set_of_possible_codes(serial_number, check_digit):
    list_of_possible_codes = set()
    full_weights = [3,7,3,3,7,3,3,7,3,3,7,3,3,7,3]
    smaller_weights = [3,7,3,3,7,3,3,7,3,3,7,3]
    codes_list = get_all_normalized_bank_codes()
    for code_dict in codes_list:
        big_sum_of_weights = 0
        small_sum_of_weights = 0
        full_check = list(code_dict["normalized"]+serial_number)
        smaller_check = list(code_dict["code"]+serial_number) if len(code_dict["code"]) == 3 else None
        if len(full_check) != 15:
            print("The full check is not 15 digits")
            raise Exception
        for idx,weight in enumerate(full_weights):
            big_sum_of_weights = weight*int(full_check[idx]) + big_sum_of_weights
            if smaller_check and idx < 12:
                small_sum_of_weights = smaller_weights[idx]*int(smaller_check[idx]) + small_sum_of_weights
        big_module = (10 - big_sum_of_weights%10)%10
        small_module = (10-small_sum_of_weights%10)%10 if small_sum_of_weights else None
        if str(big_module) == check_digit:
            list_of_possible_codes.add(code_dict["code"])
        if small_module and str(small_module) == check_digit:
            list_of_possible_codes.add(code_dict["code"])
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


TEST_ACCOUNT_NUMBERS = os.getenv("TEST_ACCOUNT_NUMBERS","1901880678").split(",") # No longer in use
TUPLE_LIST_ACCOUNT_NUMBERS = helpers.parse_multiple_tuple_strings(os.getenv("TUPLE_LIST_ACCOUNT_NUMBERS"))


def main_with_account_numbers_list(): # Simpler testing version using TEST_ACCOUNT_NUMBERS variable
    
    for account_no in TEST_ACCOUNT_NUMBERS:
        get_possible_banks(account_no.strip())
        print("\n\n\n\n\n\n")


def main_with_tuple_list(): # More robust testing version using TUPLE_LIST_ACCOUNT_NUMBERS variable
    success_matches = 0
    failed_matches = 0
    failed_banks = set()
    total_list = []
    for account_number_with_bank_code in TUPLE_LIST_ACCOUNT_NUMBERS:
        possible_codes_with_bank_names_and_popularity = get_possible_banks(account_number_with_bank_code[0])
        total_list.append(len(possible_codes_with_bank_names_and_popularity))
        bank_code = account_number_with_bank_code[1]
        bank_name_and_popularity_from_code = get_bank_name_and_popularity_from_code(bank_code)
        if (bank_code,bank_name_and_popularity_from_code) in possible_codes_with_bank_names_and_popularity:
            print(f"Match was found for bank: {bank_name_and_popularity_from_code[0]}")
            success_matches += 1
        else:
            print(f"No match was found for bank: {bank_name_and_popularity_from_code[0]} account number: {account_number_with_bank_code[0]}")
            failed_matches += 1
            failed_banks.add(bank_name_and_popularity_from_code[0])
        print("\n\n\n\n\n\n\n")

    print("FINAL REPORT")
    print("Total number of demo data in tuple list: ",len(TUPLE_LIST_ACCOUNT_NUMBERS))
    print(f"Number of successful matches: {success_matches}")
    print(f"Number of failed matches: {failed_matches}")
    print(f"Failed banks: {failed_banks if failed_banks else 'None'}")
    print(f"Average number of possible banks: {sum(total_list)/len(total_list)}")

if __name__ == "__main__":
    # main_with_account_numbers_list()
    main_with_tuple_list()