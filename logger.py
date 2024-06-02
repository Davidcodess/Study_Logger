import datetime
import json
import FreeSimpleGUI as sg
import os 

# Define the layout with input fields and buttons
current_time = datetime.datetime.now()

list_of_months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

current_hour = current_time.hour
current_minutes = current_time.minute
current_day = current_time.day 
current_month = current_time.month 
current_year = current_time.year

month = list_of_months[current_month - 1]

layout = [
    [sg.Text("Hello! This is your personal study log. Today is " + str(month) + " " + str(current_day) + ", " + str(current_year) + ".", justification='center', size=(80, 1))], 
    [sg.Text("What did you study today?", justification='left', size=(30, 1)), sg.InputText(key='-TOPIC-')],
    [sg.Text("Enter duration ( in hours):", justification='left', size=(30, 1)), sg.InputText(key='-DURATION-')],
    [sg.Button("Log Study"), sg.Button("Show Log"), sg.Button("Exit"),sg.Button("Total Time Spent Studying")],
    [sg.Text("Study Log:", size=(40, 1), justification='center')],
    [sg.Multiline(key='-LOG-', size=(50, 10), disabled=True)]
]

# Create the window
window = sg.Window("Study Logger", layout, size=(600, 300))

# JSON file to store logs
log_file = "study_log.json"

# Load existing logs from JSON file if it exists
if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
    try:
        with open(log_file, 'r') as file:
            study_log = json.load(file)
    except json.JSONDecodeError:
        study_log = []
        sg.popup("Error", "Failed to load logs. The JSON file might be corrupted.")
else:
    study_log = []

# Event loop to process button clicks
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Log Study":
        study_topic = values['-TOPIC-']
        study_duration = values['-DURATION-']
        if study_topic and study_duration:
            new_log_entry = f" ** You worked on: {study_topic} for {study_duration} hours on " + str(month) + " " + str(current_day) + " " + str(current_year) + "!"
            study_log.append(new_log_entry)
            # Save logs to JSON file
            with open(log_file, 'w') as file:
                json.dump(study_log, file)
            # Update the multiline element with the new log
            window['-LOG-'].update("\n".join(study_log))
        else:
            sg.popup("Please enter both a study topic and duration")

    if event == "Show Log":
        # Update the multiline element with the log
        window['-LOG-'].update("\n".join(study_log))

# Close the window
window.close()
