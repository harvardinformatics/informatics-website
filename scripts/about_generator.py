############################################################
# For informatics site, 12.23
# This generates the file "index.md" for the about page
############################################################

import sys, os
import json

############################################################

print("-" * 20);
print("RUNNING scripts/about_generatory.py TO GENERATE PROFILE CARDS")

md_template_file = "templates/about_template.md";
#tag_template_file = "templates/tag_table_template.md";
# Markdown templates

json_file = "data/people/people.json";
# JSON file with links and tags

md_output_file = "docs/about/index.md";
# The output file for the resources page

####################

print("READING TEMPLATES");
resources_template = open(md_template_file, 'r').read();
#tag_template = open(tag_template_file, 'r').read();
# Read the templates

print("READING PEOPLE JSON");
with open(json_file, 'r') as json_file:
    json_data = json.load(json_file)

# bio = resources["bioinformatics"];
# ops = resources["softwareops"];
# Read the primary JSON file to get all links and tags

#tag_list = sorted(list(tags.keys()), key=lambda x: x.lower());
# Get a list of the active tags, sorted alphabetically

####################

# tag_counts = { tag : 0 for tag in tag_list };
# # Tag counts to display in the buttons on the resources page

# for tag in tag_list:
# # Loop over every tag to generate a csv table and a markdown page for each

#     print("ADDING TAG PAGE:\t" + tag);

#     rel_tag_table_file = "data/resources/tag-csv/" + tag.replace(" ", "-") + ".csv";
#     # The path to the tag table file relative to this script

#     tag_table_file = "data/resources/tag-csv/" + tag.replace(" ", "-") + ".csv";
#     # The path to the tag table file rela   tive to the project config file (mkdocs.yml)

#     with open(rel_tag_table_file, 'w') as file:
#         csv_writer = csv.writer(file);
#         # Initialize the csv writer for the current tag table

#         headers = ['Resource', 'Tags'];
#         csv_writer.writerow(headers);
#         # Write headers for the csv file/tag table

#         for link in links:
#         # Loop over every link to check if it has the current tag

#             if links[link]['status'] == "active":
#             # Only check links that are active

#                 if tag in links[link]['tags']:
#                 # Check if the current tag is in the current link

#                     tag_counts[tag] += 1;
#                     # Increment the count for the current tag

#                     cur_link = "<a href='" + links[link]['link'] + "' target='_blank'>" + link + "</a>";
#                     # HTML for the current resource link

#                     links[link]['tags'].sort(key=lambda x: x.lower());
#                     # Sort all tags for this link alphaetically

#                     cur_tag_links = [];
#                     for link_tag in links[link]['tags']:
#                         cur_tag_links.append("<span class='tag-link'><a href='../" + link_tag.replace(" ", "-") + "/'>" + link_tag + "</a></span>");
#                     # Add HTML to link to every tag in the current link

#                     csv_writer.writerow([cur_link, " ".join(cur_tag_links)]);
#                 ## End tag check block
#             ## End active link block
#         ## End link loop

#     tag_output_name = "docs/resources/tags/" + tag.replace(" ", "-") + ".md";
#     # The path to the tag page relative to this script

#     with open(tag_output_name, 'w') as tag_output:
#         tag_output.write(tag_template.format(tag_name=tag, description=tags[tag]['description'], tag_table_file=tag_table_file));
#     # Write the tag page using the template
# ## End tag loop

####################

