# File: utils.py
# Author: Dennis Kovarik
# Description:
#   Utilities file for the project

import os, sys
import pandas as pd
import win32com.client as win32
from tqdm import tqdm


def combineFiles(dir, args):
    """
    Combines all excel files in dir into one
    :param dir: Directory containing the excel files to combine
    :param args: A dictionary of command line arguments
    """
    allDfs = []
    fileType = 'csv'
    files = grabFileType(dir, fileType)
    
    for i in tqdm(range(len(files)), desc="Concatinating .xlsx files..."):
        f = files[i]
        fname = dir + '\\' + f
        if fname.split(".")[-1] == fileType:
            df = pd.read_csv(fname)
            #allDfs.append(df.drop_duplicates())
            allDfs.append(df)

    outDf = pd.concat(allDfs)
    #outDf.drop_duplicates()
    return outDf
    


def cnvrtFiles(dpath, outdir):
    """
    Converts all .xls files in 'dpath' dir to .xlsx.
    :param dpath: Full path to the directory containing the files to convert
    :param outdir: Full path the the out dir
    """
    files = os.listdir(dpath)
    xls_files = []
    # Grab just the '.xls' files
    for i in range(len(files)):
        filename = files[i][:files[i].rfind('.')]
        if files[i].split('.')[-1] == 'xls' and filename + '.xlsx' not in files:
            xls_files.append(files[i])
    # Now convert the files
    for i in tqdm(range(len(xls_files)), desc="Converting files to .xlsx..."):
        f = xls_files[i]
        fname = dpath + f
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        wb = excel.Workbooks.Open(fname)
        wb.SaveAs(outdir + f + "x", FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
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
    
    
def grabFileType(dirpath, ext):
    """
    Just creates a list of files with a specified ext and returns them as a 
    list of strings.
    
    :param dirpath: The target directory path
    :param ext: The filetype of interest
    :return: List of filenames that have a certain extension defined by the 
             'ext' param
    """
    allFiles = os.listdir(dirpath)
    files = []
    # Grab the right file extensions
    for i in range(len(allFiles)):
        filename = allFiles[i][:allFiles[i].rfind('.')]
        if allFiles[i].split('.')[-1] == ext:
            files.append(allFiles[i])
    return files
    
    
def parseCmdArgs():
    """
    Parses and validates the cmd args.
    """
    # Help
    if '-h' in sys.argv or '-help' in sys.argv:
        displayUsage()
        exit()
    # Validate cmd args
    if len(sys.argv) < 5 or len(sys.argv) > 7:
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

    
def writeCsv(df, filename):
    """
    Writes pandas dataframe to a .csv file
    :param df: Pandas dataframe to write to csv
    :param filename: The filename of the panda's dataframe
    """
    headers = df.columns.tolist()
    data = [headers] + df.to_numpy().tolist()

    csv = open(filename, "w+")
    err = open('errors.txt', "w+") 
    for row in data:
        l = list(row)
        for i in range(len(l)):
            cell = str(l[i]).strip()
            for c in cell:
                c2w = c
             
                try:
                    csv.write(c2w)
                except:
                    #print("Error writing ' " + str(c2w) + "' in '" + cell + "'")
                    #print(c2w.encode("utf-8"))
                    #print(chr(ord(c2w)))
                    #print(row)
                    #print("") 
                    #err.write('#' + "Error writing ' " + cell + "' in " + row)
                    #err.write(chr(ord('\u045b')))
                    #err.write("elif c2w == '" + str(c2w.encode("utf-8")) + "':\n")
                    #err.write("    c2w = ''\n")
                    csv.write('?')
            if i < len(l) - 1:
                csv.write(',')
        csv.write('\n')

    ## close the csv file
    csv.close()
    err.close()
