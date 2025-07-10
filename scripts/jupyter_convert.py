import os
import subprocess

# REQUIRES: notebook>=7.4.4

jupyter_dir = "docs/workshops/python-intensive/"

jupyter_files = {
    "Python-Day1.ipynb": {
        "title": "[Workshop] Python intensive, day 1",
        "description": "Introduction to programming concepts such as functions, data types, operators, logic, and control flow.",
        "authors" : ["Gregg Thomas", "Tim Sackton"]
    },
    "Python-Day2.ipynb": {
        "title": "[Workshop] Python intensive, day 2",
        "description": "Introduction to Python data structures, including lists and dictionaries, loops, libraries, and writing functions.",
        "authors" : ["Gregg Thomas", "Danielle Khost"]
    },
    "Python-Day3.ipynb": {
        "title": "[Workshop] Python intensive, day 3",
        "description": "More on writing your own functions, debugging strategies, and exception handling in Python.",
        "authors" : ["Lei Ma", "Tim Sackton"]
    },
    "Python-Day4.ipynb": {
        "title": "[Workshop] Python intensive, day 4",
        "description": "Introduction to file handling and the numpy library for numerical computing in Python, including arrays and basic operations.",
        "authors" : ["Lei Ma", "Adam Freedman"]
    },
    "Python-Day5.ipynb": {
        "title": "[Workshop] Python intensive, day 5",
        "description": "Introduction to data manipulation with pandas and data visualization with seaborn.",
        "authors" : ["Danielle Khost", "Adam Freedman"]
    },
    "Python-Day6.ipynb": {
        "title": "[Workshop] Python intensive, day 6",
        "description": "Analyzing a real dataset: Indiana storms.",
        "authors" : ["Danielle Khost", "Lei Ma"]
    }
}

for jupyter_file in jupyter_files:
    ipynb_path = os.path.join(jupyter_dir, jupyter_file)
    md_path = os.path.splitext(ipynb_path)[0] + ".md"
    print(f"[HOOK] {ipynb_path}")

    convert_cmd = ["jupyter", "nbconvert", "--to", "markdown", ipynb_path]
    subprocess.run(convert_cmd, check=True)

    title = jupyter_files[jupyter_file]["title"]
    description = jupyter_files[jupyter_file]["description"]
    authors = jupyter_files[jupyter_file].get("authors", [])

    author_str = "\n    ".join(f"- {author}" for author in authors)

    front_matter = """---
title: "{title}"
description: "{description}"
authors:
    {authors}
---
"""

    with open(md_path, encoding="utf-8") as md_stream:
        md = md_stream.read()

    front_matter_content = front_matter.format(title=title, description=description, authors=author_str)

    with open(md_path, "w", encoding="utf-8") as md_stream:
        md_stream.write(front_matter_content + md)

