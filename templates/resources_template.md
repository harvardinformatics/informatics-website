---
title: Resources
hide:
    - navigation
---

<style>
    .md-sidebar--secondary {{
        order: 0;
    }}
</style>

# Resources

The FAS Informatics Group creates resources for bioinformatics analysis in the form of tutorials, walkthroughs, and both online and in-person workshops. We have also compiled links to other online resources.

## Current workshops

Below is a list of all current workshops the Informatics Group runs. Workshop files may be temporarily unavailable as we update them during ongoing sessions.

### Intro to Python Intensive

This is a four-day workshop that will introduce students to python as a data science language. This assumes no prior knowledge of python, but will move at a quick pace to cover all the content. The workshop meets for 3 hours for 4 sessions. 

- Day 1: Whirlwind tour of Python, covering the basic concepts of data types, data structures, functions, and plotting in a broad overview 
    - [Download the student jupyter notebook file](Workshops/Python/Python-Day1-student.ipynb)
- Day 2: Deep dive into python functions, with more about how to write functions in python with additional practice exercises
    - [Download the student jupyter notebook file](Workshops/Python/Python-Day2-student.ipynb)
- Day 3: Data transformation and plotting with pandas, matplotlib, and seaborn. 
    - [Download the student jupyter notebook file](Workshops/Python/Python-Day3-student.ipynb)
- Day 4: Putting it all together: We will cover some meta-cognitive tips & tricks as well as work through a longer exercise that combines the previous 3 days of concepts. Plus time for additional Q&A. 
    - **Download the student jupyter notebook file** (coming soon)

### One hour workshops:

- Project organization & Data management
- Git & GitHub introduction
- Installing & Managing software (Conda, Containers)
- Submitting your first SLURM script or job array
- Data Transformation with R Tidyverse
- Plotting with R ggplot
- Introduction to Genome Annotation
- Workflow Management, nextflow demonstration
- scRNA analysis introduction
- Scaling SLURM scripts on the HPC and benchmarking
- SNPArcher tutorial: A snakemake workflow for variant calling in non-model organisms


## Past Workshops

### Introduction to R (Fall 2023)

This workshop aims to introduce first-time users to the [R programming language](https://www.r-project.org/) and the [RStudio](https://posit.co/download/rstudio-desktop/) development environment. We will provide a basic introduction to coding in R and then shift to data manipulation using the [tidyverse](https://www.tidyverse.org/), a set of R libraries designed to handle data tables in a consistent and easy way. Then, we'll learn how to generate some basic plots to explore our data using [ggplot](https://ggplot2.tidyverse.org/). You do not need any prior programming experience to take this workshop. But also note that this workshop is not a comprehensive programming class nor a comprehensive statistics class. The main goal of this workshop is to get you familiar with reading your data into R and performing basic operations and generating figures.

- [Workshop information](Workshops/R/index.html)
- [Get started](Workshops/R/start.html)
- [Part 1: Introduction to R syntax](Workshops/R/R-workshop-2023-Part1.md) - [Download student RMD file](Workshops/R/R-workshop-2023-Part1-student.Rmd)
- [Part 2: Introduction to data manipulation with the tidyverse](Workshops/R/R-workshop-2023-Part2.md) - [Download student RMD file](Workshops/R/R-workshop-2023-Part2-student.Rmd)
- [Part 3: Introduction to data visualization with ggplot](Workshops/R/R-workshop-2023-Part3.md) - [Download student RMD file](Workshops/R/R-workshop-2023-Part3-student.Rmd)

### Unix tips and tricks for bioinformatics (Spring 2024)

This workshop aims to introduce students to some basic bioinformatics file formats, tools, and general best practices. The first two days of the workshop will be dedicated to introductions of bioinformatics file formats and the command line tools that we use to view, manipulate, and analyze them. After that, we will begin to shift from using individual commands to writing shell scripts and constructing bioinformatics workflows.

- [Workshop information](https://harvardinformatics.github.io/workshops/2024-spring/biotips/)
- [Get started](https://harvardinformatics.github.io/workshops/2024-spring/biotips/start.html)

- [Part 1: Bioinformatics tools and file formats 1: FASTA, FASTQ, grep, BAM/SAM, samtools](Workshops/Unix/Biotips-workshop-2024-Day1.md) - [Download student RMD file](Workshops/Unix/Biotips-workshop-2024-Day1-student.Rmd) 
- [Part 2: Bioinformatics tools and file formats 2: bed, awk, bedtools](Workshops/Unix/Biotips-workshop-2024-Day2.md) - [Download student RMD file](Workshops/Unix/Biotips-workshop-2024-Day2-student.Rmd)
- [Part 3: Bioinformatics tools and file formats 3: GFF, VCF, bcftools](Workshops/Unix/Biotips-workshop-2024-Day3.md) - [Download student RMD file](Workshops/Unix/Biotips-workshop-2024-Day3-student.Rmd)
- [Part 4: Shell scripting](Workshops/Unix/Biotips-workshop-2024-Day4.md) - [Download student RMD file](Workshops/Unix/Biotips-workshop-2024-Day4-student.Rmd)

### Healthy Habits for Data Science (Spring 2024)

This workshop aims to teach students how to be more effective at working on their projects using reproducible habits. We learn how to organize projects on the local machine as well as the Cannon cluster, how to manage software environments, how to use git and GitHub to track code changes, and how to write and scale scripts on an HPC. Loose transcripts of the lectures are available below. Download the pdfs of the slides (if applicable) to follow along with the lecture. 

- [Workshop Information](https://harvardinformatics.github.io/workshops/2024-spring/healthy_habits/)
- [Get started](https://harvardinformatics.github.io/workshops/2024-spring/healthy_habits/start.html)

- [Day 1: Reproducibility, and project organization](Workshops/Healthy/healthy_habits_day1.md) - [Download pdf of slides](Workshops/Healthy/healthy_habits_day1_ppt.pdf)
- [Day 2: Installing and Managing Software](Workshops/Healthy/healthy_habits_day2.md)
- [Day 3: Version control with git and GitHub](Workshops/Healthy/healthy_habits_day3.md) - [Download pdf of slides](Workshops/Healthy/healthy_habits_day3_ppt.pdf)
- [Day 4: Running scripts on the Cannon cluster](Workshops/Healthy/healthy_habits_day4.md)


## External resources

We have compiled a list of external resources and tagged them with the categories below. Click on each tag to see the links!

{tags_table}