# main.py (located in your docs root)

def define_env(env):
    # Map from author name (as used in front matter) to avatar URL
    author_avatars = {
        "Gregg Thomas": "/img/people/greggthomas.jpg",
        "Adam Freedman": "/img/people/adamfreedman.png",
        "Alex Smith": "/img/people/alexsmith.jpg",
        # Add more as needed
    }

    @env.macro
    def get_avatar(author):
        # Return the mapped avatar or a default image
        return author_avatars.get(author, "/img/people/default.jpg")