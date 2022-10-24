# File: combineCsv.py
# Author: Dennis Kovarik
# Description:
#   Combines multiple files downloaded from iCIMS into one csv file.
# Usage:
#   py combineCsv.py -indir inputDir -outcsv outCsvFile
#   py combineCsv.py -indir inputDir -outcsv outCsvFile -group_by group_by_field

import os, sys
import pandas as pd
from utils import *
import shutil
import math

 
# Parse cmd args 
args = parseCmdArgs()

# Concatinate .xlsx files
df = combineFiles(args['-indir'], args)

#writeCsv(df, args['-outcsv'])

df.to_csv(args['-outcsv'], index=False)
#df.to_excel(args['-outcsv'], index=False)

#print(df)


# Delete files in temp dir
#deleteFiles(tempdir)
