############################################################
# For informatics site, 11.23
# This generates the file "index.md" for the resources page
# and all tag pages
############################################################

import sys, os
# import random
import json
import csv

############################################################

print("-" * 20);
print("RUNNING scripts/resources_generatory.py TO GENERATE TAG PAGES")

md_template_file = "templates/resources_template.md";
tag_template_file = "templates/tag_table_template.md";
# Markdown templates

# computing_glossary_dir = "data/glossary-tables/computing-programming/";
# computing_files = os.listdir(computing_glossary_dir)
# random_computing_table = random.choice(computing_files)
# # Select a random computing glossary table to display on the resources page

json_file = "data/resources/resources-primary.json";
# JSON file with links and tags

resources_output_file = "docs/resources/index.md";
# The output file for the resources page

####################

print("READING TEMPLATES");
md_template = open(md_template_file, 'r').read();
tag_template = open(tag_template_file, 'r').read();
# Read the templates

print("READING RESOURCES JSON");
with open(json_file, 'r') as json_file_stream:
    resources = json.load(json_file_stream)

links = resources["links"];
tags = resources["tags"];
# Read the primary JSON file to get all links and tags

tag_list = sorted(list(tags.keys()), key=lambda x: x.lower());
# Get a list of the active tags, sorted alphabetically

if not os.path.isdir("data/resources/tag-csv"):
    os.mkdir("data/resources/tag-csv");
# Make the directory for the tag tables if it doesn't exist

####################

tag_counts = { tag : 0 for tag in tag_list };
# Tag counts to display in the buttons on the resources page

for tag in tag_list:
# Loop over every tag to generate a csv table and a markdown page for each

    print("ADDING TAG PAGE:\t" + tag);

    rel_tag_table_file = "data/resources/tag-csv/" + tag.replace(" ", "-") + ".csv";
    # The path to the tag table file relative to this script

    tag_table_file = "data/resources/tag-csv/" + tag.replace(" ", "-") + ".csv";
    # The path to the tag table file rela   tive to the project config file (mkdocs.yml)

    with open(rel_tag_table_file, 'w') as file:
        csv_writer = csv.writer(file);
        # Initialize the csv writer for the current tag table

        headers = ['Resource', 'Tags'];
        csv_writer.writerow(headers);
        # Write headers for the csv file/tag table

        for link in links:
        # Loop over every link to check if it has the current tag

            if links[link]['status'] == "active":
            # Only check links that are active

                if tag in links[link]['tags']:
                # Check if the current tag is in the current link

                    tag_counts[tag] += 1;
                    # Increment the count for the current tag

                    cur_link = "<a href='" + links[link]['link'] + "' target='_blank'>" + link + "</a>";
                    # HTML for the current resource link

                    links[link]['tags'].sort(key=lambda x: x.lower());
                    # Sort all tags for this link alphaetically

                    cur_tag_links = [];
                    for link_tag in links[link]['tags']:
                        cur_tag_links.append("<span class='tag-link'><a href='../" + link_tag.replace(" ", "-") + "/'>" + link_tag + "</a></span>");
                    # Add HTML to link to every tag in the current link

                    csv_writer.writerow([cur_link, " ".join(cur_tag_links)]);
                ## End tag check block
            ## End active link block
        ## End link loop

    tag_output_name = "docs/resources/tags/" + tag.replace(" ", "-") + ".md";
    # The path to the tag page relative to this script

    with open(tag_output_name, 'w') as tag_output:
        tag_output.write(tag_template.format(tag_name=tag, description=tags[tag]['description'], tag_table_file=tag_table_file));
    # Write the tag page using the template
## End tag loop

####################

print("GENERATING TAG TABLE");
with open(resources_output_file, 'w') as resources_output:

    tags_table = "";
    tags_per_row = 4;
    tags_in_row = 0;
    first_row = True;
    # Initialize variables for the tag table

    for tag in tag_list:
    # Add a button link for every active tag
        if tags[tag]['status'] == "active":

            cur_tag_count = str(tag_counts[tag]);

            if first_row:
                tags_table += "<div class='row res-tag-table'>\n";
                first_row = False;
            # For the first row, add a div to contain the tag buttons

            if tags_in_row == tags_per_row:
                tags_table += "</div>\n";
                # tags_table += "---\n";
                tags_table += "<div class='sep-div'></div>\n";
                if tag != tag_list[-1]:
                    tags_table += "<div class='row res-tag-table'>\n";
                tags_in_row = 0;
            # If the current row is full, close it and add a new one

            tags_table += "<div class='col-5-24 res-tag-link-cont'>\n"
            tags_table += "<div class='res-tag-link'><a href='tags/" + tag.replace(" ", "-") + "/'>" + tag + " (" + cur_tag_count + ")</a></div>\n";
            tags_table += "</div>\n";
            tags_table += "<div class='col-1-24 res-tag-sep'></div>\n";
            tags_in_row += 1;
            # Add the current tag button to the table
        ## End active tag block
    ## End tag loop

    if tags_in_row != tags_per_row:
        tags_table += "</div>\n";
    # If the last row isn't full, close it

    resources_output.write(md_template.format(tags_table=tags_table));
    # Write the resources page using the template
## Close the resources output file

print("-" * 20);

############################################################
