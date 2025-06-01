---
title: Unix tips and tricks for bioinformatics
---

This workshop aims to introduce students to some basic bioinformatics file formats, tools, and general best practices. The first two days of the workshop will be dedicated to introductions of bioinformatics file formats and the command line tools that we use to view, manipulate, and analyze them. After that, we will begin to shift from using individual commands to writing shell scripts and constructing bioinformatics workflows.

Each day we'll be going through some hands-on activities to help you get familiar with some basic tools and file formats used in bioinformatics and genomics research. We will do this by running commands and common bioinformatics programs. While this can be achieved on any terminal with the correct programs installed, we have setup the workshop as a series of R Markdown files so that you can follow along and run the commands within RStudio.

This workshop assumes you have some basic knowledge of the Linux command line. If you know several simple commands like `ls`, `cd`, `cp`, and `mv` you should be ok. However, we won't be teaching these basics in this course, so if you aren't familiar with them you may find the course difficult to follow. 

## Before Class

This workshops requires substantial setup before class, so please read through the instructions below and make sure you have everything ready before the workshop starts. Please contact us at least 24 hours before the workshop if you have any questions or issues.

We **_strongly recommend_** that you run these workshops on the [FASRC Cannon cluster](https://www.rc.fas.harvard.edu/cluster/) so that you can use the same environment as the instructors:

[Biotips setup - Cannon](setup-cannon.md){ .md-button .md-button--primary .centered }

We also provide instructions for running the workshop on your local machine, but you will need to install the required software and packages yourself:

[Biotips setup - Local](setup-local.md){ .md-button .md-button--primary .centered }

---

## Workshop content

Workshop content is available below. R Markdown (.Rmd) files with exercises and solutions are available for download. Additionally, the data files used in the exercises are available for download if you are using a local setup on your own machine.

### Day 1: Bioinformatics tools and file formats 1

Wednesday February 21st, 9:30 am - 12:30 pm, Location: [Northwest Building](https://maps.app.goo.gl/1MqNswcVaTYcCx68A) room 453 

* Sequence file formats: FASTA, FASTQ
* Intro to commands useful for bioinformatics: `grep`, `awk`
* Alignment file formats: BAM/SAM, [`samtools`](http://www.htslib.org/)
* Introduction to piping and redirecting output

Download the R Markdown file for the exercises and solutions:

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day1-student.Rmd
```

View the rendered version with the exercises and solutions:

[Biotips workshop Day 1 - Genomics formats & tools, part 1](https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day1-instructor.html){ .md-button }

Download the data files used in the exercises (local setup only):

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/data1.zip
```

### Day 2: Bioinformatics tools and file formats 2

Thursday February 22nd, 9:30 am - 12:30 pm, Location: [Biolabs](https://maps.app.goo.gl/mtqAuyd1HwFRLJyZ6) room 2062/2064 

* More on piping and redirecting output
* Interval files: bed, GFF
* More on `grep` and `awk`
* Intro to [`bedtools`](https://bedtools.readthedocs.io/en/latest/index.html)

Download the R Markdown file for the exercises and solutions:

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day2-student.Rmd
```

View the rendered version with the exercises and solutions:

[Biotips workshop Day 2 - Genomics formats & tools, part 2](https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day2-instructor.html){ .md-button }

Download the data files used in the exercises (local setup only):

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/data2.zip
```

### Day 3: Shell scripting 1

Wednesday February 28th, 9:30 am - 12:30 pm, Location: [Northwest Building](https://maps.app.goo.gl/1MqNswcVaTYcCx68A) room 353 (NOTE ROOM CHANGE FROM DAY 1)

* More about interval files: bed, GFF
* Variant files: VCF
* Introduction to [`bcftools`](https://samtools.github.io/bcftools/bcftools.html)
* Shell scripting

Download the R Markdown file for the exercises and solutions:

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day3-student.Rmd
```

View the rendered version with the exercises and solutions:

[Biotips workshop Day 3 - Shell scripting, part 1](https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day3-instructor.html){ .md-button }

Download the data files used in the exercises (local setup only):

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/data3.zip
```

### Day 4: Shell scripting 2

Thursday February 29th, 9:30 am - 12:30 pm, Location: [Biolabs](https://maps.app.goo.gl/mtqAuyd1HwFRLJyZ6) room 2062/2064 

* Loops
* Conditional statements
* Handling command line arguments in shell scripts
* Reproducibility best practices

Download the R Markdown file for the exercises and solutions:

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day4-student.Rmd
```

View the rendered version with the exercises and solutions:

[Biotips workshop Day 4 - Shell scripting, part 2](https://harvardinformatics.github.io/workshops/2024-spring/biotips/Biotips-workshop-2024-Day4-instructor.html){ .md-button }

Download the data files used in the exercises (local setup only):

```bash
wget https://harvardinformatics.github.io/workshops/2024-spring/biotips/data4.zip
```