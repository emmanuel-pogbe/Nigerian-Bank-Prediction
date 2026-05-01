v1.
Most banks have 6 digit codes or 3 digit codes
2 Nigerian banks have 5 digit codes
50211 - Kuda Micro-finance Bank
50304 - Mint-Finex Micro-finance Bank

Old algorithm skips over non-3 digit code banks

New algorithm works with all bank codes:
CBN 16 digit format:
Positions 1–6 (ABCDEF): Bank identifier (6 digits)
Positions 7–15 (GHIJKLMNO): 9-digit account serial number
Position 16 (P): Check digit

Weights to use -> [3,7,3,3,7,3,3,7,3,3,7,3,3,7,3]

Some microfinance banks don't comply
Moniepoint doesn't work with this algorithm for some reason

for 5 different Kuda account numbers, a match was produced - so it's safe to say that Kuda might be compliant
Opay and Palmpay aren't compliant - I'm pretty sure it's because they just strip off the leading 0 of a phone number and call that an account number, that's going to give this algorithm some problems


v2.
Wrote a looks_like_phone_number() function that takes into account the most popular banks that use phone numbers as account numbers
Next: looking to give a popularity index to all banks in the banks list, which can be used as a probabilistic measure to rank the banks and pick 3-5 possible matches for a given account number