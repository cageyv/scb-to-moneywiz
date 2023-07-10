#!/usr/bin/env bash

source env/bin/activate
python3 main.py acc_bnk_pst_pdf.pdf
python3 main.py --password XXXXXX --account TEST --infile ./data/AcctSt_Jul23.pdf --save --debug