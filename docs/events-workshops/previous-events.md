---
title: "Previous events and workshops"
description: "A list of all previous events and workshops developed and hosted by the Harvard FAS Informatics group"
---

# Previous events and workshops

These are topics of previous events with no attached contents and the dates of our previous workshops. See [Events & Workshops](index.md) for the most up-to-date workshop content! 

---

<table class="icon-key">
    <caption><em>Event icon key. Additionally, hover icons on page to view label.</em></caption>
    <tr>
        <td><span class="twemoji" aria-label="Workshop" title="Workshop">{% include "assets/.icons/tools.svg" %}</span> = Workshop</td>
        <td><span class="twemoji" aria-label="Short training" title="Short training">{% include "assets/.icons/monitor-account.svg" %}</span> = Short training</td>
        <td><span class="twemoji" aria-label="Special event" title="Special event">{% include "assets/.icons/star-plus-outline.svg" %}</span> = Special event</td>
        <td><span class="twemoji" aria-label="Programming and Pizza" title="Programming and Pizza">{% include "assets/.icons/pizza-slice.svg" %}</span> = Programming and Pizza</td>
    </tr>
</table>

## 2025
 
{{ read_csv('data/previous-events/2025-events.csv') }}

## 2024

{{ read_csv('data/previous-events/2024-events.csv') }}

## 2023

{{ read_csv('data/previous-events/2023-events.csv') }}

## 2020

{{ read_csv('data/previous-events/2020-events.csv') }}

## 2019

{{ read_csv('data/previous-events/2019-events.csv') }}

> *2019 Bioinformatics nanocourse topics
>
> Week 1: Introduction to R (Mon-Wed) and Introduction to Python (Wed-Fri, Northwest Building B108)
>
> Week 2: Introduction to Bioinformatics (Monday, Lamont Library B-30), Population Genetics (Tuesday, Biolabs 1058), RNA-seq (Wednesday, Lamont Library B-30), and single-cell analysis (Thursday, Lamont Library B-30) 

## 2018

{{ read_csv('data/previous-events/2018-events.csv') }}

> *2018     Bioinformatics nanocourse topics
>
> Introduction to R, Introduction to Unix, Introduction to the Odyssey cluster, Functional Genomics, Comparative and Population Genomics

## 2017

{{ read_csv('data/previous-events/2017-events.csv') }}    

---

<!-- --------------------------------- -->
<!-- Page specfic CSS -->
<!-- These styles modify the table class -->

<style>
    .md-typeset__table {
        width: 100% !important;
        max-width: 1280px !important;
    }
    /* Ensure table takes full width */
    
    .md-typeset__table table {
        width: 100% !important;
        table-layout: fixed;
    }
    /* Ensure table takes full width and has fixed layout */

    .md-typeset th, .md-typeset td {
    white-space: normal;
    overflow-wrap: break-word;
    word-break: break-word;
    }
    /* Ensure text wraps in table cells */

    .md-typeset table th:nth-child(1),
    .md-typeset table td:nth-child(1) { width: 3%; }

    .md-typeset table th:nth-child(2),
    .md-typeset table td:nth-child(2) { width: 40%; }

    .md-typeset table th:nth-child(3),
    .md-typeset table td:nth-child(3) { width: 16%; }

    .md-typeset table th:nth-child(4),
    .md-typeset table td:nth-child(4) { width: 14%; }

    .md-typeset table th:nth-child(5),
    .md-typeset table td:nth-child(5) { width: 26%; }
    /* Set widths for all 5 columns */

    table thead { display: none; }
    .md-typeset table, 
    .md-typeset th, 
    .md-typeset td {
        border: none !important;
    }
    /* Remove borders from table, th, and td */

    .md-typeset__table tr:nth-child(even):hover,
    .md-typeset__table tbody tr:nth-child(even):hover {
        background-color: #f6f8fa !important;
    }
    .md-typeset__table tr:nth-child(odd):hover,
    .md-typeset__table tbody tr:nth-child(odd):hover {
        background-color: #ffffff !important;
    }
    /* Disable hover effect on table rows */


    /* ----- */
    /* Icon key table styles */
    table.icon-key {
        /* margin-left: auto;
        margin-right: auto;         */
        /* border: 1px solid #888888 !important;    Or your desired color and thickness */
        border-radius: 8px !important;        /* Optional, for rounded edges */
        border-collapse: separate !important; /* Essential to prevent cell borders */
        overflow: hidden !important;          /* Optional, for clean rounded corners */
        padding-left: 1em !important; /* Optional, for spacing around the table */
    }

    .icon-key caption {
        caption-side: top;         /* default, but can use bottom */
        font-size: 0.9em;
        color: #666666;
        text-align: left;
    }

    .icon-key td, .icon-key th {
        /* Optional: add very basic, uniform formatting, or none at all */
        width: auto !important;
        background: none !important;
        border: none !important;
        text-align: left;
        padding-right: 1em;
    }    
</style>




