import argparse
from decimal import Decimal


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Calculate compound interest (INR)."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-p', '--principle', type=float, help='Principle amount', required=True)
    parser.add_argument('-r', '--rate', type=float, help='Rate of interest return', required=True)
    parser.add_argument('-t', '--time', type=float, help='Time period of invesment (in years)', required=True)
    return parser


def compound_interest(principle: Decimal, rate: float, time: float) -> Decimal:
    """ Calculate Compound Interest (INR)
    
    Args:
        principle: Principle Amount or Invested Amount
        rate: Rate of Interest
        time: Invested time period (in years)
    
    Return:
        Total Amount Interest
    """

    final = principle * ( pow((1 + (rate / 100.0 )), time ))
    return final



def simple_interest(principle: Decimal, rate: float, time: float) -> Decimal:
    """ Calculate Simple Interest (INR)
    
    Args:
        principle: Principle Amount or Invested Amount
        rate: Rate of Interest
        time: Invested time period (in years)
    
    Return:
        Total Amount Interest
    """

    final = (principle * time * rate ) / 100
    return final


if __name__ == '__main__':
    parser = init_argparse()
    args = parser.parse_args()

    p = args.principle
    r = args.rate
    t = args.time

    final = compound_interest(p, r, t)
    interest = simple_interest(p, r, t)
    print("Final Amount: ", final)
    print("Interest Amount: ", interest)