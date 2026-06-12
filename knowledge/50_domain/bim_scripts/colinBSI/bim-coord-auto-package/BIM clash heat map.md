Next we will build the Automated Clash Heat Map System. This converts Navisworks clash reports into visual coordination intelligence so your BIM Command Center can instantly show:

  

- Where clashes concentrate in the building
- Which floors are high-risk
- Which disciplines create the most clashes
- Where coordination effort should focus

  

  

This is one of the most powerful coordination tools used by elite VDC teams.

  

  

  

  

Automated Clash Heat Map System

  

  

  

System Overview

  

Navisworks Clash Test

        ↓

Export Clash Data (XML / CSV)

        ↓

Clash Data Parser (Python)

        ↓

Grid + Level Aggregation

        ↓

Heat Map Dataset

        ↓

Power BI Visualization

Output example:

Level 3 / Grid C5 → 42 clashes

Level 2 / Grid B3 → 18 clashes

Level 1 / Grid D7 → 6 clashes

  

  

  

  

Step 1 — Export Clash Data from Navisworks

  

  

In Navisworks Manage → Clash Detective:

Run Clash Tests

Then export results:

Clash Detective

→ Results

→ Export

→ XML Report

Recommended format:

XML

because it includes:

clash ID

item 1

item 2

level

coordinates

clash status

discipline

Save reports to:

ACC/BIM Coordination/ClashReports/

  

  

  

  

Step 2 — Clash Data Parser (Python)

  

  

This script converts the Navisworks clash report into structured coordination data.

  

Save as:

clash_parser.py

import xml.etree.ElementTree as ET

import csv

  

input_file = "clash_report.xml"

output_file = "clash_heatmap_data.csv"

  

tree = ET.parse(input_file)

root = tree.getroot()

  

data = []

  

for clash in root.iter("clashresult"):

  

    clash_id = clash.attrib.get("name")

  

    status = clash.find("status")

    if status is not None:

        status = status.text

    else:

        status = "active"

  

    pos = clash.find("clashpoint/pos3f")

  

    if pos is not None:

        x = float(pos.attrib.get("x"))

        y = float(pos.attrib.get("y"))

        z = float(pos.attrib.get("z"))

    else:

        x = y = z = 0

  

    data.append([clash_id, status, x, y, z])

  

with open(output_file, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow(["ClashID","Status","X","Y","Z"])

    writer.writerows(data)

  

print("Clash data exported to:", output_file)

Output example:

|   |   |   |   |   |
|---|---|---|---|---|
|ClashID|Status|X|Y|Z|
|Clash 001|Active|245|812|36|
|Clash 002|Active|221|790|38|

  

  

  

  

Step 3 — Convert Coordinates to Grid + Level

  

  

Now convert coordinates to building zones.

  

Example mapping:

Z coordinate → Level

X coordinate → Grid

Y coordinate → Grid

Example:

|   |   |
|---|---|
|Z Height|Level|
|0–15 ft|Level 1|
|15–30 ft|Level 2|
|30–45 ft|Level 3|

Add this logic to the script:

def get_level(z):

    if z < 15:

        return "Level 1"

    elif z < 30:

        return "Level 2"

    elif z < 45:

        return "Level 3"

    else:

        return "Roof"

Each clash now gets:

Level

Zone

Grid region

  

  

  

  

Step 4 — Clash Aggregation

  

  

Now group clashes.

  

Example grouping logic:

Level + Grid Region

Example result:

|   |   |   |
|---|---|---|
|Level|Zone|ClashCount|
|Level 3|Mechanical Room|42|
|Level 2|Corridor|18|
|Level 1|Lobby|7|

  

  

  

  

Step 5 — Power BI Heat Map

  

  

Import dataset:

clash_heatmap_data.csv

Create visuals.

  

  

  

  

Heat Map by Level

  

  

Axis:

X → Grid

Y → Level

Value:

Clash Count

Color scale:

0–10 = Green

10–25 = Yellow

25+ = Red

  

  

  

  

Clash Concentration Map

  

  

Bar chart:

Location vs Clash Count

Example output:

|   |   |
|---|---|
|Location|Clashes|
|Level 3 Mechanical Room|42|
|Level 2 Corridor|18|
|Roof Structure|12|

  

  

  

  

Discipline Clash Chart

  

  

Use clash test names:

|   |   |
|---|---|
|Discipline Pair|Clashes|
|Mechanical vs Structure|210|
|Mechanical vs Electrical|88|
|Plumbing vs Structure|45|

  

  

  

  

Step 6 — Command Center Display

  

  

Your BIM Command Center now shows:

  

  

Screen 1

  

Model Health Scores

  

Screen 2

  

Clash Heat Map

  

Screen 3

  

Open Issues

  

Screen 4

  

Coordination Risk

Coordination meetings become data driven instead of guesswork.

  

  

  

  

Weekly Automated Workflow

  

  

Monday

Model uploads (deadline for all disciplines)

Tuesday

Clash tests run in Navisworks; clash XML exported

Wednesday

Automation scripts process clashes; heat map script runs; clash groups generated

Thursday

ACC issues created automatically; Power BI dashboard refreshed

Friday

Coordination meeting using dashboards and heat maps

  

  

  

  

Example Output

  

  

Heat map reveals:

Level 3 Mechanical Room = 94 clashes

Instead of reviewing hundreds of clashes randomly, the team immediately knows:

Focus coordination on Level 3 Mechanical Room

This can reduce coordination time by 40–60%.

  

  

  

  

The Next System That Will Make Your Team Extremely Powerful

  

  

If you’d like, the next thing we can build is the BIM Coordination Automation Toolkit, which includes:

  

- Automated clash grouping in Navisworks
- Automatic ACC issue creation from clashes
- Coordination report generator
- Weekly BIM performance reports

  

  

Together with what we’ve already built, this forms a complete BIM automation ecosystem that only the most advanced VDC departments implement.