# File: combineCsv.py
# Author: Dennis Kovarik
# Description:
#   Combines multiple files downloaded from iCIMS into one csv file.
# Usage:
#   py combineCsv.py -indir inputDir -outcsv outCsvFile

import os, sys
import pandas as pd
from utils import *
import shutil

 
# Parse cmd args 
args = parseCmdArgs()

# Create temp folder
if os.path.isdir('temp'):
    shutil.rmtree('temp')
os.mkdir('temp')

tempdir = os.getcwd() + '\\temp\\'

# Convert to .xlsx   
cnvrtFiles(args['-indir'], tempdir)
    
# Concatinate .xlsx files
df = combineFiles(tempdir)

df.to_csv(args['-outcsv'], index=False)
#df.to_excel(args['-outcsv'])

print(df)

# Delete files in temp dir
#deleteFiles(tempdir)
