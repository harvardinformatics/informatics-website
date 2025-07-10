import re
import os

jupyter_dir = "site/workshops/python-intensive/"

jupyter_files = {
    "Python-Day1": {
        "title": "[Workshop] Python intensive, day 1",
        "description": "Introduction to programming concepts such as functions, data types, operators, logic, and control flow."
    },
    "Python-Day2": {
        "title": "[Workshop] Python intensive, day 2",
        "description": "Introduction to Python data structures, including lists and dictionaries, loops, libraries, and writing functions."
    },
    "Python-Day3": {
        "title": "[Workshop] Python intensive, day 3",
        "description": "More on writing your own functions, debugging strategies, and exception handling in Python."
    },
    "Python-Day4": {
        "title": "[Workshop] Python intensive, day 4",
        "description": "Introduction to file handling and the numpy library for numerical computing in Python, including arrays and basic operations."
    },
    "Python-Day5": {
        "title": "[Workshop] Python intensive, day 5",
        "description": "Introduction to data manipulation with pandas and data visualization with seaborn."
    },
    "Python-Day6": {
        "title": "[Workshop] Python intensive, day 6",
        "description": "Analyzing a real dataset: Indiana storms."
    }
}

for jupyter_file in jupyter_files:
    html_path = os.path.join(jupyter_dir, jupyter_file, "index.html")
    print(f"[PATCH] {html_path}")
    
    title = jupyter_files[jupyter_file]["title"]
    description = jupyter_files[jupyter_file]["description"]

    with open(html_path, encoding="utf-8") as html_stream:
        html = html_stream.read()

        # Patch <title>
        html = re.sub(
            r"<title>.*?</title>",
            "<title>[Workshop] Python intensive, day 1</title>",
            html,
            flags=re.DOTALL
        )

        # Patch/add <meta name="description">
        desc = (
            f'<meta name="description" content="{description}">'
        )
        if 'meta name="description"' in html:
            html = re.sub(
                r'<meta name="description" content=".*?">',
                desc,
                html,
                flags=re.DOTALL
            )
        else:
            html = html.replace("</head>", desc + "\n</head>")

        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)

