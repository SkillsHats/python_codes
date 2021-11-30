import argparse


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Calculate EMI."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-p', '--principle', type=float, help='Principle amount', required=True)
    parser.add_argument('-r', '--rate', type=float, help='Rate of interest return', required=True)
    parser.add_argument('-t', '--time', type=int, help='Time period of invesment (in years)', required=True)
    return parser


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


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    p = args.principle
    r = args.rate # percentage
    t = args.time # in years

    emi_amount = calculate_emi(p, r, t) 
    payable_amount = round(emi_amount * t * 12)
    interest_amount = round(payable_amount - p)

    print("Total Amount payable: ", payable_amount)
    print("Total Interest: ", interest_amount)
    print("Monthly EMI:  ", emi_amount)
