import argparse
import requests


def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] ...",
        description="Convert Currency"
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )
    parser.add_argument('-a', '--amount', type=float, help='Amount', required=True)
    parser.add_argument('-fc', '--from_cur', type=str, help='From Currency', required=False, default='INR')
    parser.add_argument('-tc', '--to_cur', type=str, help='To Currency', required=False, default='USD')
    return parser


class CurrencyConverter():
    def __init__(self, url: str):
        self.data = requests.get(url).json()
        self.currencies = self.data['rates']

    def perform(self, from_currency: str, to_currency: str, amount: float) -> float:
        """ Calculate amount if initial currency is not USD. """

        if from_currency != 'USD' : 
            amount = amount / self.currencies[from_currency] 
  
        # limiting the precision to 4 decimal places 
        amount = round(amount * self.currencies[to_currency], 4) 
        return amount

    def convert(self, from_curr: str, to_curr: str, amount: float) -> float:
        """ Convert Amount from one currency to another currency """ 
        
        converted_amount = self.perform(from_curr, to_curr, amount)
        converted_amount = round(converted_amount, 2)

        return converted_amount


if __name__ == '__main__':
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    converter = CurrencyConverter(url)

    parser = init_argparse()
    args = parser.parse_args()

    amount = args.amount
    from_curr = args.from_cur
    to_curr = args.to_cur
    
    converted_amount = converter.convert( from_curr, to_curr, amount )
    print(f"Convert Amount : ", converted_amount)