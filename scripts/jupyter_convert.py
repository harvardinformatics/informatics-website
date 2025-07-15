import os, sys
import re
import subprocess


############################################################

def wrapOutputBlocks(md_lines):
    result = []
    in_code_block = False
    in_div = False  # Track if inside <div>...</div>
    expect_output_block = False   # Set to True immediately after code block ends

    i = 0
    while i < len(md_lines):
        line = md_lines[i]

        # Track entry/exit of <div>...</div>
        if not in_code_block:
            if re.search(r'<div\b', line):
                in_div = True
            if re.search(r'</div>', line):
                in_div = False

        # Detect start/end of code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            result.append(line)
            i += 1
            if not in_code_block:
                # Just finished a code block!
                expect_output_block = True
            continue

        # If we just finished a code block, and this line is indented (and not in div), wrap the block
        if expect_output_block and not in_div and re.match(r' {4,}', line):
            output_block = []
            while i < len(md_lines) and (re.match(r' {4,}', md_lines[i]) or md_lines[i].strip() == ""):
                output_line = md_lines[i][4:]  # Remove 4 spaces
                output_line = output_line.replace("<", "&lt;").replace(">", "&gt;")
                output_block.append(output_line)
                i += 1

            while output_block and output_block[-1].strip() == "":
                output_block.pop()

            result.append('<pre class="output-block">')
            result.extend(output_block)
            result.append('</pre>\n')
            expect_output_block = False   # ONLY wrap *immediately after* code block
            continue
        else:
            result.append(line)
            i += 1
            if line.strip() != "" and expect_output_block:
                # We reached a non-output line after code, turn off the expectation
                expect_output_block = False

    return result

############################################################

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
        "authors" : ["Lei Ma", "Tim Sackton"],
    },
    "Python-Day4.ipynb": {
        "title": "[Workshop] Python intensive, day 4",
        "description": "Introduction to file handling and the numpy library for numerical computing in Python, including arrays and basic operations.",
        "authors" : ["Lei Ma", "Adam Freedman"],
        "alts" : ["A pie chart titled 'Programming Language Popularity': Python 26.9%, Ruby 26.2%, C++ 30.6%, and Java 16.2%."]
    },
    "Python-Day5.ipynb": {
        "title": "[Workshop] Python intensive, day 5",
        "description": "Introduction to data manipulation with pandas and data visualization with seaborn.",
        "authors" : ["Danielle Khost", "Adam Freedman"],
        "alts" : ["An illustration of a penguin's head with 'bill length' and 'bill depth'. Note: In the raw data, bill dimensions are recorded as 'culmen length' and 'culmen depth'. The culmen is the dorsal ridge atop the bill.",
                  "An image showing the different seaborn plot categories and the types of plots within them: relplots are scatter plots and line plots; distplots are histograms, KDE plots, ecdf plots, and rug plots; catplots are bar plots, box plots, violin plots, strip plots, swarm plots, and point plots",
                  "A histogram showing 'flipper length' in millimeters on the x-axis ranging from 170-230 and 'Count' on the y-axis ranging from 0 to 80. There is a sharp peak around 190mm, a drop-off at 205mm, and then a smaller peak around 215mm.",
                  "A categorical boxplot. On the x-axis are 3 bird species: Adelie, Gentoo, and Chinstrap. The y-axis is 'bill length' in millimeters ranging from 35-60. Adelie have the shortest bill length with a median around 39mm while the other two species have similar distributions of bill length with medians around 46-47mm.",
                  "An overlapping histogram showing the distribution of 'flipper length' in millimeters for 3 species of penguins: Adelie, Gentoo, and Chinstrap. The x-axis ranges from 170-230mm and the y-axis is 'Count'. Because the bars overlap, the data is difficult to parse.",
                  "A stacked histogram showing the distribution of 'flipper length' in millimeters for 3 species of penguins: Adelie, Gentoo, and Chinstrap. The x-axis ranges from 170-230mm and the y-axis is 'Count'. The bars are stacked on top of each other, making it easier to see the distribution of each species.",
                  "A scatter plot with 'bill length' in millimeters on the x-axis ranging from 35-60 and 'body mass' in grams on the y-axis ranging from 3000-6000. The points are colored by species: Adelie, Gentoo, and Chinstrap. dots represent males and x's represent females. The plot shows a clear separation between the species based on bill length and body mass and a separation between sexes within species."
                  ]
    },
    "Python-Day6.ipynb": {
        "title": "[Workshop] Python intensive, day 6",
        "description": "Analyzing a real dataset: Indiana storms.",
        "authors" : ["Danielle Khost", "Lei Ma"],
        "alts" : ["A barplot showing the number of Floods and Flash Floods in different counties in Indiana. The x-axis separates 'Flood' and 'Flash Flood' events, while the y-axis shows the number of events. Bars in each category are colored by county name.",
                  "A strip plot showing the duration of different events in hours in hours on the x-axis, ranging from 0 to 35. The y-axis shows the event type.",
                  "A strip plot showing the duration of Flood and Flash flood events in hours on the x-axis, ranging from 0 to 35. The y-axis shows the event type."]
    }
}

