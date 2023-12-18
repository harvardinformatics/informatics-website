---
title: "Harvard Informatics Bioinformatics Tips Workshop"
subtitle: "Day 2: Bioinformatics command line tips and file formats"
date: "March 23, 2023"
author: "Gregg Thomas"
output: 
  html_document:
    keep_md: true
editor_options: 
  chunk_output_type: inline
---

<style type="text/css">

pre {
  overflow-x: scroll
}

pre code {
  white-space: pre;
}

/* This makes the output blocks scroll horizontally in HTML renders */

</style>

Welcome to the second day of the [FAS Informatics](https://informatics.fas.harvard.edu/) [Bioinformatics Tips & Tricks workshop](https://harvardinformatics.github.io/workshops/2023-fall/biotips/)!

If you're viewing this file on the website, you are viewing the final, formatted version of the workshop. The workshop itself will take place in the RStudio program and you will *edit and execute the code in this file*. Please download the raw file [here](https://harvardinformatics.github.io/workshops/2023-fall/biotips/Biotips-workshop-2023-Day2-student.Rmd)

Today we're going to continue our tour and explanation of common genomics file formats and their associated tools by talking about interval files, that is files which indicate regions of a genome (.bed files, .gff files).

We'll be learning about how to view and manipulate these files using both the native commands present in the Linux command line as well as tools developed specifically for these file formats.

## Setting up our link to the data files  

As with yesterday, we'll create a *symbolic link* (analogous to a Windows *shortcut*) in your current working directory called "data" that points to the workshop data directory.

> Run the following commands in the terminal window to create links to the files in our data directory in your own data directory:

```bash

mkdir -p data2
ln -s -f /n/holylfs05/LABS/informatics/Everyone/workshop-data/biotips-2023/day2/* data2
# ln: The Unix link command, which can create shortcuts to folders and files at the provided path to the second provided path
# -s: This option tells ln to create a symbolic link rather than a hard link (original files are not changed)
# -f: This option forces ln to create the link

ls -l data2
# Show the details of the files in the new linked directory

```

# Command input and output

Just to begin, I wanted to take a second to re-iterate a few concepts we learned yesterday. In general, the aim of a lot of the **commands** we run is to take text in a file that is formatted in a specific way and manipulate or process that text. This is central to the Unix philosophy:

**formatted text -> command -> processed text**

## How do commands output text?

1. By default, most commands simply **print their output to the screen**. While this doesn't immediately make sense when processing such large files, it is integral to be able to perform some other operations namely, **piping** and **redirecting**.

2. Many times, instead of displaying output to the screen we will want to save the output to a file. Natively, Unix has the **redirect** operator, which is the `>` character. Note that this is distinct from the literal string `">"`, which we see as the header character in **FASTA** files. Rather, this is part of the command being run:

```
command > output_file.txt
```

If we are using `grep` to search for header lines in a **FASTA** file like we did yesterday, we may see a command like this:

```
grep '>' file.fa > headers.txt
```

In this example, `'>'` and `>` are doing 2 different things. The string literal `'>'`, being quoted, is the string we are searching for in our file with `grep` -- it is an input argument to our `grep` command. The second, unquoted `>` is the Unix redirect operator, which is placed at the end of the command and tells the shell to redirect the output into the provided file.

Many programs will also have built-in options to redirect output to a file. A common option is `-o filename.txt`, which would tell a command to write output to that file rather than display it on the screen. We saw this yesterday with `samtools`, e.g.:

```
samtools view -b -o output.bam input.sam
```

which would convert `input.sam` to **BAM** format and save it to `output.bam`. While `-o` is a common output option, it is not universal and its important to read the documentation for each tool you use to see the output options.

3. The other way output can be used in a Unix command is by **piping** it to another command with the `|` operator. Remember that commands simply take text as input and process it in someway that is output to the screen. If the output of one command is compatible with another, then they can be strung together:

```
command1 input_file.txt | command2
```

Here, we've specified the input file for `command1`, but not for `command2`. Instead, the `|` operator says *take the output of `command1` and use it as the input of `command2`*. This is an extremely powerful way to construct basic pipelines and we did this a bit yesterday.

**Pipes** and **redirects** can be combined:

```
command1 input_file.txt | command2 > output_file.txt
```

Here, the text in `input_file.txt` is first processed by `command1` and that processed text is **piped** to `command2` as input. `command2` does its processing of the text and then this is **redirected** to `output_file.txt`, which should now have the text processed by both commands.

Note that if the program you run has a `-o` option to save output that you use, you can no longer **pipe** that output to another command:

```
command1 -o output_file.txt input_file.txt | command2
```

This will result in `output_file.txt` containing only the text processed by `command1`. Since the text from `command1` was written to the file, there is nothing to **pipe** to `command2`, which may or may not display an error.

# Bed files

Today we'll talk about **bed** files. Bed files are used to indicate regions of a genome with each line in the file representing one region. The bed format is an extremely flexible format -- the regions contained within it can represent anything. In it's most basic and common form it is also an extremely *simple* format, consisting of three columns of text separated by a tab character. The first column represents the chromosome or assembly scaffold of the region, while the second indicates the starting coordinate and the third indicates the ending coordinate.

Bed files might have the `.bed` extension, and while it is best practice to use a file extension that properly describes the format of a file it is not required. Any 3 column tab delimited file that has the columns we described is a **bed** file.

## A warning about coordinate systems
We will talk about several different file types today that are used to reference locations in the genome. Unfortunately for all of us, for various reasons different file types use different coordinate styles. Bed files, which we will talk about first, use 0-based coordinates and do not include end base in the interval (technically, this is called a right-open interval). So in a bed file, an interval that includes the first 100 bases of a chromosome would have start=0, end=100. 

Gff files in contrast use 1-based coordinates and do include both the start and the end base in the interval (technically, this is called a closed interval). So in a gff file, an interval that includes the first 100 bases of a chromosome would have start=1, end=100. 

It is worth noting that while the 1-based closed format of GFF files is more intuitive to read, it does suffer some issues. In particular, it is impossible unambiguously encode a 0-length feature in a GFF file. 

- Check [this post on BioStars](https://www.biostars.org/p/84686/) for a simple illustration of 0- vs. 1-based coordinate systems.

## Bed file example - Macaque structural variants

Today we'll be working with a bed file that contains calls of structural variants (e.g. large deletions and duplications of segments of the genome; *abbreviated SVs*) from a small population of rhesus macaques (if you attended the R workshop earlier this month you might already be familiar with this dataset). [Rhesus macaques](https://en.wikipedia.org/wiki/Rhesus_macaque) are small, Old-World monkeys that are widespread across southern and eastern Asia and are a common model organism for the study of human disease and primate evolution. [We sequenced these genomes to study the evolution structural variation over different timescales](https://doi.org/10.1093/molbev/msaa303).

First thing we should do is *look at our data*. We can do this a couple of ways here. With the RStudio setup with the VDI, we can just use our file browser on the right to navigate to the path of the file and open it in the text editor (this panel).

However, if we want to see things in a more Unix way, we can use a command to directly display the contents of the file in our Terminal.

> Run the following command in the Terminal below to view the bed file containing macaque SVs.

**Note that whenever you see the > character followed by green text, this is an exercise or action to be done by you!** 

```bash

less -S data2/macaque-svs-filtered.bed

```

`less` is a file viewing program that lets us look at parts of a file without loading the whole thing into memory. You can scroll through the file with `<up arrow>` and `<down arrow>` to move line-by-line, or with `<spacebar>` and `b` to move by page (one screen of text). The `-S` flag simply means do not wrap the lines to fit on the screen, so we can also scroll left and right with `<left arrow>` and `<right arrow>`. Press `q` to quit and return to the Terminal interface.

So what do we see? We see, as described, three columns of text indicating the chromosome, start coordinate, and end coordinate of each SV (row). We also see a **fourth column** with a bunch of extra information. The fourth column in a bed file is an optional column meant to provide each region with a unique ID. In this case, the unique ID is just a long string of separate pieces of information delimited by a colon (`:`) character. In a way, I've made this column a sort of catch-all for other information not included in the base **bed** format (e.g. SV length, SV type), which is a common strategy in genomic file formats. Most of this information we can ignore, but I will point out that TYPE of each SV is encoded as a string, with deletions being `<DEL>` and duplications being `<DUP>`. We may use this information later.

In addition to this optional fourth column for an ID, **bed** files have several other common pieces of information that could be encoded in extra columns. Most of the time these extra columns are ignored by the tools that process bed files, but sometimes specific columns are used.

For more information on bed files and these extra columns, visit the following links:

- [Description of bed files from bedtools](https://bedtools.readthedocs.io/en/latest/content/general-usage.html)
- [Description of bed files from UCSC](https://genome.ucsc.edu/FAQ/FAQformat#format1)

# Summarizing SVs from the command line

So imagine we get this **bed** file from our collaborator who has called these SVs, and the first thing we should do is get a general idea about the variants called. What can we do from the command line?

The most basic thing we'll want to know is how many structural variants have been called. Recalling that each line in a bed file represents one region, which in this case means one structural variant, we can simply count the number of lines in the file with the wc command.

> Run the command below to count the number of SVs in the bed file. How many SVs are there?

```bash

wc -l data2/macaque-svs-filtered.bed
# wc: the Unix word count command
# -l: tells wc to only return the line count

```

Cool! We also may want to known how many of these SVs are deletions and how many are duplications. We can figure that out with `grep`.

> **Exercise**:
> Write commands that use `grep` to count the number of deletions and duplications separately. Remember that SV type is encoded in the fourth column of our bed file. Execute these commands in the Terminal and then record them in the code block below.

=== "Exercise"

    ```bash

    ## Count the number of deletions
    # data2/macaque-svs-filtered.bed

    ## Count the number of deletions


    ## Count the number of duplications
    # data2/macaque-svs-filtered.bed

    ## Count the number of duplications

    ```
=== "Solution"

    ```bash

    ## Count the number of deletions
    grep -c "DEL" data2/macaque-svs-filtered.bed
    ## Count the number of deletions


    ## Count the number of duplications
    grep -c "DUP" data2/macaque-svs-filtered.bed
    ## Count the number of duplications

    ```

# `awk` basics

So we have a lot more deletions than duplications. If we didn't have reason to believe that deletions are more common than duplications (which we think they are) we may want to ask our collaborator to re-check their calls. But we can do some more checking ourselves too. Maybe, on average, the deletions being called are smaller events than the duplications so it would be expected that there are more of them. To check whether that is the case, we could get the *average length of deletions and duplications* in our bed file. The first step of that is to get the **length** of each SV.

Yesterday, we started to learn about `awk`, which is a scripting language that is interpreted in the Unix shell. Basically what this means is that we can use `awk` much the same way as if we were programming in a text editor. `awk`'s appeal for us is that it is set up to automatically read through and process text files, line by line, which is a common task in bioinformatics. We could achieve the same functionality by writing a Python or R script, but because those are not integrated into the shell we would waste time writing code to read and write files. `awk` does that automatically, so for simple file operations it is an extremely useful to for bioinformaticians to have.

Yesterday you learned the basic syntax of an `awk` command:

```
awk '{ action; other action }' input_file.txt
```

This means that `awk` reads `input_file.txt` line by line, and for each line performs both `action` and `other action`. A semi-colon (`;`) is used to de-limit separate actions.

The simplest `awk` program we could right then, would be something like this.

> Run the code below. What happens?

```bash

awk '{}' data2/macaque-svs-filtered.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

Here, `awk` has read through our bed file, but nothing is displayed to the screen because we didn't code any actions for it to perform.

The most basic action we can code for an `awk` program is the `print` command.

> Run the code below:

```bash

awk '{print}' data2/macaque-svs-filtered.n20.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

This time, now that we've given the instruction for `awk` to `print` we see each line displayed on the screen. This is a good demonstration of `awk`, but doesn't really do anything we couldn't do before. We can view the contents of files with `cat`, `less`, `head`, `tail`, etc. `awk`, however, also splits each **record** (line) into **fields** (columns) based on some character delimiter (tab by default). This naturally turns our text file into a data table to manipulate right in the shell.

In `awk`, the **fields** or columns are identified by number and a special character, the dollar sign `$`, to indicate we want to access that column. So, for instance, if I wanted to access only the third column from a given **record**, I could do so with `$3`.

> Run the code below to use `awk` to print the only the third column from the bed file with macaque SVs. We call `head` first to not overflow the screen with output:

```bash

head data2/macaque-svs-filtered.n20.bed | awk '{print $3}'
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

Another functionality of `awk`, since it is a scripting language is that there are basic operations it can perform on the input data. For instance, given two input columns that are numeric, `awk` can add, subtract, multiply, and divide them with the `+`, `-`, `*`, and `/` operators.

> **Exercise**:
> Use `awk` to print the length of each SV. Once it works, copy it to the code block below:

=== "Exercise"

    ```bash

    ## Use awk to print the length of each SV
    # data2/macaque-svs-filtered.n20.bed

    ## Use awk to print the length of each SV

    ```
=== "Solution"

    ```bash

    ## Use awk to print the length of each SV
    awk '{print $3 - $2}' data2/macaque-svs-filtered.n20.bed
    ## Use awk to print the length of each SV

    ```

## A note on data types

As a programmer (we are coding now!), **one of the most important things I can tell you about programming is to always remember what data types you are operating on!**

We won't get into it too much here, but briefly, you should know about **data types**. **Data types** are the way different pieces of information are encoded. `3` is an **integer**. `"hello world"` is a **string** of characters. `"3"` is a **character**. This is important to remember because different functions and operators may perform different actions depending on the **data type** input to them, or they might not work at all with the wrong data type. For example, with algebraic operators like addition (`+`), `3 + 3` is a perfectly valid instruction to write. But what does `3 + "hello world"` mean? Different programming languages may perform differently in this situation, some by erroring out and some by doing something you may not expect and not leaving any trace that something is wrong. And different programming languages generally have different data types.

The command above worked because both column 3 and column 2 contain only **integers**, so `awk` correctly subtracts their values when the `-` operator is provided between them. The other columns in our bed file, however, contain character strings.

> Run the code block below to try and perform an algebraic operation (`-`) on a column made up of integers and a column made of strings. What happens? What did you expect to happen?

```bash

awk '{print $3 - $1}' data2/macaque-svs-filtered.n20.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

This is only printing out the third column unchanged. `awk` is pretty good about **not** throwing errors, so if you didn't catch this, either because of a typo or because you thought column 1 also contained integers, you may move forward in your analysis and get some strange results you'd struggle to explain later.

All of which is to say (and to re-iterate) that you should **always remember what data types you are operating on!**

# **Variables** in `awk`

In programming, **variables** are names given to pieces of information, allowing the information to be used later on in the program. The column numbers used by `awk` with the `$` notation are variables that are updated as every record is read.

`awk` has several default **variables** that are initialized when the command is run:

- `FS`: field separator (default: white space)
- `OFS`: output field separator, i.e. what character separates fields when printing
- `RS`: record separator, i.e. what character records are split on (default: new line)
- `ORS`: output record separator
- `NR`: a running count of the number of records that is updated after each record. At the end of the program `NR` will equal the total number of records (lines in the file by default)

Most of these pertain to how `awk` separates **records** and **fields**. Like any other **variable** in a program, its value can be accessed and overwritten. For instance, we can change the **field separator** (`FS`) to be something other than white space (e.g. a tab character).

> Run the block below to change the FS variable to colon (`:`) and print out the first 3 fields. How is this different from the default behavior?

```bash

awk 'BEGIN{FS=":"}{print $1,$2,$3}' data2/macaque-svs-filtered.n20.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

Now, the first field includes everything in the line up to the first colon in the last tab separated column. This is most of the line. 

`NR` is also important. Rather than dealing with how fields and records are read, it simply counts the number of records as they are read.

> Run the code below to see how the value of `NR` changes for each record read:

```bash

awk '{print NR}' data2/macaque-svs-filtered.n20.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

# `awk` **patterns** and custom variables

Yesterday you learned a bit about **regular expressions** and how to use them with `grep`. Well, in actuality, `awk` is also using **regular expressions** to decide which **records** to display. By default, the blank regular expression (because none is provided) matches every line in the file, so every line is displayed. However, you can use `awk` similarly to `grep` to display and process lines that only match some pattern.

> Run the code below to use awk to display only lines that represent duplications:

```bash

awk ' /<DUP>/ {print}' data2/macaque-svs-filtered.n20.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

This should be equivalent to the following:

```bash

grep "<DUP>" data2/macaque-svs-filtered.n20.bed
# grep: The Unix string search command
# "<DUP>": The string to search for in the provided file

```

However, with `awk`, we can also process the output from the same command.

> **Exercise**:
> Use a single `awk` command to print the length of every duplication in the macaque SV bed file.

=== "Exercise"

    ```bash

    ## Use awk to print the length of every duplication
    # data2/macaque-svs-filtered.n20.bed

    ## Use awk to print the length of every duplication

    ```

=== "Solution"

    ```bash

    ## Use awk to print the length of every duplication
    awk '/<DUP>/ {print $3 - $2}' data2/macaque-svs-filtered.n20.bed
    ## Use awk to print the length of every duplication

    ```

We can also print lines that contain information in a certain column using the same `$` notation as before to refer to the column. For instance, we can print only SVs on the X chromosome.

> Run the following code to print only lines of the **bed** file where the first column is "chrX":

```bash

awk ' $1=="chrX"{print};' data2/macaque-svs-filtered.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

## `BEGIN` and `END`

`awk` has two special patterns, `BEGIN` and `END`. These patterns are followed by instructions that are to be performed either before (`BEGIN`) or after (`END`) `awk` reads every record in the file. Recall that, by default, `awk` performs the specified actions on every **record** (line) in the input file. These two keywords allow us to perform summary tasks both before and after the records are read and processed.

> Run the code below to use `awk` to only print the total number of records (without using `NR`):

```bash

awk ' BEGIN{sum=0} {sum++} END{print sum}' data2/macaque-svs-filtered.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file

```

To break this down, we told `awk` that we want it to read every record in the bed file, but BEFORE doing that set the value of a new **variable** called `sum` to 0. Then, as every record is read, increment `sum` by 1 with the `++` operator. Finally, after all records have been read, print out the value of `sum`, which should now be the total number of lines in the file. Remember that `awk` already has a **variable** that does this, `NR`.

In addition to the `++` operator, which adds 1 to a variable, it is useful to know about the `+=` operator, which adds whatever is on the right side of the equation to the variable on the left side. So we could have written the code above as `{sum += 1}`. The `++` operate is a shortcut when we just need to incremete a variable, but the `+=` operator allows us to increment a variable by more than 1, or even by another variable (e.g., `{sum += $1}` would keep a running total of the first column of a file). 

This command introduces another key concept in `awk` programs: **user-defined variables**. Here, `sum` is not part of `awk`'s default namespace -- we create and manipulate this **variable** on our own. We could have easily called it something else (e.g. `random_data=0`), but `sum` seems to be a good descriptive name for its purpose. `record_count` would also be a good name for this.

# Average SV length with `awk`

Great! Now we've got some new `awk` knowledge. Let's try and put it all together to calculate the *average length of all SVs* in our bed file.

> **Exercise**:
> Write a single `awk` command that calculates the average length of the SVs in the bed file. This command will need to:
> 1. Calculate the length of each SV
> 2. Add the length to a running total
> 3. After reading all records, divide the final total length of all SVs by the total number of SVs in the file (hint: remember `NR`!)  
>
> Once it works, copy it to the code block below:

=== "Exercise"

    ```bash

    ## Write awk command to calculate average length of SVs
    # data2/macaque-svs-filtered.bed

    ## Write awk command to calculate average length of SVs

    ```
=== "Solution"

    ```bash

    ## Write awk command to calculate average length of SVs
    awk 'BEGIN{len_sum=0} {cur_len=$3-$2; len_sum = len_sum + cur_len} END{print len_sum / NR}' data2/macaque-svs-filtered.bed
    # Solution 1: explicit but long

    awk 'BEGIN{len_sum=0} {len_sum = len_sum + $3-$2} END{print len_sum / NR}' data2/macaque-svs-filtered.bed
    # Solution 2: calculate length without storing it in a intermediate variable

    awk '{len_sum = len_sum + $3-$2} END{print len_sum / NR}' data2/macaque-svs-filtered.bed
    # Solution 3: no need to initialize the summing variable, len_sum, since awk will start it at 0

    awk '{len_sum += $3-$2} END{print len_sum += NR}' data2/macaque-svs-filtered.bed
    # Solution 4: the += shortcut

    awk '{len_sum += $3-$2} END{if(NR > 0){print len_sum / NR}}' data2/macaque-svs-filtered.bed
    # Solution 5: checking to make sure the file is not empty (NR > 0)

    awk 'BEGIN{len_sum=0} {len_sum += $3-$2} END{if(NR > 0){print len_sum / NR}}' data2/macaque-svs-filtered.bed
    # Solution 6: back to initializing len_sum to be slightly more explicit

    ## Write awk command to calculate average length of SVs

    #awk '{length += $3-$2} END{print length / NR}' data2/macaque-svs-filtered.bed
    # This won't work ... why?
    # length() is a function in awk, so you cannot use "length" as a variable name

    ```

Ok, so we now have the average length of ALL SVs. What about deletions and duplications separately?

> **Exercise**:
> Calculate the average length of duplications and deletions separately (2 commands). This can be done in several ways using the tools we've taught (i.e. `grep`, `awk`, pipes (`|`)) or just with a single `awk` command per SV type. Are deletions or duplications longer on average?

=== "Exercise"

    ```bash

    ## Calculate the average length of deletions
    # data2/macaque-svs-filtered.bed

    ## Calculate the average length of deletions


    ## Calculate the average length of duplications
    # data2/macaque-svs-filtered.bed

    ## Calculate the average length of duplications

    ```
=== "Solution"

    ```bash

    ## Calculate the average length of deletions
    # data2/macaque-svs-filtered.bed
    awk 'BEGIN{num_dels=0} /<DEL>/{len_sum += $3-$2; num_dels+=1} END{if(num_dels > 0){print len_sum / num_dels}}' data2/macaque-svs-filtered.bed
    # awk solution

    grep "<DEL>" data2/macaque-svs-filtered.bed | awk '{len_sum += $3-$2} END{if(NR > 0){print len_sum / NR}}'
    # grep and pipe solution
    ## Calculate the average length of deletions


    ## Calculate the average length of duplications
    # data2/macaque-svs-filtered.bed
    awk 'BEGIN{num_dups=0} /<DUP>/{len_sum += $3-$2; num_dups+=1} END{if(num_dups > 0){print len_sum / num_dups}}' data2/macaque-svs-filtered.bed
    # awk solution

    grep "<DUP>" data2/macaque-svs-filtered.bed | awk '{len_sum += $3-$2} END{if(NR > 0){print len_sum / NR}}'
    # grep and pipe solution
    ## Calculate the average length of duplications

    ```

# bedtools

We can do a lot of simple processing of **bed** files (and genomic files in general) with native bash commands like `grep`, `awk`, `wc`, etc. However, there are a lot of tasks that require software (commands) built specifically for these types of files. For bed files (and other interval files), **bedtools** is a great program. It has a wide range of functions for working with these files, and is particularly powerful when you are interested in the overlap between regions in two files.

We'll only have time to go over a small number of **bedtools** functions in this workshop, so be sure to check out the bedtools website for more in-depth documentation on all its functions:

[bedtools website](https://bedtools.readthedocs.io/en/latest/index.html)

## bedtools getfasta

Given a set of genomic regions in a **bed** file, one common task you may want to accomplish is to get the *sequences* contained within those intervals from the genome. **bedtools** can do this with the `bedtools getfasta` command. You can type `bedtools getfasta -h` in the Terminal below to see some documentation about this command. To do this, you will need:

1. The bed file with regions of interest.
2. The whole genome FASTA file from which the coordinates in the bed file are derived.
3. A sequence index (`.fai` file) of the input genome -- though bedtools will create this automatically if it isn't found.

We've provided the genome file for you. So let's get the sequences of our macaque SVs in **FASTA** format.

> Run the code below to extract the sequences of the macaque SVs in the bed file in FASTA format:

```bash

bedtools getfasta -fi data2/rheMac8.fa -bed data2/macaque-svs-filtered.bed -fo macaque-svs-filtered.fa
# bedtools: A suite of programs to process bed files
# getfasta: The sub-program of bedtools to execute
# -fi: The genome fasta file as input
# -bed: The bed file as input
# -fo: The desired output fasta file

head macaque-svs-filtered.fa
# Display the first few lines of the new file with head

```

Let's break this command down since there is a lot going on. Here is a table that explains each option:

| Command line option | Description |
| ------------------- | ----------- |
| `bedtools` | Call the main `bedtools` interface |
| `getfasta` | The sub-program in the `bedtools` program to run |
| `-fi` | The path to the input whole genome sequence file in **FASTA** format |
| `-bed` | The path to the input **bed** file |
| `-fo` | The desired name of the file to write the extracted sequences to in **FASTA** format |

We saw this a bit yesterday as well, but this is another framework for running commands. While it still follows the Unix philosophy (**formatted text -> command -> processed text**), the Unix commands we've seen up to this point generally act on a single file, the use of multiple command line options allow us to specify multiple input files, here a **FASTA** file of sequences and a **bed** file of intervals. Also, like Unix commands, the default action of `bedtools` is to simply print output to the screen. This output can be **redirected** to a file with `>`, but here we also have an option (`-fo`) to tell the program directly to print output to that file instead.

The use of a main program (`bedtools`) and a sub-program (`getfasta`) is also a norm among bioinformatics tools.

The downside of having multiple input files is that it makes **piping** with `|` difficult. 

> Try running the code block below to **pipe** output from `grep` to `bedtools getfasta`:

```bash

grep chr10 data2/macaque-svs-filtered.bed | bedtools getfasta -fi data2/rheMac8.fa -fo macaque-svs-filtered-chr10.fa
# grep: The Unix string search command
# chr10: The string to search for in the provided file
# | : The Unix pipe operator to pass output from one command as input to another command
# bedtools: A suite of programs to process bed files
# getfasta: The sub-program of bedtools to execute
# -fi: The genome fasta file as input
# -bed: The bed file as input
# -fo: The desired output fasta file

```

This doesn't work because `bedtools getfasta` *requires* the `-bed` option to be specified. It doesn't know that we've given it the bed formatted input through a pipe.

Luckily, many bioinformatics tools have a shortcut help us **pipe** output to a specific input option.

## Using `-` to pipe

For tools that require an input file to be specified with a command line option (like `-bed` above), we may still want to **pipe** the output from another command to it. We can often do so with the `-` shortcut. Basically, when this is provided as an option in lieu of an actual path to a file, many commands read from the process's *standard input* (which in a pipeline would receive the *standard output* of the previous command in the pipeline) instead of a file.

```bash

grep chr10 data2/macaque-svs-filtered.bed | bedtools getfasta -fi data2/rheMac8.fa -bed - -fo macaque-svs-filtered-chr10.fa
# grep: The Unix string search command
# chr10: The string to search for in the provided file
# | : The Unix pipe operator to pass output from one command as input to another command
# bedtools: A suite of programs to process bed files
# getfasta: The sub-program of bedtools to execute
# -fi: The genome fasta file as input
# - : Another way to pipe the output from the previous command to the input of the current command when an input option is required
# -bed: The bed file as input
# -fo: The desired output fasta file


head macaque-svs-filtered-chr10.fa
# Display the first few lines of the new file with head
```

Did you spot the difference between this command and the one above it?

Here, all we've added is `-bed -`, which tells `getfasta` that the input for the `-bed` option will come from the output of the previous `grep` command.

**Note that not all command-line tools accept this shortcut, but most of the ones we cover today do. The special file /dev/stdin can be used in most environments for commands that do not support `-` in this manner.**

> **Exercise**:
> Write a command that extracts the sequences of only the duplications in the **bed** file from the macaque genome. Output these sequences to a file called `macaque-svs-filtered-dups.fa`.
> **BONUS**: Figure out how to keep the SV name (4th column of **bed** file) as the header of the sequences in the output **FASTA** file (Hint: check the help menu of `bedtools getfasta`!).

=== "Exercise"

    ```bash

    ## Use grep and bedtools to extract sequences of duplications only
    # data2/macaque-svs-filtered.bed
    # data2/rheMac8.fa

    ## Use grep and bedtools to extract sequences of duplications only

    head macaque-svs-filtered-dups.fa
    # View the first few lines of the file you created

    ```
=== "Solution"

    ```bash

    ## Use grep and bedtools to extract sequences of duplications only
    # data2/macaque-svs-filtered.bed
    # data2/rheMac8.fa
    grep "<DUP>" data2/macaque-svs-filtered.bed | bedtools getfasta -fi data2/rheMac8.fa -bed - -name -fo macaque-svs-filtered-dups.fa
    ## Use grep and bedtools to extract sequences of duplications only

    head macaque-svs-filtered-dups.fa
    # View the first few lines of the file you created

    ```

## bedtools merge

Like we said, `bedtools` has a ton of features -- we could write a whole workshop about it. And I wanted to give one more example before we move on. Something else we might want to do with the regions in a bed file would be to **merge** ones that are overlapping or within some distance of each other. For instance, we may think the method we used to call SVs may be slightly inaccurate and is calling the same polymorphism as separate mutations in different individuals, so we want to merge overlapping events.

For this we can use `bedtools merge`. There is one catch, however.

> Run the code below to see what happens when we run `bedtools merge` on the bed file with macaque SVs:

```bash

bedtools merge -i data2/macaque-svs-filtered.bed
# bedtools: A suite of programs to process bed files
# merge   : The sub-program of bedtools to execute

```

The input bed file must be **sorted**! There are a couple of ways we could do this. If you look at the [documentation](https://bedtools.readthedocs.io/en/latest/content/tools/merge.html) for `bedtools merge`, they suggest using the native Unix `sort` command. However, **bedtools** itself also has a `sort` command. Let's try that.

> Run the code below to sort the bed file with macaque SVs and then merge overlapping SV calls:

```bash

bedtools sort -i data2/macaque-svs-filtered.bed | bedtools merge > macaque-svs-filtered.sorted.merged.bed
# bedtools: A suite of programs to process bed files
# sort: The sub-program of bedtools to execute
# -i: The input bed file
# | : The Unix pipe operator to pass output from one command as input to another command
# bedtools: A suite of programs to process bed files
# merge: The sub-program of bedtools to execute
# > : The Unix redirect operator to write the output of the command to the following file

wc -l data2/macaque-svs-filtered.bed
wc -l macaque-svs-filtered.sorted.merged.bed
# Use wc -l to count the number of un-merged SVs in the original file and the number after merging

```

So we merged a few hundred calls. Note that because `bedtools merge` only requires one input file, we can default back to the standard Unix **piping** procedure without having to use the `-` shortcut (though we still could specify `-i -`).

Of course, in actuality we would only want to merge duplications with other duplications and deletions with other deletions.

> **Exercise**:
> In the code block below, write a command that merges only duplications with other duplications. Save the result in a file called `macaque-svs-filtered-dups.sorted.merged.bed`.
> **BONUS**: Adjust the settings to merge any duplications within 1000bp of each other as well as directly overlapping (Hint: Check the help menu of `bedtools merge`!).

=== "Exercise"

    ```bash

    ## Use the tools you've learned to merge only duplications with other duplications
    # data2/macaque-svs-filtered.bed

    ## Use the tools you've learned to merge only duplications with other duplications


    # Count the number of lines in the original file and the new file to confirm we merged some duplications

    ```
=== "Solution"

    ```bash

    ## Use the tools you've learned to merge only duplications with other duplications
    grep "<DUP>" data2/macaque-svs-filtered.bed | bedtools sort | bedtools merge -d 1000 > macaque-svs-filtered-dups.sorted.merged.bed

    ## Use the tools you've learned to merge only duplications with other duplications

    grep -c "<DUP>" data2/macaque-svs-filtered.bed
    wc -l macaque-svs-filtered-dups.sorted.merged.bed
    # Count the number of lines in the original file and the new file to confirm we merged some duplications

    ```

# End of Day 2

That's it for day 2! Join us next week to learn about GFF files, VCF files, and shell scripts.


