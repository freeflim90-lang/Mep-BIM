# Import the required libraries.
import os
import sys
import shutil
import time
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import psutil


# Function for checking if the required paths exist.
def paths_exist(*paths):
    """
    Check if any of the input paths are accessible.
    Quit if any of the paths are not accessible.
    Requires the os library to run.
    """
    for path in paths:
        if not os.path.exists(path):
            sys.exit("One or more of the paths does not exist")

# Paths to be checked.
path_bpas_logo = r'Z:\IT\Dynamo Packages\bpasLogo.gif'
path_dynamo_packages = r'Z:\IT\Dynamo Packages\2.13'

# Check if the paths exist.
try:
    paths_exist(path_bpas_logo, path_dynamo_packages)
    print("The paths exist")
except:
    print("The paths do not exist")
    quit()


# Function for checking if revit is running. Quit if running.
def programs_running(*programs):
    """
    Check if any of the input programs are running in the task manager.
    Quit if any of the input programs is found running.
    Requires the sys and psutil libraries to run.
    """
    running_processes = list(p.name() for p in psutil.process_iter())

    # Check if any of the input programs are in 'running_processes'.
    for program in programs:
        if program in running_processes:
            sys.exit("One or more of the programs was found running")

# Check if Revit is running.
try:
    programs_running('revit.exe', 'Revit.exe')
    print("Revit is not running")
except:
    print("Revit is running")
    quit()


# Class to create splash screen/loading window.
class LoadingScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(400, 450)
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.CustomizeWindowHint)

        # Create a vertical layout to hold the gif and label widgets
        self.layout = QVBoxLayout(self)

        # Add the gif widget.
        self.label_animation = QLabel(self)
        gif_file_path = r'Z:\IT\Dynamo Packages\bpasLogo.gif'
        self.movie = QMovie(gif_file_path)
        self.label_animation.setMovie(self.movie)
        self.layout.addWidget(self.label_animation)

        # Add greeting for user.
        self.greeting = QLabel(self)
        self.greeting.setText(f"Hello, {os.getlogin().title()}!")
        font = QFont()
        font.setFamily("Sans-Serif")
        font.setPointSize(13)
        self.greeting.setFont(font)
        self.layout.addWidget(self.greeting)

        # Add note that Dynamo packages are installing.
        self.package_run = QLabel(self)
        self.package_run.setText("Dynamo Packages Installing. Please wait."
        " Do NOT open Revit.")
        font2 = QFont()
        font2.setFamily("Sans-Serif")
        font2.setPointSize(8)
        self.package_run.setFont(font2)
        self.layout.addWidget(self.package_run)

        # Add note on when to proceed.
        self.proceed_text = QLabel(self)
        self.proceed_text.setText("Proceed when this window closes.")
        self.proceed_text.setFont(font2)
        self.layout.addWidget(self.proceed_text)

        # Animate the gif file.
        self.startAnimation()

        # Create and start a timer to call the run_code function repeatedly.
        self.timer = QTimer()
        self.timer.timeout.connect(self.run_code)
        self.timer.start(5000)  # Set the timer interval to 5000 milliseconds.

        self.show()

    def startAnimation(self):
        self.movie.start()

    def stopAnimation(self):
        self.movie.stop()
        self.close()

    # To run the code that copies all the dynamo package files.
    def run_code(self):
        # Target directory for the dynamo packages.
        # Combine the c: drive user folder path with the target directory path end.
        begDir = os.path.expanduser('~')
        endDir = 'AppData/Roaming/Dynamo/Dynamo Revit/2.13'
        target_dir = os.path.join(begDir,endDir)
        print(target_dir)

        # Source directory for the dynamo packages on the server
        source_dir = r'Z:\IT\Dynamo Packages\2.13'

        # Get all file names in the source directory
        fileNames = os.listdir(source_dir)
        print(fileNames)

        # While loop to ensure that the directories are accessible while
        # the files are being copied. In case of load shedding/internet cuts.
        # Stops copying if the directory is not found.
        directories_accessible = True
        while directories_accessible:
            if not os.path.exists(source_dir):
                print('Directory no longer accessible')
                directories_accessible = False
            else:
                # Check if the target directory exists.
                if not os.path.exists(target_dir):
                    # Copy the dynamo package folder if the folder
                    #does not exist at the target path.
                    shutil.copytree(source_dir, target_dir)
                else:
                    # Check if the source directory has been modified more
                    # recently than the target directory.
                    print(os.path.exists(source_dir) and os.path.getmtime \
                    (source_dir) > os.path.getmtime(target_dir))
                    if os.path.exists(source_dir) and os.path.getmtime \
                    (source_dir) > os.path.getmtime(target_dir):

                        # Delete target directory if it exists.
                        if os.path.exists(target_dir):
                            # Delete file.
                            if os.path.isfile(target_dir):
                                os.remove(target_dir)
                            # Delete directory.
                            else:
                                shutil.rmtree(target_dir)

                        shutil.copytree(source_dir, target_dir)

                    else:
                        quit()


        # Stop the timer and close the splash screen when
        # the code finishes running.
        self.timer.stop()
        self.stopAnimation()

if __name__=='__main__':
    app = QApplication(sys.argv)

    splash_screen = LoadingScreen()

    app.quit()
    sys.exit(app.exec_())
