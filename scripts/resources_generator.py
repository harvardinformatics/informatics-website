############################################################
# For informatics site, 11.23
# This generates the file "index.md" for the resources page
# and all tag pages
############################################################

import sys, os
import csv

############################################################

resources_template_file = "templates/resources_template.md";
tag_template_file = "templates/tag_table_template.md";

links_file = "../data/links_and_tags.csv"
# Input files and templates

resources_output_file = "../docs/resources/index.md";

####################

resources_template = open(resources_template_file, 'r').read();
tag_template = open(tag_template_file, 'r').read();
# Read the templates

links = {};
tags = [];
with open(links_file, 'r') as file:
    csv_reader = csv.reader(file);
    for row in csv_reader:
        name = row[0];
        if name not in links:
            links[name] = {'link' : row[1], 'tags' : [] };
        links[name]['tags'].append(row[2]);

        tags.append(row[2]);
tags = list(set(tags));
# Read the csv file

####################

for tag in tags:
    print(tag);
    rel_tag_table_file = "../data/" + tag + ".csv";
    tag_table_file = "data/" + tag + ".csv";
    with open(rel_tag_table_file, 'w') as file:
        csv_writer = csv.writer(file);
        headers = ['Resource', 'Tags'];
        csv_writer.writerow(headers);
        for name in links:

            if tag in links[name]['tags']:
                cur_link = "<a href='" + links[name]['link'] + "' target='_blank'>" + name + "</a>";

                links[name]['tags'].sort();

                cur_tag_links = [];
                for link_tag in links[name]['tags']:
                    cur_tag_links.append("<span class='tag-link'><a href='../" + link_tag + "/'>" + link_tag + "</a></span>");

                csv_writer.writerow([cur_link, " ".join(cur_tag_links)]);
    # Write the csv files for each tag

    tag_output_name = "../docs/resources/tags/" + tag + ".md";
    with open(tag_output_name, 'w') as tag_output:
        tag_output.write(tag_template.format(tag_name=tag, tag_table_file=tag_table_file));

####################

with open(resources_output_file, 'w') as resources_output:
    resources_output.write(resources_template.format(tag_list=" ".join(tags)));