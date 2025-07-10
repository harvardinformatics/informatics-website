############################################################
# For informatics site, 06.2025
# An update to the tag generation script, now using
# mkdocs_gen_files and a more compact template.
# The main index tag table is now handled by jinja in 
# reources/index.md and a macro in main.py
############################################################

import os
import json
import mkdocs_gen_files

############################################################

# print("-" * 10);
print("[GEN-FILES] scripts/tags_generator.py")

# Path to your JSON data
json_path = "data/resources/resources-primary.json"

with open(json_path) as f:
    data = json.load(f)

tags = data['tags']
links = data['links']

for tag, tagmeta in tags.items():
    if tagmeta.get("status") != "active":
        continue

    tag_slug = tag.replace(" ", "-")
    filename = f"resources/tags/{tag_slug}.md"

    with mkdocs_gen_files.open(filename, "w") as f_out:
        print(f"""---
title: "[External resource] {tag}"
description: "Links to external resources related to {tag}."
---

{{% set data = get_resources() %}}
{{% set tag = "{tag}" %}}

# {tag} resources

Links to resources related to {{{{ data.tags[tag].description | lower }}}}

<table class="res-tagged-table">
    <colgroup>
        <col style="width: 40%">
        <col style="width: 60%">
    </colgroup>
    <thead>
        <tr>
            <th>Resource</th>
            <th>Tags</th>
        </tr>
    </thead>
    <tbody>
    {{% for name, item in data.links.items() if item.status=="active" and tag in item.tags %}}
        <tr>
            <td>
               <a href="{{{{ item.link }}}}" target="_blank" class="res-external-link">
                 {{{{ name }}}} <span class="twemoji">{{% include "/assets/.icons/link-external-24.svg" %}}</span>
               </a>
            </td>
            <td>
              <div class="res-inline-tags">
              {{% for t in item.tags | sort(case_sensitive=false) %}}
                  <a href="/resources/tags/{{{{ t|replace(' ', '-') }}}}/" class="res-tag-link res-tag-link--inline">{{{{ t }}}}</a>
              {{% endfor %}}
              </div>
            </td>
        </tr>
    {{% endfor %}}
    </tbody>
</table>
""", file=f_out)
        
