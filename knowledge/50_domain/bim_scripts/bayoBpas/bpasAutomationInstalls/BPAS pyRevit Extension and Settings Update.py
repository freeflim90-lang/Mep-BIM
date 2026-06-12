# Import the required libraries
import os
import shutil
import time
import configparser
import sys
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
pyrevit_extension_bpas = r'Z:\CAD Projects\B - BIM TEMPLATES\I - PYREVIT\bpas'

# Check if the paths exist.
try:
    paths_exist(pyrevit_extension_bpas)
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


###############download BPAS extension file to computer###############
# Target directory for the bpas extensions folder.
# Combine the c: drive user folder path with the target directory path end.
begDir = os.path.expanduser('~')
endDir = 'AppData/Roaming/pyRevit/bpas'
target_dir = os.path.join(begDir,endDir)
print(target_dir)


# Source directory for the bpas pyRevit extension folder on the server.
source_dir = r'Z:\CAD Projects\B - BIM TEMPLATES\I - PYREVIT\bpas'


# Get all file names in the source directory.
fileNames = os.listdir(source_dir)
print(fileNames)


# Check if the target directory exists.
if not os.path.exists(target_dir):
    # Copy the bpas extension folder if the folder does not exist at the
    # target path.
    shutil.copytree(source_dir, target_dir)


# Check if the source directory has been modified more recently than the
# target directory.
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
    sys.exit()

#################pyRevit settings and config file update##################

# Open the pyRevit configuration files from the current users computer.
conBegDir = os.path.expanduser('~')
conEndDir = 'AppData\Roaming\pyRevit\pyRevit_config.ini'
configPath = os.path.join(conBegDir,conEndDir)

# Check if the bpas extension file has been updated more recently than the
# config file.
print(os.path.exists(target_dir) and os.path.getmtime(target_dir) > \
    os.path.getmtime(configPath))
if os.path.getmtime(target_dir) > os.path.getmtime(configPath):

    # Modify the config file if the bpas extension file has been modified more
    # recently than the config file.

    # Read the current contents of the config file.
    config = configparser.ConfigParser()
    config.read(configPath)

    # Create text to be written to config files
    configText = '["'+target_dir+'"]'
    print(configText)

    # Get the contents of the pyRevit config file at the core in userextensions.
    print((config.get("core", "userextensions")))

    # Write the new contents to the config file.
    config.set("core", "userextensions", configText)
    with open(configPath, "w") as config_file:
        config.write(config_file)