HOOK_PATH = os.path.abspath(__file__)
HOOK_MTIME = os.path.getmtime(HOOK_PATH)

for jupyter_file in jupyter_files:
    ipynb_path = os.path.join(jupyter_dir, jupyter_file)
    md_path = os.path.splitext(ipynb_path)[0] + ".md"
    print(f"[HOOK] {ipynb_path}")

    rebuild = False
    if not os.path.exists(md_path):
        rebuild = True
    else:
        ipynb_mtime = os.path.getmtime(ipynb_path)
        md_mtime = os.path.getmtime(md_path)
        if ipynb_mtime > md_mtime or HOOK_MTIME > md_mtime:
            rebuild = True

    if not rebuild:
        print(f"    [SKIP] Markdown up to date for {jupyter_file}")
        continue  # Go to next notebook

    convert_cmd = ["jupyter", "nbconvert", "--to", "markdown", ipynb_path]
    subprocess.run(convert_cmd, check=True)

    title = jupyter_files[jupyter_file]["title"]
    description = jupyter_files[jupyter_file]["description"]
    authors = jupyter_files[jupyter_file].get("authors", [])

    author_str = "\n    ".join(f"- {author}" for author in authors)

    ##########

    front_matter = """---
title: "{title}"
description: "{description}"
authors:
    {authors}
---

"""

    front_matter_content = front_matter.format(title=title, description=description, authors=author_str)

    ##########

    style = """
---

<!-- --------------------------------- -->
<!-- Page speciifc CSS -->

<style>

  /* Output table styles */

  div:has(> .dataframe) {
    width: 100%;
    overflow-x: auto;
  }

  .dataframe {
    margin-left: auto;
    margin-right: auto;
    min-width: max-content;
    font-size: 12px;
    border: none;
  }

  .dataframe thead tr:last-child th {
    font-weight: bold;
    background: #fff;    
    border-bottom: 1px solid #000;
  }

  .dataframe tbody th {
    font-weight: bold;
  }

  .dataframe th,
  .dataframe td {
    border: none;
    padding: 3px 3px 3px 18px;
    text-align: right; 
    white-space: nowrap;
  }

  .dataframe thead tr th,
  .dataframe tbody tr th,
  .dataframe tbody tr td {
    border: none;
  }

  .dataframe tbody tr:nth-child(odd) {
    background: #eee;
  }
  .dataframe tbody tr:nth-child(even) {
    background: #fff;
  }
  .dataframe tbody tr:hover {
    background: #cce6ff !important;
  }

  /* Output block styles */
  
  .output-block {
    border: 1px dotted #999999;
    margin-bottom: 0 !important;
    padding: 10px;
    overflow-x: auto;
    overflow-y: auto;
    word-break: break-all;
    word-wrap: break-word;
    white-space: pre-wrap;
    font-size: 13px;
    margin-left: 40px;
    color: rgba(0,0,0,0.87) !important; 
  }

  /* Code block styles */

  .language-python {
    padding-left: 40px;
    font-size: 15px;
  }

</style>
"""

    ##########

    with open(md_path, encoding="utf-8") as md_stream:
        md = md_stream.read().split("\n")

    pattern = r"^(\s*)!\[(.*?)\](\([^\)]*\))"
    num_img = 0;
    for i in range(len(md)):
        if re.match(pattern, md[i]):
            alt_text = jupyter_files[jupyter_file].get("alts", [])[num_img]
            md[i] = re.sub(pattern, r"\1![{}]\3".format(alt_text), md[i])
            num_img += 1

    ##########

    md = wrapOutputBlocks(md)

    md = "\n".join(md)
    with open(md_path, "w", encoding="utf-8") as md_stream:
        md_stream.write(front_matter_content + md + style)

############################################################