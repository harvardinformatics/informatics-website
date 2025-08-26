---
title: Resources
description: "Links to various bioinformatics and data science resources, including tutorials, glossaries, and external resources."
---

# Resources

Here we have compiled resources related to bioinformatics and computing. These resources may be general or related to our [trainings](../events-workshops/index.md). We have also compiled links to external online resources.

## Tutorials

|     |
| --- |
| [:material-application-brackets-outline:{ .contact-icon } [ Installing command line software with conda/mamba ]][conda] |
| [:material-dna:{ .contact-icon } [ Downloading sequencing data from the Bauer Core ]][bauer] |
| [:material-format-align-top:{ .contact-icon } [ Whole genome alignment with Cactus ]][wga] |
| &nbsp;&nbsp;:material-arrow-right-bottom:[:material-filter-variant-plus:{ .contact-icon } [ Adding a genome to a whole genome alignment ]][add-genome] |
| &nbsp;&nbsp;:material-arrow-right-bottom:[:material-vector-polyline-plus:{ .contact-icon } [ Adding an outgroup to a whole genome alignment ]][add-outgroup] |
| &nbsp;&nbsp;:material-arrow-right-bottom:[:material-file-replace-outline:{ .contact-icon } [ Replacing a genome in a whole genome alignment ]][replace-genome] |
| [:curly_loop:{ .contact-icon } [ Pangenome inference with Cactus-minigraph ]][pangenome] |
| [:material-dna:{ .contact-icon } [ How to annotate a genome ]][annotate] |
| [:material-dna:{ .contact-icon } [ How to perform bulk RNA-seq differential expression analysis ]][de] |

**We are developing tutorials for other data science and bioinformatics tasks. Check back soon!**

[conda]: tutorials/installing-command-line-software-conda-mamba.md
[bauer]: tutorials/how-can-i-download-my-sequencing-data.md
[wga]: tutorials/whole-genome-alignment-cactus.md
[add-genome]: tutorials/add-to-whole-genome-alignment-cactus.md
[add-outgroup]: tutorials/add-outgroup-to-whole-genome-alignment-cactus.md
[replace-genome]: tutorials/replace-genome-whole-genome-alignment-cactus.md
[pangenome]: tutorials/pangenome-cactus-minigraph.md
[annotate]: tutorials/how-to-annotate-a-genome.md
[de]: tutorials/differential-expression-analysis.md

---
## Data Concierge Service

The FAS Informatics Group offers a Data Concierge service to support FAS-affiliated labs, especially those working with biological data, in managing research data more effectively. This service provides hands-on support for the development and implementation of data management processes and workflows, with the goal of enabling research continuity. This is a FREE service that is currently in “open beta” but may become a paid service in the future. Sign up is on a rolling basis and we maintain an active waitlist. 

**To sign up for this service, please fill out our [contact](https://forms.office.com/r/qwXEPbBvFK) form with the subject line “Data Concierge: \<PI\> Lab” and a short description of the support you need. You must be a PI or lab manager to request a data concierge.**

The Data Concierge team consists of expert bioinformaticians and will work with FASRC staff, Library Data Managers, and other Harvard groups to provide recommendations and implementation assistance. We work directly with the principal investigator (PI) and at least one additional member from the research group; there is no restriction on how many group members can participate.

The service starts with an intake meeting to discuss your lab’s data management challenges and current practices. Based on this meeting, we will develop a customized data management proposal. We then provide practical assistance to implement the proposed solutions. Example services may include:

- Comparing data storage options for your group
- Connecting instrument computers to FASRC Cannon storage
- Creating and documenting protocols for new data intake
- Organizing lab-wide directory structures and standardizing metadata
- Writing protocol documents and offboarding checklists
- Providing training and materials for the group
- Assisting with data migration
- Assisting with data or code publication

The Data Concierge service is intended to be flexible and responsive to each lab’s specific context and scientific goals. Our team works to identify needs, recommend solutions, and support implementation throughout the process.

---

## [Computing glossary](glossary.md)

Like any specific domain, the way we talk about computing and programming is almost its own language. Words in this context may have different meaning than in other contexts. 
As programmers ourselves, we are so used to using words in the context of programming that we sometimes forget others aren't used to it. This is one of the biggest roadblocks
to teaching and learning.

Here we have compiled a long list of computer and programming related terms in (hopefully) plain language as a resource for anyone learning about programming to look up if they
don't understand a term that they heard or read.

Let us know if there is something we should add!

[View the Computing Glossary:material-arrow-right:](glossary.md){ .md-button .md-button--primary .centered }

<!--

## Bioinformatics glossary

**Click here to go to the full glossary**

## Bioinformatics tools & software for sequence analysis

**Click here to go to the full list**

-->

## External resources

We have compiled a list of external resources and tagged them with the categories below. Click on each tag to see the links!

{% set data = get_resources(page) %}
{% set tag_counts = {} %}
{% for r in data.links.values() if r.status=="active" %}
    {% for tag in r.tags %}
        {% set _ = tag_counts.setdefault(tag, 0) %}
        {% set _ = tag_counts.__setitem__(tag, tag_counts[tag] + 1) %}
    {% endfor %}
{% endfor %}

<div class="res-tag-table">
{% for tag in data.tags | sort(case_sensitive=false) if data.tags[tag].status == "active" %}
  <a class="res-tag-link" href="/resources/tags/{{ tag|replace(' ', '-') }}/">
    {{ tag }} ({{ tag_counts.get(tag, 0) }})
  </a>
{% endfor %}
</div>

---

<!-- --------------------------------- -->
<!-- Page speciifc CSS -->

<style>
    h4 {
        font-weight: normal !important;
    }

    /* ----- */
    /* Style the table that displays the tutorials */
    .md-typeset th, .md-typeset td {
    white-space: normal;
    overflow-wrap: break-word;
    word-break: break-word;
    }
    /* Ensure text wraps in table cells */
    
    table thead { display: none; }
    .md-typeset table, 
    .md-typeset th, 
    .md-typeset td {
        border: none !important;
        font-size: 1.1em !important;
    }
    /* Remove borders from table, th, and td */

    .md-typeset th,
    .md-typeset td {
        padding-top: 0.7em !important;
        padding-bottom: 0.7em !important;
    }

    .md-typeset__table tr:nth-child(even):hover,
    .md-typeset__table tbody tr:nth-child(even):hover {
        background-color: #f6f8fa !important;
    }
    .md-typeset__table tr:nth-child(odd):hover,
    .md-typeset__table tbody tr:nth-child(odd):hover {
        background-color: #ffffff !important;
    }
    /* Disable hover effect on table rows */    

    .md-typeset tr:nth-child(3) td {
        padding-bottom: 0.1em !important;
    }
    /* Style ONLY the 3rd row of the first table on the page */
    
    .md-typeset tr:nth-child(4) td,
    .md-typeset tr:nth-child(5) td,
    .md-typeset tr:nth-child(6) td {
        font-size: 0.92em !important;
        padding-top: 0.1em !important;
        padding-bottom: 0.1em !important;
        background-color: #ffffff !important;        
    }
    /* Style ONLY the 4th, 5th, and 6th rows of the first table on the page */

    .md-typeset tr:nth-child(n+7):nth-child(odd) td {
        background-color: #f6f8fa !important;
    }
    .md-typeset tr:nth-child(n+7):nth-child(even) td {
        background-color: #fff !important;
    }
    /* Style all rows after the 6th row */    
</style>
