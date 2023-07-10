import tabula
# from tabulate import tabulate
import io
import logging
import argparse
import datetime

#For SCB
import scb_parser

#For MoneyWiz
import webbrowser
import moneywiz_url_parser

# Logger Setup
logging.basicConfig(format='%(levelname)s %(filename)s:%(lineno)s : %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Arg Setup
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description="Generate cost and usage report for the last 3 month grouped by service")

parser.add_argument('--infile', type=str, default=f'./data/AcctSt.pdf', help="Input file name")
parser.add_argument('--outfile', type=str, default=f'./data/acc_bnk_pst-{datetime.date.today()}.csv', help="Output file name")
parser.add_argument('--password', type=str, default="XXXXXXX", help="PDF File Password")
parser.add_argument('--account', type=str, default="TEST", help="MoneyWiz Account Name")
parser.add_argument('--currency', type=str, default="THB", help="MoneyWiz Currency")
parser.add_argument('--save' , action="store_true", help="Save MoneyWiz Transaction")
parser.add_argument('--debug', action="store_true", help="Print debug info")
args = parser.parse_args()

if args.debug:
    logger.setLevel(logging.DEBUG)

report_file_name = args.outfile

# Read PDF file
source = tabula.read_pdf(args.infile, pages="all" , password=args.password, guess=False, stream=True, multiple_tables=True, pandas_options={'header': None})

# Parse SCB Transactions
scb_parsed_transaction_data = scb_parser.parse_transations(source=source)
total = scb_parser.get_total(source=source)
is_amounts_verified = scb_parser.verify_amounts(scb_parsed_transaction_data, total)

if not is_amounts_verified:
    logger.error("Total amount is not equal to sum of transactions")
    exit(1)


# After we have to export it to CSV or try to execute MoneyWiz import URLs
# We have some succcess with MoneyWiz URLs. Code below just works. We need another attemt to make it done.

# Preprocess moneywiz_data using a list comprehension
preprocessed_data_for_moneywiz = [
    {
        "account": args.account,
        "amount": row["Amount"],
        "currency": args.currency,
        "date": row["Date"] + " " + row["Time"],
        "payee": row["Description"],
        "memo": row["Notes"] + " Code:" + row["Code/Channel"],
        "save": args.save
    }
    for _, row in scb_parsed_transaction_data.iterrows()
]

# Process the preprocessed_data using get_moneywiz_url
moneywiz_urls = [
    moneywiz_url_parser.get_moneywiz_url(
        data["account"],
        data["amount"],
        data["currency"],
        data["date"],
        payee=data["payee"],
        memo=data["memo"],
        save=data["save"]
    )
    for data in preprocessed_data_for_moneywiz
]

for url in moneywiz_urls:
    logger.debug(url)
    webbrowser.open(url)

