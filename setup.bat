:: This batch file installs the dependencies for the project
ECHO OFF
:: Update PIP
call py -m pip install --upgrade pip
:: Install win32com
call py -m pip install pywin32
:: Install Pandas
call py -m pip install pandas
:: Install openpyxl
call py -m pip install openpyxl
:: Install xlrd
call py -m pip install xlrd
:: Install tqdm
call py -m pip install tqdm