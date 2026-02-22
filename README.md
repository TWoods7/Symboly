Symboly:

Author: Harini Anantoji & Taylor Woods

Description: A web extension for videos calls to understand how engaged your audience is based on their micro expressions.

Extension Input:

    Button Click which starts taking screenshots

Process:

    Feed screenshots to AI

    Use AI to detect the level of engagement based on a screenshot every 3 seconds

    Turn those engagement levels into a line graph that updates every 3 seconds

Extension Output:

    Overlay outputs the graph

When program ends, screenshots, logs, and a final screenshot of the graph are downloaded.

TECH STACK

    IDE: VS Code

    Language: Python

    AI: Google’s MediaPipe Face Landmaker

    GenAI: Google Gemini, ChatGPT

Python Libraries:

    MediaPipe: AI that tracks eye and mouth movements

    OpenCV – Python: Image Processor (Turns image into AI understandable language)

    Numpy: Math Engine ( Calculates distance between landmarks for score)

    PyAutoGUI: Screenshots monitor every 3 seconds

    Dash: Hosts live graph as local website

    Pandas: Reads logs and created session averages

    Plotly: Creates the graph

    PyQt6: Creates transparent window for graph

    PyQt – web engine: Display graph inside window

Python Script Files:

    Start.py - Runs all the files in order

    Record.py - Takes screenshots of your application every 3 seconds

    Emotion.py - Gathers facial expressions and generates an engagement score from 1-10

    Data.py - Logs the score and time in logs

    Graph.py - Creates a graph based on the scores presented every 3 seconds

    Overlay.py - Creates a popup window that holds the graph.

Other Files and Folders:

    face_landmarker.task - A machine learning solution that detects 3D facial features.

    Screenshots – A folder that holds all screenshots taken by the program

    Data_logs – A folder that holds the logs with timestamps and scores each session

    Graphs – The end graph that gets uploaded after each session.

HOW TO RUN:
    //Have access to python 3.14 or a virtual machine in VScode that can run python
    //For full fearute capability have access to either a camera that is pluged in or the built-in webcam.
    //Run the start.py

