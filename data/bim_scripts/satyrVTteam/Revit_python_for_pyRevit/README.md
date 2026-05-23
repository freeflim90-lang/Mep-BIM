Tested with Revit 2025 and pyRevit v5.0.1
All the python script nodes are switched to CPython3 with exceptions:
1. You still have to install IronPython2.7 to make some nodes work. 
2. Don't switch pop-up python scripts to CPython3 because there is a bug in Dynamo "TaskDialog."
Feel free to edit the source .dyn script for your needs.
