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

for 5 different Kuda account numbers, a match was produced - so it's safe to say that Kuda might be compliant with the NUBAN algorithm
Opay and Palmpay aren't compliant - I'm pretty sure it's because they just strip off the leading 0 of a phone number and call that an account number, that's going to give this algorithm some problems


v2.
Wrote a looks_like_phone_number() function that takes into account the most popular banks that use phone numbers as account numbers
Next: looking to give a popularity index to all banks in the banks list, which can be used as a probabilistic measure to rank the banks and pick 3-5 possible matches for a given account number

v3.
popularity index implemented -> every bank in banks.py now has a "popularity" field - Thank you Windsurf! Smaller, less popular micro-finance banks get a popularity of 1
more popular banks get a popularity of >8
for the resulting list of the NUBAN algorithm, any bank with a popularity less than 8 won't be appended to the resulting list, reducing average output from ~25 to ~3
Next: Try out parallel_processing.py on resulting list to get ~1 bank result
Then code cleanup and finalization, maybe make it into a module or an API idk