print("GENERATING TAG TABLE");
with open(md_output_file, 'w') as md_output:

    cards_table = "";
    cards_per_row = 2;
    card_width = "10";
    inner_margin = "2"
    # Initialize variables for the card table

    for section in json_data:
        print(section);
        cards_table += "\n\n## " + section + "\n";

        for sub_section in json_data[section]:
            print(sub_section);
            first_row = True;
            cards_table += "\n\n### " + sub_section + "\n";

            people_list = sorted(list(json_data[section][sub_section].keys()));
            people_list = [ person for person in people_list if json_data[section][sub_section][person]['status'] == "active" ];
            people_left = len(people_list);

            for person in people_list:
                print(person);
                person_data = json_data[section][sub_section][person];

                if first_row:
                    cur_card_num = 1;

                    if people_left < cards_per_row:
                        row_margin = "7";
                    else:
                        row_margin = "1";

                    cards_table += '\n<div class="row card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    first_row = False;
                # For the first row, add a div to contain the tag buttons

                if cur_card_num > cards_per_row:
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cards_table += '</div>\n';

                    cards_table += '\n<div class="card-sep-div"></div>\n';
                    

                    if people_left < cards_per_row:
                        row_margin = "7";
                    else:
                        row_margin = "0";

                    cards_table += '\n<div class="row card-row">\n';
                    cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cur_card_num = 1;
                # If the current row is full, close it and add a new one

                cards_table += '\n<div class="col-' + card_width + '-24 card-container">\n';
                
                cards_table += '\t<div class="row card-name-container">\n';
                cards_table += '\t\t<div class="col-6-24 card-margin"></div>\n';
                cards_table += '\t\t<div class="col-12-24 card-name">\n';
                cards_table += '\t\t\t' + person_data['name'] + ', Ph.D.\n';
                cards_table += '\t\t</div>\n';
                cards_table += '\t\t<div class="col-6-24 card-margin"></div>\n';
                cards_table += '\t</div>\n';

                cards_table += '\t<div class="row card-content-container">\n';
                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_table += '\t\t<div class="col-8-24 card-img-container">\n';

                if person_data['link'] != "":
                    cards_table += '\t\t\t<a href="' + person_data['link'] + '" target="_blank">\n';
                    cards_table += '\t\t\t\t<img class="card-img" src="../' + person_data['img'] + '" alt="' + person_data['name'] + '">\n';
                    cards_table += '\t\t\t</a>\n';
                else:
                    cards_table += '\t\t\t<img class="card-img" src="../' + person_data['img'] + '" alt="' + person_data['name'] + '">\n';
                cards_table += '\t\t</div>\n';

                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_table += '\t\t<div class="col-13-24 card-content">\n';
                cards_table += '\t\t\t' + person_data['email'] + '<br>\n';
                cards_table += '\t\t\t Northwest Labs, ' + person_data['office'] + '<br>\n';
                cards_table += '\t\t\t<p>' + person_data['profile'] + '</p>\n';
                cards_table += '\t\t</div>\n';
                cards_table += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_table += '\t</div>\n';
                cards_table += '\t<div class="sep-div"></div>\n';


                link_types = ['link', 'pubs', 'github'];
                links = { link_type : person_data[link_type] for link_type in link_types if person_data[link_type] != "" };
                num_links = len(links);

                if num_links > 0:
                    if num_links == 3:
                        links_outer_margin = "2";
                        links_inner_margin = "2";
                    elif num_links == 2:
                        links_outer_margin = "6";
                        links_inner_margin = "2";
                    elif num_links == 1:
                        links_outer_margin = "10";
                        links_inner_margin = "0";

                    cards_table += '\t<div class="row card-link-row">\n\n';
                    cards_table += '\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';

                    if 'link' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['link'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/website-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>Website</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                
                        if num_links > 1:
                            cards_table += '\t\t<div class="col-' + links_inner_margin + '-24 card-margin"></div>\n\n';
                
                    if 'pubs' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['pubs'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/scholar-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>Scholar</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                
                        if num_links > 2:
                            cards_table += '\t\t<div class="col-' + links_inner_margin + '-24 card-margin"></div>\n\n';
                
                    if 'github' in links:
                        cards_table += '\t\t<div class="col-4-24 card-link-container">\n\n';
                        cards_table += '\t\t\t<div class="icon-link-container">\n';
                        cards_table += '\t\t\t\t<a class="icon-link" href="' + person_data['github'] + '" target="_blank">\n';
                        cards_table += '\t\t\t\t\t<div class="icon-container">\n';
                        cards_table += '\t\t\t\t\t\t<img class="icon" src="../img/icons/github-logo-black.png">\n';
                        cards_table += '\t\t\t\t\t</div>\n';
                        cards_table += '\t\t\t\t\t<span>GitHub</span>\n';
                        cards_table += '\t\t\t\t</a>\n';
                        cards_table += '\t\t\t</div>\n';
                        cards_table += '\t\t</div>\n\n';
                
                    cards_table += '\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';
                    cards_table += '\t</div>\n\n';

                cards_table += '</div>\n';
                print(cur_card_num);
                if cur_card_num != cards_per_row and people_left != 1:
                    cards_table += '<div class="col-' + inner_margin + '-24 card-margin-inner"></div>\n';        
                cur_card_num += 1;
                people_left -= 1;
                print(people_left);
                print("----")
            
                # Add the current tag button to the table
            ## End person loop
            #if cards_in_row != cards_per_row:
            print(row_margin);
            cards_table += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            cards_table += "</div>\n";
            # If the last row isn't full, close it
        ## End sub-section loop
    ## End section loop



    md_output.write(resources_template.format(profile_cards_table=cards_table));
    # Write the resources page using the template
## Close the resources output file

print("-" * 20);

############################################################


