def calculate_emi(principal: float, rate: float, time: int) -> int: 
    """ Calculate monthly EMI based on the initial principal.
    Parameter:
    ----------
        principal: float
            Loanable initial principal amount.
        rate: float
            Interest rate in yearly percentage
        time: int
            Total tenurs years        

    Return:
    -------
        Calculated monthyl EMI.
    """
    
    rate = rate / (12 * 100) 
    time = time * 12 
    emi = round((principal * rate * pow(1 + rate, time)) / (pow(1 + rate, time) - 1))
    return emi 


principal = 10000.10; 
rate = 12.7;  # percentage
time = 3;  # in years

emi_amount = calculate_emi(principal, rate, time) 
payable_amount = round(emi_amount * time * 12)
interest_amount = round(payable_amount - principal)

print("Total Amount payable: ", payable_amount)
print("Total Interest: ", interest_amount)
print("Monthly EMI:  ", emi_amount)
