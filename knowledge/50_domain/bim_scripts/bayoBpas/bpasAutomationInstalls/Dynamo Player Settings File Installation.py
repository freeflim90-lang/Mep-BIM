# Import the required libraries.
import os
import shutil
import time
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

# Path to be checked.
dynamo_settings_path = r'Z:\IT\Dynamo Player Settings\dynamoplayer-5'

# Check if the paths exist.
try:
    paths_exist(dynamo_settings_path)
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


# Target directory for the dynamo player settings.
# Combine the c: drive user folder path with the target directory path end.
begDir = os.path.expanduser('~')
endDir = 'AppData\Local\dynamoplayer-5'
target_dir = os.path.join(begDir,endDir)
print(target_dir)


# Source directory for the dynamo player settings on the server.
source_dir = r'Z:\IT\Dynamo Player Settings\dynamoplayer-5'


# Get all names files in the source directory.
fileNames = os.listdir(source_dir)
print(fileNames)


# Check if the target directory exists.
if not os.path.exists(target_dir):
    # Copy the dynamo player settings folder if the folder does not exist at
    # the target path.
    shutil.copytree(source_dir, target_dir)


# Check if the source directory has been modified more recently.
# than the target directory.
print(os.path.exists(source_dir) and os.path.getmtime(source_dir) > \
    os.path.getmtime(target_dir))
if os.path.exists(source_dir) and os.path.getmtime(source_dir) > \
    os.path.getmtime(target_dir):

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
