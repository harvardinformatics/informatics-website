############################################################
# For informatics site, 12.23
# This generates the file "index.md" for the about page
############################################################

import sys, os
from datetime import datetime
import json

############################################################

def getCardMargins(people_left, cards_per_row):
    if people_left < cards_per_row:
        return "7";
    else:
        return "1";
# This function gets the margins for the side of the current row, depending
# on how many cards are in the row
# NOTE: if we change the number of cards_per_row from 2, this will need to be updated

def getAlumCardMargins(people_left, cards_per_row):
    if people_left < cards_per_row and people_left == 2:
        return ["7", "2"];
        # [outer row margin, inner margin]
    elif people_left < cards_per_row and people_left == 1:
        return ["9", "0"];
        # [outer row margin, inner margin]
    else:
        return ["0", "1"];
        # [outer row margin, inner margin]

def parse_date(date_str):
    if date_str in [None, "", "unknown"]:
        return datetime.min  # Use a min date to push entries without a valid date to the end
    if date_str.startswith("NA-NA-"):
        year = date_str.split("-")[-1]
        return datetime.strptime(f"01-01-{year}", "%m-%d-%Y")
    try:
        return datetime.strptime(date_str, "%m-%d-%Y")
    except ValueError:
        return datetime.min  # Use a min date to push entries without a valid date to the end
# Sort the moved people by "date-left" in descending order, placing those without "date-left" at the end

############################################################

print("-" * 20);
print("RUNNING scripts/about_generatory.py TO GENERATE PROFILE CARDS")

md_template_file = "templates/about_template.md";
# Markdown templates

json_file = "data/people/people.json";
# JSON file with profiles

md_output_file = "docs/index.md";
#md_output_file2 = "docs/index.md";
# The output file for the about page

####################

print("READING TEMPLATES");
md_template = open(md_template_file, 'r').read();
#tag_template = open(tag_template_file, 'r').read();
# Read the templates

print("READING PEOPLE JSON");
with open(json_file, 'r') as json_file_stream:
    json_data = json.load(json_file_stream)
# Read the primary JSON file to get all the profiles

####################

