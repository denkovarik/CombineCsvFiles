# File: utils.py
# Author: Dennis Kovarik
# Description:
#   Utilities file for the project

import os, sys
import pandas as pd
import win32com.client as win32
from tqdm import tqdm


def combineFiles(tempdir):
    """
    Combines all excel files in dir into one
    :param tempdir: Directory containing the excel files to combine
    """
    allDfs = []
    for i in tqdm(range(len(os.listdir(tempdir))), desc="Concatinating .xlsx files..."):
        f = os.listdir(tempdir)[i]
        fname = tempdir + '\\' + f
        df = pd.read_excel(fname)
        allDfs.append(df)
    outDf = pd.concat(allDfs)
    return outDf


def cnvrtFiles(dpath, tempdir):
    """
    Converts all .xls files in 'dpath' dir to .xlsx.
    :param dpath: Full path to the directory containing the files to convert
    :param tempdir: Full path the the temp dir
    """
    for i in tqdm(range(len(os.listdir(dpath))), desc="Converting files to .xlsx..."):
        f = os.listdir(dpath)[i]
        fname = dpath + f
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(fname)
        wb.SaveAs(tempdir + f + "x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
        wb.Close()                               #FileFormat = 56 is for .xls extension
        excel.Application.Quit()
        
        
def deleteFiles(dir):
    """
    Deletes all files in 'dir'
    :param dir: Directory to delete files in
    """
    for f in os.listdir(dir):
        os.remove(dir + f)


def displayUsage():
    """
    Displays the usage message for the program
    """
    usage = "Description:\n\tCombines multiple files downloaded from iCIMS "
    usage += "into one csv file.\n"
    usage += "Usage:\n\tpy combineCsv.py -indir inputDir -outcsv outCsvFile"
    print(usage)
    
    
def parseCmdArgs():
    """
    Parses and validates the cmd args.
    """
    # Help
    if '-h' in sys.argv or '-help' in sys.argv:
        displayUsage()
        exit()
    # Validate cmd args
    if len(sys.argv) != 5:
        print("Invalid number of command line arguments\n")
        displayUsage()
        exit()    
    if not '-indir' in sys.argv or not "-outcsv" in sys.argv:
        print("Invalid command line arguments\n")
        displayUsage()
        exit()
    # Parse the args
    args = {}
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-indir' and i + 1 < len(sys.argv):
            args[sys.argv[i]] = sys.argv[i+1]
            if not os.path.isdir(args[sys.argv[i]]):
                print(args[sys.argv[i]] + " does not exist\n")
                displayUsage()
                exit()  
        if sys.argv[i] == '-outcsv' and i + 1 < len(sys.argv):
            args[sys.argv[i]] = sys.argv[i+1]
    if not '-indir' in args.keys() or not '-outcsv' in args.keys():
        print("Invalid command line arguments\n")
        displayUsage()
        exit()
    if not args['-indir'][-1] == '\\':
        args['-indir'] += '\\'
    return args   

    
