#/bin/bash

# Get PASSWORD from command line
PASSWORD=$1
# Get ACCOUNT from command line
ACCOUNT=$2

# Proccess all .pdf files in the data folder
for file in ./data/*.pdf
do
    # Get the filename without the extension
    filename=$(basename -- "$file")
    filename="${filename%.*}"
    # Run the main.py script with the password and account
    python main.py --password $PASSWORD --infile $file --account $ACCOUNT --csv --debug --outfile ./data/$filename.csv
done
