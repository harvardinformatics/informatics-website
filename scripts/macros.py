############################################################
# For informatics site, 06.25
# This script defines macros used by the site.
############################################################

import os
import re
import json
import bibtexparser

############################################################

def define_env(env):

    ## Read the JSON data file containing people information
    PEOPLE_DATA_FILE = os.path.join(env.project_dir, 'data', 'people', 'people.json')
    with open(PEOPLE_DATA_FILE, encoding="utf-8") as f:
        PEOPLE_JSON_DATA = json.load(f)

    ###############

    def getPeopleField(name, field, json_data=PEOPLE_JSON_DATA, default=""):
        """
        Helper: Search the nested JSON people data for a person's name, then return the 
        value for the specified field, or a default if not found.
        """
        for group in json_data.values():
            for subgroup in group.values():
                if name in subgroup:
                    return subgroup[name].get(field, default)
        return default

    ###############

    @env.macro
    def author_row(page):
        """
        Macro: Generates a row of author avatars and names, given page metadata.
        
        - For 4 or more authors, show just avatars as links.
        - For fewer than 5 authors, show avatar, name, and link.
        - Pulls avatar and URL info from the loaded people JSON.
        - Includes last updated info (with icon) except for "Page maintainer" rows.
        """

        # Get the authors and the author header from the page metadata
        authors = page.meta.get('authors') or [page.meta.get('author')]
        author_header = page.meta.get('author_header', 'Authors')

        if author_header == "Authors" and len(authors) == 1:
            # If there's only one author, change the header to "Author"
            author_header = "Author"

        # Start building the HTML output
        line = '<span class="author-row">'
        if author_header == "Page maintainer":
            # If this is a maintainer entry, use a different header
            line = '<span class="author-row page-maintainer-row">'
        line += f'<span class="author-header">{author_header}:</span>'

        for i, auth in enumerate(authors):

            # Look up the author's URL and avatar in the JSON data
            url = getPeopleField(auth, "link", PEOPLE_JSON_DATA)
            avatar = "/" + getPeopleField(auth, "img", PEOPLE_JSON_DATA, "images/avatars/default.png")

            # Style the author's avatar and name based on the number of authors
            if len(authors) >= 4:
                margin = " margin-right: 0.5em;" if i < len(authors)-1 else ""
                line += f'<a href="{url}" alt="{auth}" style="{margin}"><img src="{avatar}"></a>'
            else:
                margin = " margin-right: 0.75em;" if i < len(authors)-1 else ""
                line += f'<a href="{url}" alt="{auth}" style="{margin}"><img src="{avatar}" style="margin-right: 0.5em;">{auth}</a>'

        # Finish the HTML with last updated info if not for a maintainer entry
        if author_header != "Page maintainer":
            line += '''
<span style="margin: 0 0.4em;">·
<small style="color: #888;">
    :material-clock-edit-outline: Last updated: {{ git_revision_date_localized }}
</small>
</span>
</span>
'''
        return line
    
    ###############

    @env.macro
    def get_resources():
        """
        Macro: Loads the primary resource data from JSON and returns it (for use in templates).
        This is loaded/re-parsed every time the macro is called. 
        - Used in resources/index.md
        """
        with open(os.path.join(env.project_dir, "data/resources/resources-primary.json"), "r") as f:
            return json.load(f)
        
    ###############

    def bibtexLookup(json_data):
        """
        Helper: Create a lookup table from the JSON people data for bibtex names.
        The lookup table maps bibtex names to their canonical name and status.
        - Helper for render_publications macro.
        """
        lookup = {}
        for group in json_data.values():
            for subgroup in group.values():
                for canonical_name, fields in subgroup.items():
                    status = fields.get("status", "")
                    bibtex_names = fields.get("bibtex-names", [])
                    for bname in bibtex_names:
                        lookup[bname.strip()] = [canonical_name, status]
        return lookup

    def formatAuthor(author):
        """
        Helper: Format an author name into "Lastname FM" style.
        - Helper for render_publications macro.
        """
        author = author.strip()
        # If there is a comma style: "Lastname, F. M."
        if ',' in author:
            last, fi = [s.strip() for s in author.split(',', 1)]
        else:
            # Otherwise, assume "Firstname [Middle] Lastname"
            tokens = author.split()
            if len(tokens) == 1:
                # single name (unlikely)
                return author
            last = tokens[-1]
            fi = ' '.join(tokens[:-1])
        # Grab first letter of each word in fi, uppercase with no dots/spaces
        initials = ''.join([w[0].upper() for w in re.findall(r'\b\w', fi)])
        return f"{last} {initials}"

    @env.macro
    def render_publications(project):
        """
        Macro: Renders a list of publications for a given project.
        - Filters publications based on the project keyword in the bibtex entries.
        - Formats the authors, title, year, journal, volume, number, pages, and DOI.
        - Returns a formatted string suitable for Markdown rendering.
        """

        print(f"Rendering publications for project: {project}")
        project_list = ["annotation", "worm-genomes", "parasitic-plant", "moa", "scrna-methods", 
                        "axolotls", "scrna-ecology", "tube-worms", "transcriptome-assembly",
                        "rnaseq-assessment", "scrub-jay", "coalescent-processes", "snparcher",
                        "phyloacc", "convergent-comparative", "rotifers", "peak-calling", 
                        "proteomics"]
        
        if project not in project_list:
            raise ValueError(
            f"Project '{project}' is not recognized. Please ensure the project name is correct, "
            "and add it to scripts/macros.py if so."
            )

        # Load bibtex entries
        bibtex_file = os.path.join(env.project_dir, 'data', 'publications', 'fasifx-pubs.bib')
        with open(bibtex_file, encoding='utf-8') as f:
            bibtex_db = bibtexparser.load(f)

        # Create a lookup for bibtex names to canonical names and status
        bibtex_lookup = bibtexLookup(PEOPLE_JSON_DATA)

        pubs = []
        # Filter pubs by project keyword
        for entry in bibtex_db.entries:
            kwords = entry.get('keywords','').split("\n")
            if f"project:{project}" in kwords:
                pubs.append(entry)

        # Sort by year (descending) and journal name (ascending)
        pubs.sort(key=lambda e: (-int(e.get('year', 0)), e.get('journal','')))

        # Initialize output string
        output_string = '!!! abstract "Publications"\n\n'

        for pub in pubs:
            # Parse and format authors
            authorlist = [a.strip() for a in pub.get('author', '').split(' and ')]
            formatted_authors = []
            for auth in authorlist:
                # Format author name for output as "Lastname FM"
                formatted_author_name = formatAuthor(auth)

                # If the author is a member of the group, check status to format accordingly
                if auth in bibtex_lookup:
                    canonical_name, status = bibtex_lookup[auth]
                    if status == 'active':
                        formatted_authors.append(f'**{formatted_author_name}**')
                    elif status in ['moved', 'retired']:
                        formatted_authors.append(f'{formatted_author_name} :fontawesome-solid-graduation-cap:')
                    else:
                        formatted_authors.append(formatted_author_name)
                else:
                    formatted_authors.append(formatted_author_name)

            # Extract publication details
            author_str = ', '.join(formatted_authors)
            title = pub.get('title','').strip().rstrip('.')
            year = pub.get('year','')
            journal = pub.get('journal','')
            volume = pub.get('volume','')
            number = pub.get('number','')
            pages = pub.get('pages','')
            doi = pub.get('doi','')
            url = f"https://doi.org/{doi}" if doi else pub.get('url', '')

            # Additional formatting for bioRxiv
            if journal == "bioRxiv":
                pages = '';
            else:
                journal += ". "

            # Additional formatting for issue number
            if number:
                number = f"({number})"

            # Additionaly formatting for pages
            if pages and (volume or number):
                pages = f":{pages}"

            # Construct the citation string
            citation = f"* {author_str}. {year}. {title}. *{journal}*{volume}{number}{pages}."
            if url:
                citation += f' [Link :octicons-link-external-24:]({url}){{target="_blank"}}'

            # Add the citation to the output string    
            output_string += "    " + citation + '\n\n'

        return output_string        
        
############################################################