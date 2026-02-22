Symboly:

Author: Harini Anantoji & Taylor Woods

Creating a web extension for videos calls to understand how engaged your audience is based on their micro expressions.

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
