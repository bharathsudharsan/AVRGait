# AVRGait - Analyse, Visualise & Report Parameters during fitness activities. 

Run "python AVRGait_tkinter_UI.py" to open the AVRGait UI. 4 interactable buttons will appear.

1. When the Activity Level button is pressed from the UI, the pa.py code computes the Activity levels using the data from the .csv file.

2. When the Step Counter button from UI is pressed, train.py code will be executed. This code detects and counts the number of steps using data from the .csv files stored in the directory. The .csv files contain sensor readings from the wearable.

3. When the Cadence button from UI is pressed, the Cad.py code will be executed. This code computes and displays the number of steps per minute using the data from the .csv file.

4. When the Step Mean button from UI is pressed, Step_Mean.py code will be executed. This code computes the mean time between all steps
