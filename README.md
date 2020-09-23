# AVRGait - Analyse, Visualise & Report Parameters during fitness activities. 

Run "python AVRGait_tkinter_UI.py", a UI will appear with 4 interactable buttons.

1. When the Activity Level button is pressed from UI, the pa.py code to find the Activity levels using the Datasets which are obtained from the wearable will be executed.

2. When the Step Counter button from UI is pressed, train.py code will be executed. This code is used to detect and count the number of steps using data from the .csv files stored in the directory. The .csv files contain sensor readings from the wearable

3. When the Cadence button from UI is pressed, the Cad.py code will be executed. This code is used to find out and display the number of steps per minute from the .csv file.

4. When the Step Mean button from UI is pressed, Step_Mean.py code will be executed. This code is used to find out and display the mean time between all steps
