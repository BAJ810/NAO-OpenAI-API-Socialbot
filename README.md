# NAO-OpenAI-API-Socialbot

This is a program that allows the NAO robot to connect to OpenAI API. It allows you to chat with the robot using a external microphone. To run it requires 2 scripts for the OpenAI API and the NAOqi SDK. It uses MQTT to communicate between the scripts.

## NAOqi Setup
### Installing Python 2.7
If you already have python 2.7 installed and have python exe in your path then you can skip to Installing NAOqi
You can download Python 2.7 at https://www.python.org/downloads/release/python-2718/
Once downloaded use the .msi installer to install.
IMPORTANT: while installing Python 2.7 when you get to the Customise Python 2.7.18 page make sure “Add python.exe to Path is set to “Will be installed on local hard drive"
### Installing NAOqi
You can download NAOqi from https://support.aldebaran.com/support/solutions/articles/80001033994-nao-v4-v5-naoqi-2-1-4-13- or https://www.aldebaran.com/en/support/nao-6/downloads-softwares 
Once downloaded, add a folder to a safe place on your computer which does not require admin privileges. 
Then open “Edit the system environment variables” and click “Environment Variables” and add a new user variable called “PYTHONPATH” with a value of the path to the “lib” folder in the NAOqi folder e.g. “C:\naoqi\lib”

### Using NAOqi
You must use Python 2 (2.7) when using NAOqi. NAOqi will not work with Python 3+.
YouTube or ChatGPT can be useful to learn Python or NAOqi
NAOqi works with many programming languages such as C++ and Java, but Python is the easiest to use and setup. 
This website is extremely useful when finding API modules: http://doc.aldebaran.com/1-14/naoqi/index.html 
