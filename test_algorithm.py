import banks
def get_possible_banks(account_no):
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
    print("Serial number passed: ",serial_number)
    print("Check digit passed: ",check_digit)
    list_of_possible_codes = []
    weights = [3,7,3,3,7,3,3,7,3,3,7,3]
    codes_list = get_all_three_digit_codes()
    for code in codes_list:
        sum = 0
        full_check = list(code+serial_number)
        if len(full_check) != 12:
            print("THe full check is not 12 digits")
            return None
        for i,weight in enumerate(weights):
            sum = weight*int(full_check[i]) + sum
        if sum%10 == 0:
            modul = 0
        else:
            modul = 10 - sum%10
        
        if str(modul) == check_digit:
            list_of_possible_codes.append(code)
    return list_of_possible_codes

def get_all_three_digit_codes():
    list_of_codes = []
    for bank in banks.banks:
        if len(bank["code"]) == 3:
            list_of_codes.append(bank["code"])
    return list_of_codes


get_possible_banks("0667563242")
get_possible_banks("1901880678")