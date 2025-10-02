# This script creates a Python 3.11 virtual environment and installs the Snowflake Snowpark package.

# check if python 3.11 is installed; download the recommended windows installer and install it (checking "Add PATH")
python --version

# check python 3.11 added to the current PATH
$env:PATH -split ';'

#use py launcher to launch the current version to 3.11
py -3.11 --version

# create a python 3.11 virtual env
python -m venv py311_env

# verify python version inside the virtual env
.\py311_env\Scripts\activate.bat
python --version

# check if current 
$env:VIRTUAL_ENV

# Install dependencies
# note: adding --user add the end to bypass the virtual env and install packages to %APPDATA%\Python\PythonXY\site-packages
pip3 install -r C:/repos/PHECDM/dep/requirements.txt

# check packages installed
python -m site

# check for a specific package
python -m pip show snowflake-snowpark-python