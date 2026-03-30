#!/usr/bin/env python3
# generates visualization.html by plugging experiment data into template.html

import json, os

here = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(here, "viz_data.json")) as f:
    data = json.load(f)

with open(os.path.join(here, "template.html")) as f:
    html = f.read()

html = html.replace("__VIZ_DATA__", json.dumps(data))

out = os.path.join(here, "visualization.html")
with open(out, "w") as f:
    f.write(html)
print("wrote", out)
