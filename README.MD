# Introduction
pkill kills a process 
startmail kills a previous running version of outlook and starts it

## Creating the startmail binary
pyinstaller --onefile --icon=icon.ico startmail.py

## Setting up the shortcut running the command
Target: C:\Users\sebma\scripts\startmail.exe
Set to run Minimized
