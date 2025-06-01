---
title: Introduction to R
---

This workshop aims to introduce first-time users to the [R programming language](https://www.r-project.org/) and the [RStudio](https://posit.co/download/rstudio-desktop/) development environment. We will provide a basic introduction to coding in R and then shift to data manipulation using the [tidyverse](https://www.tidyverse.org/), a set of R libraries designed to handle data tables in a consistent and easy way. Then, we'll learn how to generate some basic plots to explore our data using [ggplot](https://ggplot2.tidyverse.org/). You do not need any prior programming experience to take this workshop. But also note that this workshop is not a comprehensive programming class nor a comprehensive statistics class. The main goal of this workshop is to get you familiar with reading your data into R and performing basic operations and generating figures.

## Before Class

First of all, before class, it is important that you have R and RStudio installed and are able to open RStudio. These are two programs necessary for our workshop. We'll get into their details later, but for now know that R is the programming language and RStudio is the development environment from which we will run R commands.

!!! warning "R and RStudio are installed separately"

    Note that R and RStudio are different programs and need to be installed separately, with R being installed first.

### Installing R

Please follow the instructions on [this page to install R](https://cloud.r-project.org/).

To begin, click the link for your operating system to bring up a list of files to download.

For **Windows** you will want to download the **base** install files.

For **Macs**, the file you download will depend on the processor in your computer.

* If you have an **M1 Mac** or higher, you will want the file **R-4.2.2-arm64.pkg**.
* If you have an **Intel Mac**, you will want the file **R-4.2.2.pkg**.

For **Linux**, please download the package appropriate for your distro.

After you have downloaded the file appropriate for your operating system, navigate to them and install the program as you would any other program on your computer. 

### Installing RStudio

Please follow the instructions on [this page to install RStudio](https://posit.co/download/rstudio-desktop/).

On the Rstudio install page, scroll down and select the file appropriate for your operating system and click to download.

After you have downloaded the file appropriate for your operating system, navigate to them and install the program as you would any other program on your computer.

If you have any trouble installing these programs, or experience any errors that prevent you from completing the installation, please let us know before class by replying to the email that you got with information about this workshop.

---

### Opening RStudio

Once you have **both R and RStudio** installed, navigate to the RStudio program on your computer and open the program. This should open an interface that looks something like this: 

![RStudio interface](img/RStudio.png)

!!! important "Be sure you can successfully open RStudio before class"

    If you have any trouble opening RStudio, or experience any errors that prevent you from opening the program, please **let us know before class** by replying to the email that you got with information about this workshop.

### Installing Packages

 For Days 2-4, we will use several **packages** that may not already be installed in your RStudio environment. You can try to install them before class to troubleshoot any issues or get help beforehand. Otherwise, we will walk you through installing them in class. If you already have these packages installed, it may be beneficial to make sure they are updated to the latest version.

In general, packages can be installed from the **Packages tab**in the RStudio panel in the lower right hand corner (default location). Once you click on this tab, you will see a list of packages already installed in your RStudio environment. To INSTALL a new package, click the "Install" button on the top left corner of the panel and search for the package name. To UPDATE an already installed package, click the "Update" button, also on the top of the panel, and again search for the package name. 

#### Package requirements by workshop day

Part 1 (day 1):

* No packages required

Part 2 (days 2 & 3):

* `[tidyverse](https://www.tidyverse.org/)`

Part 3 (days 3 & 4):

* `[tidyverse](https://www.tidyverse.org/)`
* `[cowplot](https://wilkelab.org/cowplot/articles/introduction.html)`
* `[viridis](https://cran.r-project.org/web/packages/viridis/vignettes/intro-to-viridis.html)`

#### Packag installation - Common problems

 Installing packages can be fraught with problems because everyone has different versions of things on their own computer. We are happy to help troubleshoot with you on the day of the workshop. If you experience problems installing packages before class, try to come a few minutes early for help. Otherwise, we will help you as best we can during the workshop.

Some common problems you may encounter: 

1. The `rlang` package is a dependency for many other packages and cannot be updated from within RStudio since it is always in use. To update this package, open the R interface (NOT RStudio) and use the `update.packages()` command. Again we will be happy to help with this if it is an issue. 

2. On Windows machines, you may be prompted to install the **RTools** dependency. Note that in most cases this can be ignored since we are using common packages that don't need to be built from source. But on the off-chance this needs to be installed it is done OUTSIDE of RStudio. We will be happy to help with this if it is an issue. 

---

## Workshop content

Workshop content is available below. Download the R Markdown (.Rmd) files for each day to do the excercises. After each day, we will make available the instructor version of the R Markdown file with the solutions to the exercises.

### Day 1: Introduction to R

Wednesday October 18th, 9:30 am - 12:30 pm, Location: [Biolabs](https://goo.gl/maps/7ngpNbkWEM5uZuap8) room 2062/2064 

* Opening RStudio and learning about its interface
* Executing R commands in the console
* Writing and running R scripts
* R objects and data types

[Download R Markdown file](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part1-student.Rmd){ .md-button } - [View instructor version](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part1.html){ .md-button }

### Day 2: Introduction to data manipulation with the tidyverse

Friday October 20th, 9:30 am - 12:30 pm, Location: [Biolabs](https://goo.gl/maps/7ngpNbkWEM5uZuap8) room 2062/2064 

* Installing and loading the tidyverse package
* Tibbles
* Filtering and manipulating data tables (tibbles)
* Piping

[Download R Markdown file](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part2-student.Rmd){ .md-button } - [View instructor version](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part2.html){ .md-button }

### Day 3: More tidyverse and introduction to data visualization with ggplot

Wednesday October 25th, 9:30 am - 12:30 pm, Location: [Jefferson Building](https://maps.app.goo.gl/2orhqJRo3djPfkCy6) room 453 

* Grouping and summarizing data
* Generating basic plots with ggplot
* Aesthetics and layers in ggplot
* Various plot types

[Download R Markdown file](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part3-student.Rmd){ .md-button } - [View instructor version](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part3.html){ .md-button }

### Day 4: More on ggplot

Friday October 27th, 9:30 am - 12:30 pm, Location: [CGIS South](https://goo.gl/maps/n2FAUngGYj8vKVCo9), S050 

* More plot types
* Colors and grouping data
* Multi-panel figures

[Download R Markdown file](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part4-student.Rmd){ .md-button } - [View instructor version](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part4.html){ .md-button }





