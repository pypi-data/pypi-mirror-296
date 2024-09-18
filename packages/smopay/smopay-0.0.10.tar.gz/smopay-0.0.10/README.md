# SMO Pay

> Note: `Test push for Version 0.0.10`.

## Technology

- Python 3.9.15

## Payment Options

- Xendit Credit Card

## Sample Credit Card Charging

```
from smopay.card import Card

card = Card()

card.ref_id = "..."
card.token_id = "..."
card.authentication_id = "..."
card.amount = "..."

response = card.charge()

print(response)
```