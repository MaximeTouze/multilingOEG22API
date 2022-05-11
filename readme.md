For setup ::
Requirement :

  Python >= 3.7

  Microsoft Visual C++ > 1.14.0 : https://visualstudio.microsoft.com/fr/visual-cpp-build-tools/

Windows : lauch setup.ps1

else :

py -m venv env

env\Scripts\activate

pip install -r requirements.txt

For lunching ::

Windows : launch run.ps1

else :

env\Scripts\activate

set FLASK_APP=app.py

flask run
