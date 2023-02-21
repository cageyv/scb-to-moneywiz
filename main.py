import tabula
# from tabulate import tabulate
# import pandas as pd
import io
import logging
import argparse
import datetime

# Logger Setup
logging.basicConfig(format='%(levelname)s %(filename)s:%(lineno)s : %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Arg Setup
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                 description="Generate cost and usage report for the last 3 month grouped by service")

parser.add_argument('--infile', type=str, default=f'./data/acc_bnk_pst_pdf.pdf', help="Input file name")
parser.add_argument('--outfile', type=str, default=f'./data/acc_bnk_pst-{datetime.date.today()}.csv', help="Output file name")
parser.add_argument('--debug', action="store_true", help="Print debug info")
args = parser.parse_args()

if args.debug:
    logger.setLevel(logging.DEBUG)

report_file_name = args.outfile

# Read PDF
# df = tabula.read_pdf(args.infile, pages="all" , 
#                          multiple_tables = True, stream = True)

# print(df)

# Convert
tabula.convert_into(args.infile, args.outfile, output_format="csv",  pages="all")


# # Transform the table into dataframe
# df = pd.read_fwf(io.StringIO(table))

# # Save the final result as csv file
# df.to_csv(".data/foo.cvs")
