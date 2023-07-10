# scb-to-moneywiz
Conversion from SCB Easy App Statement to MoneyWiz app

## Dependency
`brew install java`

<!-- The Old Way :( 
## How to get PDF file (option 1)
- Open SCB Easy Net: https://www.scbeasy.com/
- Go to My Account -> Select Account -> Historical Statement -> Select Month -> Click "Print" (bottom) -> Save file as is PDF  
-->

## How to get PDF file
- Open SCB Easy mobile app
- Go to Bank Services -> Account Summary -> Select account and click "Tap to view more details" -> "More Services" -> Request Statement -> Select range -> Check Mail Box 

## How to use 
### MoneyWiz URL Scheme
`python3 main.py --password XXXXXX --account TEST --infile ./data/AcctSt_Jul23.pdf --save --debug'`

### CSV file
`python3 main.py --password XXXXXX --account TEST --infile ./data/AcctSt_Jul23.pdf --csv --debug'`

## MoneyWiz info
https://help.wiz.money/en/articles/4525440-automate-transaction-management-with-url-schemas 

```
account (required) - the name of the account without spaces. For example "John CHASE Savings" would be "JohnCHASESavings".
amount (required) - use dot as decimal separator.
currency (optional) - enter desired currency code, such as USD, GBP, EUR, etc.
payee (optional)- the name of the payee, use %20 as whitespace separator. If the payee doesn't exist, it will be created.
category  (optional) - the hierarchy should be described by slashes. Whitespaces escaped by %20. For example: Dining%20Out/Restaurants
description (optional) - whitespaces escaped by %20
memo (optional) - whitespaces escaped by %20
tags (optional) - whitespaces escaped by %20. Multiple tags divided by comma. 
date (optional) - format yyyy-MM-dd HH:mm:ss 
save (optional) - default value is false. Set to true for MoneyWiz to directly save the transaction. Set to false for MoneyWiz to open the transaction entry screen with all the data pre-entered.
```