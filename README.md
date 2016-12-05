# ClassMood

# Version 1.0 Release Notes:
- New Features:
  - Question Presentation: Professors can now control the presentation of polling questions using the live view UI.
  - Question Answering: Students can now respond to polling questions using the live view UI.
  - Gauge Reset: Professors can now reset gauge responses to 'Good' for depth and pace during the course of a live lecture.
- Bug Fixes:
  - Multiple users can now log in to the application at the same time without error.
  - Classes, lectures, and polling questions can now be deleted using the UI.
  - Date of lecture creation has been added to lecture list to avoid confusion.
- Known Bugs:
  - New Google users are defaulted to students. Professors must be manually entered into the database.
  - Students are removed from the live lecture quite a bit after it has ended.

# **Install Guide**

### **Prerequisites**

Ensure that python 2.7 is installed. If not download from https://www.python.org/downloads/ and install the appropriate file for your OS. Also ensure that Git is installed.

### **Dependent Libraries**

Install [NodeJS](https://nodejs.org/en/)  and then [Typescript](http://www.typescriptlang.org/)

### **Download Instructions**

Open terminal and run `git clone https://github.com/goutamvenkat/ClassMood.git ` 

### **Build Instructions**

Using the terminal, first cd into the ClassMood directory. To ensure everything is installed, run the command `pip install -r requirements.txt`. You only to run this once to install all the necessary python libraries. 

### **Run Instructions**

Then run the command `python runserver.py`. Go to the browser and visit http://localhost:5000 Troubleshooting: The most common error during installation is that a python library is not installed. If that is the case then simply run `pip install <that library>`. If you do not pip or the python package manager then follow these instructions to get it.


