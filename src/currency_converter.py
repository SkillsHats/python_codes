import requests


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

    amount = 100
    from_curr = "INR"
    to_curr = "USD"
    
    converted_amount = converter.convert( from_curr, to_curr, amount )
    print(f"Convert Amount : ", converted_amount)