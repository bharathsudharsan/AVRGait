# AVRGait - Analyse, Visualise & Report Parameters during fitness activities. 

Initially run the AVRGait_tkinter_UI.py script using "python AVRGait_tkinter_UI.py"

When the Activity Level button is pressed from UI, the pa.py code to find the Activity levels using the Datasets which are obtained from the wearable will be executed.

When the Step Counter button from UI is pressed, train.py code will be executed. This code is used to detect and count the number of steps using data from the .csv files stored in the directory. The .csv files contain sensor readings from the wearable

When the Cadence button from UI is pressed, the Cad.py code will be executed. This code is used to find out and display the number of steps per minute from the .csv file.

When the Step Mean button from UI is pressed, Step_Mean.py code will be executed. This code is used to find out and display the mean time between all steps

Install necessary packages to run this Python and the Tkinter library-based script, then

python AVRGait_tkinter_UI.py


Reference:
https://pypi.org/project/sensormotion/
