:: This batch file installs the dependencies for the project
ECHO OFF
:: Update PIP
call py -m pip install --upgrade pip
:: Install Pandas
call py -m pip install pandas
