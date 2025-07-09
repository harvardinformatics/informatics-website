############################################################
# For informatics site, 06.2025
# This generates the file "index.md" for the about page
# Update version uses Jinja2 templates to render the content
# from a JSON data file containing information about people.
############################################################

import json
from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import mkdocs_gen_files

############################################################

def getYearRange(person):
    if person.get("date-joined") and person.get("date-left"):
        start_year = person["date-joined"].split("-")[-1]
        end_year = person["date-left"].split("-")[-1]
        return f"{start_year}" if start_year == end_year else f"{start_year}-{end_year}"
    elif person.get("date-joined"):
        return person["date-joined"].split("-")[-1]
    else:
        return ""

####################

def parseEndYear(person):
    y = person.get("years", "")
    # For "2021-2024" → 2024, for "2022" → 2022
    if "-" in y:
        return int(y.split("-")[-1])
    try:
        return int(y)
    except Exception:
        return -1  # Or another value to push "unknown" to the end

####################

def groupPeopleByTitleAndChunk(people, cards_per_row=2):
    def chunk(lst, n):
        for i in range(0, len(lst), n):
            yield lst[i:i+n]
    all_rows = []
    current_group = []
    current_title = None
    for person in people:
        if person["title"] != current_title and current_group:
            # Split title group into rows of (cards_per_row)
            all_rows.extend(list(chunk(current_group, cards_per_row)))
            current_group = []
        current_group.append(person)
        current_title = person["title"]
    if current_group:
        all_rows.extend(list(chunk(current_group, cards_per_row)))
    return all_rows

####################

def getPeopleByStatus(json_data, status_list):
    people = []
    for section in json_data.values():
        for subsection in section.values():
            for person in subsection.values():
                if person.get("status") in status_list:
                    # Add convenience fields for templates:
                    person = dict(person)  # shallow copy
                    if "degree" not in person:
                        person["degree"] = ""
                    if "years" not in person or not person["years"]:
                        person["years"] = getYearRange(person)
                    people.append(person)
    return people

############################################################

print("-" * 10);
print("MKDOCS-GEN-FILES: scripts/about_generator.py")

DATA_FILE = 'data/people/people.json'
OUTPUT_FILE = 'index.md'

#print("READING PEOPLE JSON");
with open(DATA_FILE, "r", encoding="utf-8") as f:
    json_data = json.load(f)

####################

# Prepare data
#print("PREPARING DATA");
staff = getPeopleByStatus(json_data, ["active"])
grouped_staff = groupPeopleByTitleAndChunk(staff, 2)
alumni = getPeopleByStatus(json_data, ["moved", "retired"])
alumni.sort(key=parseEndYear, reverse=True)

####################

# Set up Jinja2
#print("ADDING TEMPLATES");
env = Environment(
    loader=FileSystemLoader([
        "templates",
        "docs/assets/.icons"
    ]),
    autoescape=False
)
staff_cards = env.get_template("active-cards.html").render(grouped_staff=grouped_staff)
alumni_cards = env.get_template("alumni-cards.html").render(people=alumni)
about_template = env.get_template("about_template.md")

####################

#print("WRITING OUTPUT FILE");
with mkdocs_gen_files.open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(about_template.render(
        staff_cards=staff_cards,
        alumni_cards=alumni_cards,
    ))
#print("DONE: Wrote docs/index.md")
#print("-" * 20);

############################################################