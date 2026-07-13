############################################################
# For informatics site, 07.2026
# This generates "js/scheduled-banners-data.js", a virtual JS
# file exposing the scheduled banner data (data/scheduled-banners/banners.json)
# as a global variable for docs/js/scheduled_banner.js to read.
############################################################

import json
import mkdocs_gen_files

############################################################

print("[GEN-FILES] scripts/scheduled_banners_generator.py")

DATA_FILE = 'data/scheduled-banners/banners.json'
OUTPUT_FILE = 'js/scheduled-banners-data.js'

with open(DATA_FILE, "r", encoding="utf-8") as f:
    banners = json.load(f)

with mkdocs_gen_files.open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write("window.SCHEDULED_BANNERS = ")
    f.write(json.dumps(banners))
    f.write(";\n")

############################################################
