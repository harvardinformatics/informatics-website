def define_env(env):
    author_avatars = {
        "Gregg Thomas": "/img/people/greggthomas.jpg",
        "Adam Freedman": "/img/people/adamfreedman.jpg",
        "Tim Sackton": "/img/people/timsackton.jpg",
        "Lei Ma": "/img/people/leima.jpg",
        "Nathan Weeks": "/img/people/nathanweeks.jpg",
    }

    @env.macro
    def author_row(page):
        authors = page.meta.get('authors') or [page.meta.get('author')]
        author_header = page.meta.get('author_header', 'Authors')
        line = '<span class="author-row">'
        line += f'<span class="author-header">{author_header}:</span>'
        if len(authors) >= 5:
            for i, auth in enumerate(authors):
                url = get_author_url(auth)
                avatar = get_avatar(auth)
                margin = " margin-right: 0.5em;" if i < len(authors)-1 else ""
                line += f'<a href="{url}" style="{margin}"><img src="{avatar}"></a>'
        else:
            for i, auth in enumerate(authors):
                url = get_author_url(auth)
                avatar = get_avatar(auth)
                margin = " margin-right: 0.75em;" if i < len(authors)-1 else ""
                line += f'<a href="{url}" style="{margin}"><img src="{avatar}" style="margin-right: 0.5em;">{auth}</a>'
        line += '''
<span style="margin: 0 0.4em;">·
<small style="color: #888;">
    :material-clock-edit-outline: Last updated: {{ git_revision_date_localized }}
</small>
</span>
</span>
'''
        return line

    def author_str(author):
        if isinstance(author, dict):
            return author.get("name", "")
        return str(author)

    @env.macro
    def get_avatar(author):
        name = author_str(author)
        return author_avatars.get(name, "/img/people/default.jpg")

    @env.filter
    def slugify(author):
        name = author_str(author)
        return name.lower().replace(" ", "-")

    @env.macro
    def get_author_url(author):
        name = author_str(author)
        return f"/people/{name.lower().replace(' ', '-')}/"