print("GENERATING BIO PROFILE CARDS");
with open(md_output_file, 'w') as md_output:

    cards_tables = {};
    cards_per_row = 2;
    card_width = "10";
    inner_margin = "2"
    # Initialize variables for the card table
    # Some of these control the width of the cards and the space between them
    # NOTE: that some margins depend on the number of cards in the row, and are set later on

    # Initialize counters
    counts = {
        "Senior Bioinformatics Scientists": 0,
        "Postdoctoral Researchers": 0
    };

    # Loop through the entries and count active people
    for sub_section in counts.keys():
        if sub_section in json_data:
            for person, details in json_data[sub_section].items():
                if details.get("status") == "active":
                    counts[sub_section] += 1;

    for section in json_data:
        cards_tables[section] = "";
        # Write the section header

        for sub_section in json_data[section]:
            first_row = True;
            # cards_table += "\n\n### " + sub_section + "\n";
            # Write the sub-section header

            people_list = list(json_data[section][sub_section].keys());
            people_list = [ person for person in people_list if json_data[section][sub_section][person]['status'] == "active" ];
            people_left = len(people_list);
            # Get the list of active people in the current sub-section and the number of people

            for person in people_list:
                person_data = json_data[section][sub_section][person];
                # Get the profile data for the current person

                if first_row:
                    cur_card_num = 1;

                    row_margin = getCardMargins(people_left, cards_per_row);
                    # Get the row margin for the current row depending on how many cards are in the row

                    cards_tables[section] += '\n<div class="row card-row">\n';
                    cards_tables[section] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    first_row = False;
                ## Get the margins and add a div for the first row

                if cur_card_num > cards_per_row:
                    cards_tables[section] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cards_tables[section] += '</div>\n';
                    # Close the current row

                    cards_tables[section] += '\n<div class="card-sep-div"></div>\n';
                    # Put a vertical space between the two rows
                    
                    row_margin = getCardMargins(people_left, cards_per_row);
                    # Get the row margins for the next row depending on how many cards are left

                    cards_tables[section] += '\n<div class="row card-row">\n';
                    cards_tables[section] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
                    cur_card_num = 1;
                    # Add the new row divs
                ## If the current row is full, close it and add a new one

                cards_tables[section] += '\n<div class="col-' + card_width + '-24 card-container">\n';
                
                cards_tables[section] += '\t<div class="row card-name-container">\n';
                ## The card container div

                cards_tables[section] += '\t\t<div class="col-0-24 card-name-margin"></div>\n';
                cards_tables[section] += '\t\t<div class="col-24-24 card-name">\n';

                degree = "";
                if 'degree' in person_data:
                    if person_data['degree'] != "":
                # Get the degree for the current person if it is available
                        degree = ', ' + person_data['degree'];
                else:
                    degree = ", Ph.D.";
                if person_data['link'] != "":
                    if person_data['link'].startswith("about/people/"):
                        cards_tables[section] += '\t\t\t<b><a href="' + person_data['link'] + '">' + person_data['name'] + degree + '</a></b><br>\n\n';
                    else:
                        cards_tables[section] += '\t\t\t<b><a href="' + person_data['link'] + '" target="_blank">' + person_data['name'] + degree + '</a></b><br>\n\n';
                    # For internal links, don't open in a new tab (no target="_blank")
                else:
                    cards_tables[section] += '\t\t\t<b>' + person_data['name'] + degree + '</b><br>\n\n';
                # Add the person name with or without a link                

                cards_tables[section] += '\t\t</div>\n';
                cards_tables[section] += '\t\t<div class="col-0-24 card-name-margin"></div>\n';
                cards_tables[section] += '\t</div>\n';
                # The card name header div

                cards_tables[section] += '\t<div class="card-name-sep-div"></div>\n';

                cards_tables[section] += '\t<div class="row card-content-container">\n';
                cards_tables[section] += '\t\t<div class="col-1-24 card-margin"></div>\n';

                cards_tables[section] += '\t\t<div class="col-8-24 card-img-container">\n';
                if person_data['link'] != "":
                    if person_data['link'].startswith("about/people/"):
                        cards_tables[section] += '\t\t\t<a href="' + person_data['link'] + '">\n';
                    else:
                        cards_tables[section] += '\t\t\t<a href="' + person_data['link'] + '" target="_blank">\n';
                    cards_tables[section] += '\t\t\t\t<img class="card-img" src="' + person_data['img'] + '" alt="Profile picture of ' + person_data['name'] + '">\n';
                    cards_tables[section] += '\t\t\t</a>\n';
                else:
                    cards_tables[section] += '\t\t\t<img class="card-img" src="' + person_data['img'] + '" alt="Profile picture of ' + person_data['name'] + '">\n';
                # Profile image

                link_types = ['pubs', 'github'];
                links = { link_type : person_data[link_type] for link_type in link_types if person_data[link_type] != "" };
                num_links = len(links);
                # Get the links for the current person

                if num_links > 0:
                    link_width = "12";
                    if num_links == 2:
                        links_outer_margin = "0";
                        links_inner_margin = "0";
                    elif num_links == 1:
                        links_outer_margin = "5";
                        links_inner_margin = "0";
                    # Set the margins for the link row depending on the number of links in the profile

                    cards_tables[section] += '\t\t\t<div class="row card-link-row">\n\n';
                    cards_tables[section] += '\t\t\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';
                    # The link row div and outer margin
                
                    if 'pubs' in links:
                        cards_tables[section] += '\t\t\t\t<div class="col-' + link_width + '-24 card-link-container">\n\n';
                        cards_tables[section] += '\t\t\t\t\t<div class="icon-link-container">\n';
                        cards_tables[section] += '\t\t\t\t\t\t<a class="icon-link" href="' + person_data['pubs'] + '" target="_blank" title="Google Scholar link for ' + person_data['name'] + '">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t<div class="icon-container">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t\t<img class="icon" src="img/icons/scholar-logo-black.png" alt="Google Scholar link profile for ' + person_data['name'] + '">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t</div>\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t<span>Scholar</span>\n';
                        cards_tables[section] += '\t\t\t\t\t\t</a>\n';
                        cards_tables[section] += '\t\t\t\t\t</div>\n';
                        cards_tables[section] += '\t\t\t\t</div>\n\n';
                
                        if num_links > 1:
                            cards_tables[section] += '\t\t\t\t<div class="col-' + links_inner_margin + '-24 card-margin"></div>\n\n';
                    ## End scholar link block
                
                    if 'github' in links:
                        cards_tables[section] += '\t\t\t\t<div class="col-' + link_width + '-24 card-link-container">\n\n';
                        cards_tables[section] += '\t\t\t\t\t<div class="icon-link-container">\n';
                        cards_tables[section] += '\t\t\t\t\t\t<a class="icon-link" href="' + person_data['github'] + '" target="_blank" title="GitHub profile link for ' + person_data['name'] + '">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t<div class="icon-container">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t\t<img class="icon" src="img/icons/github-logo-black.png" alt="Github profile link for ' + person_data['name'] + '">\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t</div>\n';
                        cards_tables[section] += '\t\t\t\t\t\t\t<span>GitHub</span>\n';
                        cards_tables[section] += '\t\t\t\t\t\t</a>\n';
                        cards_tables[section] += '\t\t\t\t\t</div>\n';
                        cards_tables[section] += '\t\t\t\t</div>\n\n';
                    ## End github link block
                
                    cards_tables[section] += '\t\t\t\t<div class="col-' + links_outer_margin + '-24 card-margin"></div>\n\n';
                    cards_tables[section] += '\t\t\t</div>\n\n';
                    # Add the end margin and close the link row div
                ## End links block

                cards_tables[section] += '\t\t</div>\n';
                # Close the image container div

                cards_tables[section] += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_tables[section] += '\t\t<div class="col-13-24 card-content">\n';
                cards_tables[section] += '\t\t\t<b>' + person_data['title'] + '</b><br>\n';
                # cards_tables[section] += '\t\t\t' + person_data['email'] + '<br>\n';
                cards_tables[section] += '\t\t\t Northwest Labs, ' + person_data['office'] + '<br>\n';
                cards_tables[section] += '\t\t\t<p>' + person_data['profile'] + '</p>\n';
                cards_tables[section] += '\t\t</div>\n';
                # Contact info and profile

                cards_tables[section] += '\t\t<div class="col-1-24 card-margin"></div>\n';
                cards_tables[section] += '\t</div>\n';
                ## The card content (image, contact, profile)

                cards_tables[section] += '\t<div class="sep-div"></div>\n';
                # Add a horizontal space between the content and the links     

                cards_tables[section] += '</div>\n';
                ## Close the card container div

                if cur_card_num != cards_per_row and people_left != 1:
                    cards_tables[section] += '<div class="col-' + inner_margin + '-24 card-margin-inner"></div>\n'; 
                # Add the inner margin if the current card isn't the last one in the row

                cur_card_num += 1;
                people_left -= 1;
                # Increment the card number and decrement the number of people left
            ## End person loop

            cards_tables[section] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            cards_tables[section] += "</div>\n";
            # Add the outer margin and close the last row

            cards_tables[section] += '\n<div class="card-sep-div"></div>\n';
            # Put a horizontal space between the sections
        ## End sub-section loop
    ## End section loop

