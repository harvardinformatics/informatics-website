############################################################
# For informatics site, 06.25
# This script defines macros used by the site.
############################################################

import os
import json

############################################################

def define_env(env):

    ## Read the JSON data file containing people information
    PEOPLE_DATA_FILE = os.path.join(env.project_dir, 'data', 'people', 'people.json')
    with open(PEOPLE_DATA_FILE, encoding="utf-8") as f:
        PEOPLE_JSON_DATA = json.load(f)

    ###############

    def getPeopleField(name, field, json_data=PEOPLE_JSON_DATA, default=""):
        """
        Search the nested JSON people data for a person's name, then return the 
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
        
############################################################        