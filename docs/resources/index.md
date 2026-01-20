---
title: Resources
description: "Links to various bioinformatics and data science resources, including tutorials, glossaries, and external resources."
---

# Resources

Here we have compiled resources related to bioinformatics and computing. These resources may be general or related to our [trainings](../events-workshops/index.md). We have also compiled links to external online resources.

## Tutorials

<div class="grid cards" markdown>

- :material-application-brackets-outline: **[Installing command line software with conda/mamba][conda]**

- :material-dna: **[Downloading sequencing data from the Bauer Core][bauer]**

- :material-dna: **[How to annotate a genome][annotate]**

- :material-dna: **[How to perform bulk RNA-seq differential expression analysis][de]**

- :curly_loop: **[Pangenome inference with Cactus-minigraph][pangenome]**

- <span class="empty-card"></span>

- :material-format-align-top: **[Whole genome alignment with Cactus][wga]**

    ---
    
    **Related tasks:**
    
    :material-filter-variant-plus: [Adding a genome][add-genome]

    :material-vector-polyline-plus: [Adding an outgroup][add-outgroup]

    :material-file-replace-outline: [Replacing a genome][replace-genome]

- <span class="empty-card"></span>

- <span class="empty-card"></span>

</div>

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

## Snakemake configuration for Cannon partition selection

<div style="text-align:center;">
    <img src="../../img/software-logos/cannon-snakemake-cfg.png" alt="Cannon Snakemake configuration" />
</div>

See our page describing how to use the configuration file for automatic partition selection when running Snakemake on the Cannon cluster:

[Snakemake Cannon config :material-arrow-right:](snakemake-cannon-config.md){ .md-button .md-button--primary .centered }

---

## [Computing glossary](glossary.md)

Like any specific domain, the way we talk about computing and programming is almost its own language. Words in this context may have different meaning than in other contexts. 
As programmers ourselves, we are so used to using words in the context of programming that we sometimes forget others aren't used to it. This is one of the biggest roadblocks
to teaching and learning.

Here we have compiled a long list of computer and programming related terms in (hopefully) plain language as a resource for anyone learning about programming to look up if they
don't understand a term that they heard or read.

Let us know if there is something we should add!

[View the Computing Glossary :material-arrow-right:](glossary.md){ .md-button .md-button--primary .centered }

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
    /* Style the tutorial grid cards */
    .md-typeset tr:nth-child(n+7):nth-child(odd) td {
        background-color: #f6f8fa !important;
    }
    .md-typeset tr:nth-child(n+7):nth-child(even) td {
        background-color: #fff !important;
    }
    /* Style all rows after the 6th row */    

    .grid.cards {
        grid-template-columns: repeat(3, 1fr);
    }

    .grid.cards > :is(ul, ol) {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
    }

    /* Completely hide empty placeholder cards */
    .grid.cards > :is(ul, ol) > li:has(.empty-card) {
        visibility: hidden !important;
        border: none !important;
        background: none !important;
        box-shadow: none !important;
        pointer-events: none !important;
    }

    /* Responsive: 2 columns on tablets */
    @media screen and (max-width: 960px) {
        .grid.cards,
        .grid.cards > :is(ul, ol) {
            grid-template-columns: repeat(2, 1fr);
        }
    }

    /* Responsive: 1 column on mobile */
    @media screen and (max-width: 600px) {
        .grid.cards,
        .grid.cards > :is(ul, ol) {
            grid-template-columns: 1fr;
        }
    }
</style>
