############################################################
# For informatics site, 06.25
# This generates staff bio pages in the authors directory.
# This can read a bio from data/people/<person>.md and scans
# all markdown files in the docs directory to find pages authored by each person.
############################################################

import os
from pathlib import Path
import glob
import yaml
import json

############################################################

print("-" * 20);
print("RUNNING scripts/generate_author_pages.py TO GENERATE AUTHOR PAGES")

# Settings
docs_dir = "docs"
base_authors_dir = "people"
authors_dir = os.path.join(docs_dir, base_authors_dir)
os.makedirs(authors_dir, exist_ok=True)
md_template_file = "templates/bio_template.md"
author_to_pages = {}

json_file = "data/people/people.json";
# JSON file with profiles

ignore_dirs = [
    authors_dir,  # Skip the authors directory itself
    os.path.normpath("docs/workshops/biotips/2023-fall/"),
]

####################

print("READING TEMPLATES");
md_template = open(md_template_file, 'r').read();
# Read the templates

print("READING PEOPLE JSON");
with open(json_file, 'r') as json_file_stream:
    json_data = json.load(json_file_stream)
# Read the primary JSON file to get all the profiles

# Gather all pages with authors
for mdfile in glob.glob(os.path.join(docs_dir, "**/*.md"), recursive=True):

    # Normalize for comparison
    mdfile_norm = os.path.normpath(mdfile)
    # Skip if in an ignored directory
    if any(mdfile_norm.startswith(os.path.normpath(ignored)) for ignored in ignore_dirs):
        continue

    with open(mdfile, "r", encoding="utf-8") as f:
        lines = f.readlines()
        if lines and lines[0].strip() == "---":
            # Has YAML frontmatter; extract it
            yaml_end = lines[1:].index("---\n") + 1 if "---\n" in lines[1:] else lines[1:].index("---") + 1
            frontmatter = "".join(lines[1:yaml_end])
            meta = yaml.safe_load(frontmatter)
            authors = meta.get("authors") or ([meta["author"]] if "author" in meta else [])
            for author in authors:
                slug = author.lower().replace(" ", "-")
                author_to_pages.setdefault(slug, {'name': author, 'pages': []})

                # Compute relative URL and title
                title = meta.get("title", os.path.basename(mdfile))

                if "author_header" in meta and meta["author_header"].lower() == "page maintainer":
                    title = "[Maintainer] " + title                   
                else:
                    if "Tutorials" in mdfile:
                        title = "[Tutorial] " + title
                    if "workshops" in mdfile:
                        title = "[Workshop] " + title
                    #print(mdfile);
                author_to_pages[slug]['pages'].append({'title': title, 'path': mdfile})

# Write author pages
for slug, data in author_to_pages.items():
    md_output_file = os.path.join(authors_dir, f"{slug}.md")
    print(f"GENERATING AUTHOR PAGE: {md_output_file}")

    person = data['name']

    bio = "";
    if os.path.exists(f"data/people/{slug}.md"):
        with open(f"data/people/{slug}.md", "r", encoding="utf-8") as bio_file:
            bio = bio_file.read()

    # Separate maintainer pages and others
    maintainer_pages = []
    other_pages = []
    for p in data['pages']:
        if p['title'].startswith("[Maintainer]"):
            maintainer_pages.append(p)
        else:
            other_pages.append(p)

    # Combine: others first, then maintainers
    sorted_pages = other_pages + maintainer_pages

    pages_list = []
    for p in sorted_pages:
        from_path = os.path.join(base_authors_dir, f"{slug}.md")
        to_path = p['path'][len("docs")+1:]
        rel_link = os.path.relpath(to_path, os.path.dirname(from_path)).replace("\\", "/")
        pages_list.append(f" - [{p['title']}]({rel_link})")


    with open(md_output_file, "w", encoding="utf-8") as md_output:
        md_output.write(md_template.format(person_lower=person.lower().replace(" ",""), person=person, bio=bio, pages="\n".join(pages_list)));
    # Write the resources page using the template

print("-" * 20);