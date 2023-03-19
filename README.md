# moneywiz-scb-pdf-to-cvs
Conversion from PDF to CVS for SCB Bank

## Dependency
`brew install java`

## How to get PDF file (option 1)
- Open SCB Easy Net: https://www.scbeasy.com/
- Go to My Account -> Select Account -> Historical Statement -> Select Month -> Click "Print" (bottom) -> Save file as is PDF 

## How to get PDF file (option 2)
- Open SCB Easy mobile app
- Go to Bank Services -> Account Summary -> Select account and click "Tap to view more details" -> "More Services" -> Request Statement -> Select range -> Check Mail Box 

## How to run
`python3 main.py --infile='./data/acc_bnk_pst_pdf_mar2023.pdf' --outfile='mar2023.csv'`