####################

    cards_tables[section] += '<div class="row">\n';
    cards_tables[section] += '<span class="icon-note">Social icons: <a href="https://icons8.com/" target="_blank">Icons8</a></span>\n';
    cards_tables[section] += '</div>\n';

####################

    print("GENERATING ALUMNI CARDS");
    cards_tables["alum"] = "";

    cards_per_row = 3;
    cur_card_num = 1;
    alum_width = "6";
    people_left = 0;
    # Initialize variables for the alumni card table
    # Some of these control the width of the cards and the space between them
    # NOTE: that some margins depend on the number of cards in the row, and are set later on

    alumni_list = [];

    for section in json_data:
        for sub_section in json_data[section]:
            for person in json_data[section][sub_section]:
                person_data = json_data[section][sub_section][person]
                if person_data['status'] != "active":
                    alumni_list.append(person_data);
                    people_left += 1;
    ## Get the list of alumni and the number of people
    ## Since the alumni cards will be in one table, we need to count the total number of people instead of doing it by section like above 

    alumni_list.sort(key=lambda x: parse_date(x.get("date-left", "")), reverse=True)
    # Sort the alumni by "date-left" in descending order, placing those without "date-left" at the end

    for person_data in alumni_list:
        print(person_data.get('name'))

    first_row = True;
    # Since this is one table, we don't need to reset the first row variable for each section

    # for section in json_data:
    #     for sub_section in json_data[section]:
    #         for person in json_data[section][sub_section]:

    for person_data in alumni_list:
        
        #person_data = json_data[section][sub_section][person];
        # Lookup the profile data for the current person

        if person_data['status'] == "active":
            continue;
        # Skip the current person if they are active

        if first_row:
            row_margin, alum_inner_margin = getAlumCardMargins(people_left, cards_per_row);
            # Get the row margins for the current row depending on how many cards are in the row

            cards_tables["alum"] += '\n<div class="row alum-card-row">\n';
            cards_tables["alum"] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            first_row = False;
        ## Get the margins and add a div for the first row

        if cur_card_num > cards_per_row:
            cards_tables["alum"] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            cards_tables["alum"] += '</div>\n';
            # Close the current row

            cards_tables["alum"] += '\n<div class="card-sep-div"></div>\n';
            # Put a vertical space between the two rows
            
            row_margin, alum_inner_margin = getAlumCardMargins(people_left, cards_per_row);
            # Get the row margins for the current row depending on how many cards are in the row

            cards_tables["alum"] += '\n<div class="row alum-card-row">\n';
            cards_tables["alum"] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
            cur_card_num = 1;
            # Add the new row divs
        ## If the current row is full, close it and add a new one

        if person_data['profile'] == "":
            cards_tables["alum"] += '\n<div class="col-' + alum_width + '-24 card-container alum-card-container-no-profile">\n';
        else:
            cards_tables["alum"] += '\n<div class="col-' + alum_width + '-24 card-container alum-card-container">\n';
        ## The card container div 

        if person_data['link'] != "":
            if person_data['link'].startswith("about/people/"):
                cards_tables["alum"] += '\t\t<span class="alum-name"><a href="' + person_data['link'] + '">' + person_data['name'] + '</a></span><br>\n\n';
            else:
                cards_tables["alum"] += '\t\t<span class="alum-name"><a href="' + person_data['link'] + '" target="_blank">' + person_data['name'] + '</a></span><br>\n\n';
        else:
            cards_tables["alum"] += '\t\t<span class="alum-name">' + person_data['name'] + '</span><br>\n\n';
        # Add the person name with or without a link
        
        if person_data['date-joined'] != "" and person_data['date-left'] != "":
            start_year = person_data['date-joined'].split("-")[2];
            end_year = person_data['date-left'].split("-")[2];

            if start_year == end_year:
                cards_tables["alum"] += '\t\t(' + start_year + ')<br>\n\n';
            else:
                cards_tables["alum"] += '\t\t(' + start_year + '-' + end_year + ')<br>\n\n';
        # Lookup the start and end years for the current person and add them to the card if they are available

        if person_data['profile'] != "":
            cards_tables["alum"] += '\t\t<p>' + person_data['profile'] + '</p>\n';
        # Add the person profile if it is available

        cards_tables["alum"] += '</div>\n';
        ## Close the card container div

        if cur_card_num != cards_per_row and people_left != 1:
            cards_tables["alum"] += '<div class="col-' + alum_inner_margin + '-24 card-margin-inner"></div>\n';
        # Add the inner margin if the current card isn't the last one in the row

        cur_card_num += 1;
        people_left -= 1;
        # Increment the card number and decrement the number of people left
    ## End alumni loop

    cards_tables["alum"] += '\n<div class="col-' + row_margin + '-24 card-margin-outer"></div>\n';
    cards_tables["alum"] += "</div>\n\n";        
    # Add the outer margin and close the last row

####################

    print("WRITING OUTPUT FILE");
    md_output.write(md_template.format(bio_profiles=cards_tables["Bioinformatics"], ops_profiles=cards_tables["Software Operations"], alum_profiles=cards_tables["alum"]));
    # Write the resources page using the template
## Close the resources output file

print("-" * 20);

############################################################


