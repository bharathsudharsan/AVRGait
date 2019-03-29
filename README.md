# AVRGait

Python, Tkinter & sensormotion library based AVRGait - Aanalyse, Visualise & Report Parametersduring fitness activites. 

When the Activity Level button is pressed from UI the pa.py code to find the Activity levels using the Datasets which are obtained from the wearable will be executed.

When Step Counter button from UI is pressed train.py code will be executed. This code is used to detect and count the number of steps using data from the .csv files stored in the directory. The .csv files contains sensor readings from the wearable

When Cadence button from UI is pressed Cad.py code will be executed. This code is used to find out and display Number of steps per minute from the .csv file.

When Step Mean button from UI is pressed Step_Mean.py code will be executed. This code is used to find out and display Mean time between all steps

How to run:

Created a Virtual environment using python -m venv F:\Python_VENV\AVRGait 
& install necessary packages to run this Python and the Tkinter library based script.

Commands used to activate virt_env(Python_VENV) and run the UI from cmd 

F:

cd \Python_VENV\AVRGait\Scripts

.\activate

cd \AVRGait\Code

python AVRGait_tkinter_UI.py


Reference:
https://pypi.org/project/sensormotion/


