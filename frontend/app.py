import logging
import py_nuban
from flask import Flask, render_template, request

app = Flask(__name__)

logger = logging.getLogger(__name__)

# Check ../demo/test_algorithm.py
WEIGHTS = [3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3, 3, 7, 3]


def normalize_code(code: str) -> str:
    """
    Convert a bank code to its 6-digit normalized form.
    - 3-digit code  → "000" + code
    - 5-digit code  → "9" + code
    - 6-digit code  → code as-is
    - Any other length → log a warning and return None
    """
    if len(code) == 3:
        return "000" + code
    elif len(code) == 5:
        return "9" + code
    elif len(code) == 6:
        return code
    else:
        logger.warning("normalize_code: unexpected code length %d for code %r", len(code), code)
        return None


def build_check_string(normalized_code: str, serial_number: str) -> str:
    """
    Concatenate the 6-digit normalized code with the 9-digit serial number
    to produce the 15-character string used in the checksum calculation.
    """
    return normalized_code + serial_number


def compute_products(check_string: str) -> list:
    """
    Multiply each character of the 15-char check string by the corresponding
    weight in WEIGHTS. Returns a list of 15 integers.
    """
    return [int(ch) * w for ch, w in zip(check_string, WEIGHTS)]


def compute_weighted_sum(products: list) -> int:
    """Sum all 15 products."""
    return sum(products)


def compute_checksum(weighted_sum: int) -> int:
    """
    Return 10 - (weighted_sum % 10), or 0 if weighted_sum % 10 == 0.
    """
    remainder = weighted_sum % 10
    return 0 if remainder == 0 else 10 - remainder


def build_explainer(bank_code: str, bank_name: str, account_number: str) -> dict:
    """
    Build the full explainer data dict for one bank.
    Returns a dict with keys: bank_name, bank_code, normalized_code, check_string,
    digits (list of 15 chars), weights (list of 15 ints), products (list of 15 ints),
    weighted_sum (int), checksum (int), check_digit (str), match (bool).
    """
    serial_number = account_number[:9]
    check_digit = account_number[-1]

    normalized_code = normalize_code(bank_code)
    check_string = build_check_string(normalized_code, serial_number)
    products = compute_products(check_string)
    weighted_sum = compute_weighted_sum(products)
    checksum = compute_checksum(weighted_sum)
    return {
        "bank_name": bank_name,
        "bank_code": bank_code,
        "normalized_code": normalized_code,
        "check_string": check_string,
        "digits": list(check_string),
        "weights": WEIGHTS,
        "products": products,
        "weighted_sum": weighted_sum,
        "checksum": checksum,
        "check_digit": int(check_digit),
        "match": checksum == int(check_digit)
    }


@app.route("/", methods=["GET", "POST"])
def index():
    """
    GET:  Render the empty form.
    POST: Validate input, run algorithm, build explainer data, render results.
    """
    account_number = ""
    error = None
    all_banks = []
    nuban_banks = []
    heuristics_banks = []
    no_results = False

    if request.method == "POST":
        account_number = request.form.get("account_number", "")

        if len(account_number) != 10:
            error = "Account number must be exactly 10 digits."
        elif not account_number.isdigit():
            error = "Account number must contain digits only."

        if error is None:
            try:
                results = py_nuban.get_possible_banks(account_number)
            except Exception as exc:
                logger.error("py_nuban.get_possible_banks raised an exception: %s", exc, exc_info=True)
                error = "An unkown error occurred while processing the account number. Please try again."
                results = None

            if results is not None:
                if len(results) == 0:
                    no_results = True
                else:
                    for bank_code, bank_name in results:
                        explainer_dict = build_explainer(bank_code, bank_name, account_number)
                        all_banks.append(explainer_dict)
                        if explainer_dict.get("match"):
                            nuban_banks.append(explainer_dict)
                        else:
                            heuristics_banks.append(explainer_dict)
    return render_template(
        "index.html",
        account_number=account_number,
        error=error,
        all_banks=all_banks,
        nuban_banks=nuban_banks,
        heuristics_banks=heuristics_banks,
        no_results=no_results,
    )


if __name__ == "__main__":
    app.run(debug=True)
