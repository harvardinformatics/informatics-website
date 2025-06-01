---
title: "Harvard Informatics Bioinformatics Tips Workshop"
subtitle: "Day 4: Loops, conditionals and scripts"
date: "November 17, 2023"
author: "Nathan Weeks, Gregg Thomas, Lei Ma, Tim Sackton"
output: 
  html_document:
    keep_md: true
---

Welcome to the fourth day of the [FAS Informatics](https://informatics.fas.harvard.edu/) [Bioinformatics Tips and Tricks Workshop](https://harvardinformatics.github.io/workshops/2023-fall/biotips/)!

If you're viewing this file on the website, you are viewing the final, formatted version of the workshop. The workshop itself will take place in the RStudio program and you will *edit the file while executing code in the terminal*. Please download the raw file [here](https://harvardinformatics.github.io/workshops/2023-fall/biotips/Biotips-workshop-2023-Day4-student.Rmd)

Today you'll learn more about how to write scripts, control the behavior of your scripts using loops and conditional statements, and more!

## Setting up our link to the data files  

As with yesterday, we'll create a *symbolic link* (analogous to a Windows *shortcut*) in your current working directory called "data4" that points to the workshop data directory.

> Run the following commands in the terminal window to create links to the files in our data directory in your own data directory:

```bash

mkdir -p data4
ln -s -f /n/holylfs05/LABS/informatics/Everyone/workshop-data/biotips-2023/day4/* data4
# ln: The Unix link command, which can create shortcuts to folders and files at the provided path to the second provided path
# -s: This option tells ln to create a symbolic link rather than a hard link (original files are not changed)
# -f: This option forces ln to create the link

ls -l data4
# Show the details of the files in the new linked directory

```

# Part 1: The For loop

We introduced scripting yesterday. If you need a refresher on how we developed our first script, the `data4` folder contains different iterations of "snp-density-*.sh" that step through the process. 

## Why we might want loops

Loops are useful if you want to repeat the same command multiple times, while changing something specific about that command each time. For example, on day 3 we counted the number of genes in the macaque annotation `.gff` file, but what if we wanted to know the number of genes in all the gff files across our data folders? Or what if we wanted to extract the different regions of the genome, like introns or exons from a `gff` file? Today we'll learn how to do those things using the "For" loop, which executes a sequence of commands once for each item in a list of items. 

> Run the following code block by copy-pasting it to your terminal to see a for loop in action. You can also write out the code in the terminal, and note how the prompt changes as you type a multi-line command. 

```bash

# a simple loop
for i in 1 2 3
do
  echo $i
done
# for: loops over a list of values
# i: this is the variable name of the current value in the list and can be used within the loop
# in: a keyword that precedes the list of values to loop over

```

> **Note:** bash also has `while` loops that execute the loop body while a condition evaluates to true.

## How to build a loop

The components of a loop are:

1. The `for` keyword
2. A variable name (can be any valid shell variable name, but try to make it descriptive and not misleading)
3. The `in` keyword
4. A list of elements to iterate over (there are many ways to generate this list, which we'll cover later)
5. The `do` keyword
6. The commands to run in the loop (indenting this section is optional, but makes it easier to read)
7. The `done` keyword

The `for` loop will iterate over the elements in the list, assigning each element to the variable name in turn. The commands in the loop will be run once for each element in the list. The "$" sign is used to access the value of the variable.
After the `for` loop, the variable will subsequently retain its value from the last iteration of the loop.

What is the thought process that goes into writing a loop? First, we start with a command that we want to repeat multiple times. Then, we think about what we want to change each time we run the command. This is the variable. Then, we think about what values we want to assign to the variable. This is the list of elements the loop will iterate over. Finally, we put it all together. 

When first testing out a loop, it's a good idea to make use of the `echo` command to see what your loop will do before it actually does it. 

> Run the below code to see how echo can be used to do a trial run of a loop.
    
```bash

for i in 1 2 3
do
  echo "some_command $i | another_command > $i-result.txt"
done
# for: loops over a list of values
# i: this is the variable name of the current value in the list and can be used within the loop
# in: a keyword that precedes the list of values to loop over

```

Let's find out how many exercises there are in each RMarkdown document (student version).

> **Exercise**: Using the steps above, write a loop that will print out how many exercises there are in each Rmarkdown document `data4/Biotips-workshop-2023-Day1-student.Rmd`, `data4/Biotips-workshop-2023-Day2-student.Rmd`, and `data4/Biotips-workshop-2023-Day3-student.Rmd`. You can use the `grep -c` command to count the number of matches to "Exercise" in a file. When iterating over file name, it is a good idea to encase the variable name in double quotes so that any weird characters such as spaces in the file name are parsed correctly. Write your solution in the code block below.

=== "Exercise"

    ```bash
    # The command we want to repeat is: grep -c 'Exercise'
    # The variable we want to change each time we run the command is: filename
    # The values we want to assign to the variable are: 
    # data4/Biotips-workshop-2023-Day1-student.Rmd 
    # data4/Biotips-workshop-2023-Day2-student.Rmd 
    # data4/Biotips-workshop-2023-Day3-student.Rmd
    # If we're unsure how it'll go, we can put echo in front of the command

    # Put your solution here:


    ```
=== "Solution"

    ```bash
    # The command we want to repeat is: grep -c 'Exercise'
    # The variable we want to change each time we run the command is: filename
    # The values we want to assign to the variable are: 
    # data4/Biotips-workshop-2023-Day1-student.Rmd 
    # data4/Biotips-workshop-2023-Day2-student.Rmd 
    # data4/Biotips-workshop-2023-Day3-student.Rmd
    # If we're unsure how it'll go, we can put echo in front of the command

    # Put your solution here:

    for filename in data4/Biotips-workshop-2023-Day1-student.Rmd data4/Biotips-workshop-2023-Day2-student.Rmd  data4/Biotips-workshop-2023-Day3-student.Rmd
    do
        grep -c 'Exercise' "$filename"
    done
    # for: loops over a list of values
    # i: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    ```

------

!!! Note
    **A note on using echo to test your code. Run the following two code chunks and compare the result:**

```bash

for filename in data4/Biotips-workshop-2023-Day2-student.Rmd
do
    echo "grep -c 'Exercise' \"$filename\" > $filename-count.txt"
done

```

```bash

for filename in data4/Biotips-workshop-2023-Day2-student.Rmd
do
    echo grep -c 'Exercise' "$filename" > $filename-count.txt
done

```

What happened here? In the first version, the full command was enclosed in double quotes, and treated as a string to print to the terminal (note the `\"` to *escape* the inner double quotes, and treat them as literal `"` characters within the string instead of terminating / starting a string). In the second version, the `echo` was only applied to the `grep`, the output of which was then redirected (with `>`) into the file `data4/Biotips-workshop-2023-Day2-student.Rmd-count.txt`. You can go to your `data4/` folder in the Files pane and view that text file. When using echo to test your code, be mindful of which part of your code you are echoing.

------

Now let's figure out a command to get the exercises themselves. Sometimes it's easier to build out a command outside the loop, working on a single file at a time, so let's start with just finding the exercises for the second day's file. 

> **Exercise**: Awk can be used to capture multiple lines based on a pattern. The syntax for that is `awk /start/,/end/ file-to-match`. Write a command that will print out the full exercise prompts in `data4/Biotips-workshop-2023-Day2-student.Rmd`. What should be your "start" and what should be your "end" in the awk command?  *Hint: there is an empty line after every exercise prompt.* Write your solution in the code block below.

=== "Exercise"

    ```bash

    ## An awk command that will print out all the exercises in the file data4/Biotips-workshop-2023-Day2-student.Rmd


    ```
=== "Solution"

    ```bash

    ## An awk command that will print out all the exercises in the file data4/Biotips-workshop-2023-Day2-student.Rmd
    awk '/Exercise/,/^`/' data4/Biotips-workshop-2023-Day2-student.Rmd
    # OR
    awk '/Exercise/,/^$/' data4/Biotips-workshop-2023-Day2-student.Rmd
    # awk: A command line scripting language command
    # '' : Within the single quotes is the user defined script for awk to run on the provided file

    ```

> **Exercise**: 
>
> 1. Incorporate the working `awk` command into a for loop, iterating over the same `.Rmd` files as before.
> 
> 2. Use `>>` to append the output to a file called `exercises.txt`. Where should you add this code? Write your solution in the code block below.

=== "Exercise"

    ```bash

    ## A for loop that extracts all the exercises from the RMarkdown files and appends them to a file called exercises.txt


    ```
=== "Solution"

    ```bash

    ## A for loop that extracts all the exercises from the RMarkdown files and appends them to a file called exercises.txt
    for filename in data4/Biotips-workshop-2023-Day1-student.Rmd data4/Biotips-workshop-2023-Day2-student.Rmd data4/Biotips-workshop-2023-Day3-student.Rmd
    do
        awk '/Exercise/,/^$/' "$filename" >> exercises.txt
    done
    # for: loops over a list of values
    # filename: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    ```

Now you can see how useful loops can be to process multiple files at once! 

## Adding wildcards to your loop specifications

Enumerating all the files in your for loop can get tedious and messy. Since some of our files all share the same extension, we can use wildcards to specify all the files that match that extension. Wildcards get processed before the loop is run so it essentially generates the list of files the loop iterates over. 

> Run the following code to see how wildcards work in a for loop:

```bash

for filename in data2/*.vcf
do
    echo $filename
done
# for: loops over a list of values
# filename: this is the variable name of the current value in the list and can be used within the loop
# in: a keyword that precedes the list of values to loop over

```

> **Note:** if the wildcard pattern does not match any existing path (file or directory) name, the pattern will not expand into a list, resulting in a string containing a literal `*`.
> E.g., the following results in "data2/*.bcf" being echoed:


```bash

for filename in data2/*.bcf
do
    echo $filename
done
# for: loops over a list of values
# filename: this is the variable name of the current value in the list and can be used within the loop
# in: a keyword that precedes the list of values to loop over

```

> **Exercise**: Create a for loop that prints out the path for all the `.Rmd` files we processed earlier. Write your solution in the code block below.

=== "Exercise"

    ```bash
    ## A for loop that prints out the path for all the .Rmd files we processed earlier


    ```
=== "Solution"

    ```bash

    for filename in data4/*student.Rmd
    do
        echo $filename
    done
    # for: loops over a list of values
    # filename: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    ```

## Using a loop in a script

Now that we've practiced making `for` loops directly in the command line, we can start writing them in scripts for added **reproducibility** and **portability**. In this section we'll walk you through how a script comes together conceptually. It starts with an idea for a single command that gradually gets too complicated to keep track of in your head.

In the last session, we used the `bedtools makewindows` function to generate a `.bed` file with the coordinates of the 100 kilobase windows in the scaffold for the Amazon molly genome. We can also generate `.bed` files for different subsets of the annotation we have for the Amazon molly: coding exons, introns, intergenic regions, UTRs. For example, to extract the exons from a `gff` file, we can use the following `awk` command:


```bash

awk 'BEGIN{OFS="\t"}; $3=="exon"{print $1, $4-1, $5}' data3/poeFor_NW_006799939.gff > exon.bed
# awk: A command line scripting language command
# '' : Within the single quotes is the user defined script for awk to run on the provided file
# > : The Unix redirect operator to write the output of the command to the following file

```

We can then repeat the command and substitute "exon" in both the awk and output bed for "CDS", "mRNA", or "gene", for a total of 4 different bed files. We could just copy and paste the command and change the file name, but that's not very efficient. This is a good candidate for a loop! Note that `awk`, by default doesn't have access to shell variables, but we can pass them to an `awk` script with the `-v` option. The syntax for that is: 

```
awk -v variable=$SHELL_VALUE 'normal awk command but variable will be the shell value' file-to-awk
``` 

> **Exercise**: Write a loop to create the 4 different bed files, but `echo` the command since we won't be running it just yet. Write your solution in the code block below. 
>
> NOTE: When using `echo` to display an `awk` command, some things may not display exactly how you think they should. This is because `awk` and `bash` (the terminal program) share some of the same syntax. For example, both `awk` and `bash` use the `$` to indicate variable names. When *evaluating* an `awk` command, the terminal knows to use the variable within `awk`. However, when using `echo` to display the `awk` command, the `$` is interpreted by `bash` instead. This can lead to unexpected behavior if, for instance, your `awk` command uses `$3`. If `$3` does not exist in your `bash` environment an empty string will be displayed by `echo`, even though the command would evaluate correctly in `awk`.
>
> We can get around this by **escaping** these shared syntactic characters using the `\` symbol. For example, `$3` will try to be evaluated by `bash`, but `\$3` will tell bash to instead literally use the "$" character.
>
> Keep this in mind when you display your commands with `echo`.

=== "Exercise"

    ```bash

    ## Write a for loop to create for different bed files, but only echo the command, do not run it

    ```
=== "Solution"

    ```bash

    for TYPE in exon CDS mRNA gene
    do
        echo "awk -v type=$TYPE 'BEGIN{OFS=\"\t\"}; \$3==type {print \$1, \$4-1, \$5}' data3/poeFor_NW_006799939.gff > $TYPE.bed"
    done
    # for: loops over a list of values
    # TYPE: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    ```

Since we're creating four `.bed` files, let's organize them by putting them all in a folder called `poeFor_beds`. So we want to add a command for making a folder before running this for loop using `mkdir -p poeFor_beds`. Now that the command is more than just one line, we should probably put it in a script. In RStudio create a new script from File --> New File --> Shell script. Name it `make-beds.sh`. Now copy and paste what we have so far into the script. Also add on `| bedtools sort -i - | bedtools merge` before the redirect to the `.bed` file. This will sort the bed file and merge overlapping intervals. You new script should look like the following:

> **Exercise**: Write a script called `make-beds.sh` that redirects the output of the for loop into a new directory called `poeFor_beds`. Also add in the sorting and merging of overlapping intervals. Write your solution in the code block below (and also modify it in your bash script).

=== "Exercise"

    ```bash

    ## Run the make-beds.sh script

    ```
=== "Solution"

    ```bash

    #!/bin/bash

    mkdir -p poeFor_beds

    for TYPE in exon CDS mRNA gene
    do
        awk -v type=$TYPE 'BEGIN{OFS="\t"}; $3==type {print $1, $4-1, $5}' data3/poeFor_NW_006799939.gff | bedtools sort -i - | bedtools merge > poeFor_beds/$TYPE.bed
    done
    # for: loops over a list of values
    # TYPE: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    chmod +x make-beds.sh
    ./make-beds.sh
    ## Run the make-beds.sh script

    ```

Now we can run the script by typing `bash make-beds.sh` in the terminal. You should see 4 new `.bed` files in the `poeFor_beds` folder. Great! But what if we want to run this script on a different gff file? We can add a variable for the gff file name and change the script to use that variable instead of the hard-coded file name.

> **Exercise**: Recall what we learned about running bash scripts with variables in the previous session. Add a variable for the gff file name and change the script to use that variable instead of the hard-coded file name. Modify your bash script with your code (and also write it in the code block below if you want).

=== "Exercise"

    ```bash

    ## Run the modified make-beds.sh script

    ```
=== "Solution"

    ```bash

    #!/bin/bash

    GFF=$1
    mkdir -p poeFor_beds

    for TYPE in exon CDS mRNA gene
    do
        awk -v type=$TYPE 'BEGIN{OFS="\t"}; $3==type {print $1, $4-1, $5}' $GFF | bedtools sort -i - | bedtools merge > poeFor_beds/$TYPE.bed
    done
    # for: loops over a list of values
    # TYPE: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over

    ```

Now we can run the script by typing `bash make-beds.sh data3/poeFor_NW_006799939.gff` in the terminal. Use `ls poeFor_beds` to confirm that there are 4 bed files in that folder. Note that the previous bed files were overwritten! Always use caution when running your scripts. In this case, we are fine with the previous files being overwritten. 

We are almost done; let's make a few more using `bedtools complement`, which reports all regions of the genome NOT in an interval, and `bedtools subtract`, which removes overlaps. For example, we don't have an `intergenic` feature in our GFF, but we can create one by getting everything that is not a gene. And we don't have a `UTR` feature or an `intron` feature, but we can get them by taking our exons and removing coding sequences (CDS) or by taking genes and removing exons.

> **Exercise**: Add the following lines to the end of your `make-bed.sh` script and re-run the script. 

```bash

bedtools complement -i poeFor_beds/gene.bed -g data3/poeFor_NW_006799939.fasta.fai > poeFor_beds/intergenic.bed
# bedtools: A suite of programs to process bed files
# complement: The sub-program of bedtools to execute
# -i: The input bed file
# -g:  A genome size file, which needs two columns, the scaffold/chromosome name and the size of that feature
# > : The Unix redirect operator to write the output of the command to the following file

bedtools subtract -a poeFor_beds/gene.bed -b poeFor_beds/exon.bed | bedtools sort -i - | bedtools merge > poeFor_beds/intron.bed
bedtools subtract -a poeFor_beds/exon.bed -b poeFor_beds/CDS.bed | bedtools sort -i - | bedtools merge > poeFor_beds/UTR.bed
# Two commands that subtract bed intervals in one file (-b) from another (-a) and pipe both with | and - into other bedtools commands and
# finally redirect to an output bed file.

```

Run `wc -l poeFor_beds/*.bed` to see how many lines are in each bed file. Note that here we have run a command on multiple files without an explicit loop, thanks to regex!

------

## Looping over lists of files

In this section we'll work on another script to continue our analysis of the Amazon molly genome. We'll write a script that will calculate the SNP density for each of the different bed files we created in the previous section. We already have code for this from the previous session, which is reproduced below. (If you don't have the file already, create a file named `snp-density.sh` and copy the below code into it.):

```bash

#!/bin/bash

BED=$1
VCF=$2

bedtools intersect -c -a $BED -b $VCF | awk 'BEGIN{snps=0; lens=0} {snps+=$4; lens+=$3-$2} END{print snps/lens}'

```

In order to run this, we have to specify a **bed** file and a **VCF** file as command line arguments. 

> Try running this script in your terminal using the command:

```bash

bash snp-density.sh poeFor_beds/exon.bed data3/poeFor_NW_006799939.vcf

```

It's not bad, but it still requires a lot of typing if we want to run this on the all the `.bed` files. Plus, we want to run this and essentially generate a report summarizing the results all in one place. To better wrap my brain around what kind of code I need, I like to write what I want in plain English first, then in **pseudocode**, and then in real code. **Pseudocode** is a programming word meaning a sketch of code that. It should be structured like the code you intend the write, but without worrying about grammar or syntax. **Pseudocode** is useful for creating a template that gets filled in with real code. It can also help identify logical flow errors and prevent laborious bug-fixing. 

Here's my plain English version:

"I want to loop over the an arbitrary list of bed files and run the snp-density-4.sh script on each one, and then print out the results in a file called snp-densities.txt. The script should be run like bash script-name.sh list-of-bed-files.txt vcf-file.vcf > snp-densities.txt"

Here's my pseudocode (I didn't necessarily write this up linearly, but it's presented here in a linear fashion):

```
bed_list=a list of bed files
vcf_file=a vcf file

for each bed_file in the bed_list:
    print out "the snp density for <bed_file> is:"
    run bedtools intersect on the bed_file and the vcf_file then pipe it to the awk statement to get the snp density
    print out "----" as a spacer
```

Now let's start translating the **pseudocode** into real code. We'll start with the for loop. We already know how to write a for loop, but we need to figure out how to get the list of bed files. How would you get a list (in the form of a text file) of the bed files we need process? 

> **Exercise**: Write a shell command (not script, this is too simple for a script) to get a list of the bed files we need to process and write it to `bed_files.txt`. Write your solution in the code block below. Use `wc -l bed_files.txt` to check the number of `.bed` files. Put your command in the code block below. 

=== "Exercise"

    ```bash

    ## A shell command to get a list of bed files and save it to a file


    ```
=== "Solution"

    ```bash

    ## A shell command to get a list of bed files and save it to a file
    ls poeFor_beds/*.bed > bed_files.txt

    ```

We've got the list of bed files we want. Let's write out the skeleton of the loop. Before when we were assembling the list of things to loop over, we simply typed them out (e.g. `for TYPE in exon CDS mRNA gene;`). However, now we want to get the output from a command, in this case `cat` to get the lines of the file and then pipe that to the for loop. We can do this by storing the output of that command in a shell variable and looping over that with this syntax:

```

for VAR in $(cat FILENAME)

```

This says that we're going to run the `cat` command on our file, but instead of displaying the contents of the file to the screen, we're going to substitute its output in our script using the `$()` (*command substitution*) syntax. In this case, we're not storing the output of `cat` in a named variable (e.g. `x=$(cat FILENAME)`), but instead using it directly in our `for` loop. Now, in our loop, each line in `FILENAME` will be iterated over and stored as `VAR`.

> **Exercise**: Write a for loop that iterates over each bed file in the `bed_files.txt` file and prints out the name of the bed file. Write your solution in the code block below.

=== "Exercise"

    ```bash

    ## A for loop that prints out the name of the files in bed_files.txt

    ```
=== "Solution"

    ```bash

    ## A for loop that prints out the name of the files in bed_files.txt
    for BED in $(cat bed_files.txt)
    do
        echo $BED
    done
    # for: loops over a list of values
    # BED: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over
    # $(cat bed_files.txt): this runs the cat command on the bed_files.txt file and uses it as input to the loop

    ```

Now we have all the parts we need to create our script.

> **Exercise**: Write a script called `snp-density-5.sh` that takes as input a file of bed files and a vcf file and finds the snp density of each bed file within the vcf. Write your solution in the code block below (and also modify it in your bash script). I've copied over the pseudocode to help you out.

=== "Exercise"

    ```bash
    # bed_list=a list of bed files
    # vcf_file=a vcf file

    # for each bed_file in the bed_list:
    #    print out "the snp density for <bed_file> is:"
    #    run bedtools intersect on the bed_file and the vcf_file then pipe it to the awk statement to get the snp density
    #    print out "----" as a spacer
    ```
=== "Solution"

    ```bash

    # bed_list=a list of bed files
    # vcf_file=a vcf file

    # for each bed_file in the bed_list:
    #    print out "the snp density for <bed_file> is:"
    #    run bedtools intersect on the bed_file and the vcf_file then pipe it to the awk statement to get the snp density
    #    print out "----" as a spacer

    #!/bin/bash

    BEDFILES=$1
    VCF=$2

    for BEDFILE in $(cat $BEDFILES)
    do
      echo "SNP density for $BEDFILE:"
      bedtools intersect -c -a $BEDFILE -b $VCF | awk 'BEGIN{snps=0; lens=0} {snps+=$4; lens+=$3-$2} END{if(lens > 0){print snps/lens}}'
      echo "---"
    done
    # for: loops over a list of values
    # BEDFILE: this is the variable name of the current value in the list and can be used within the loop
    # in: a keyword that precedes the list of values to loop over
    # $(cat bed_files.txt): this runs the cat command on the bed_files.txt file and uses it as input to the loop


    ```

> Use `chmod +x snp-density-5.sh` to make the script executable. 
>
> Then let's run the script in the terminal:


```bash

bash snp-density-5.sh bed_files.txt data3/poeFor_NW_006799939.vcf > snp-densities.txt

```

You should see a file called `snp-densities.txt` in your data3 folder. Let's take a look at it using `cat snp-densities.txt`. Congratulations! You've made a working script that can be reused or just kept as a record of how you processed your data. Can you think of ways in which the script might be improved?

-------

# Part 2: Conditional statements

## if statements

In this section, we'll get into some more advanced bash scripting concepts. We'll learn how to use **conditional statements** to control the flow of our scripts. **Conditional statements** can allow your script to make decisions based on the results of a command or the value of a variable, making it more responsive. Here is a simple example of a conditional statement:

```bash

FILE=bed_files.txt

if [[ -f "$FILE" ]]
then
    echo "File $FILE exists."
fi
# if: a conditional statement which evaluates the expression contained in [[]] as true or false and executes the subsequent lines only if true

```

This conditional statement is made up of the following components:

1. The `if` keyword
2. A command to execute (in this case, a *conditional expression* enclosed in `[[` `]]`).
3. The `then` keyword
4. The commands to run if the `if` command's *exit status* is zero
5. The `fi` keyword

The `if` keyword starts the conditional. The conditional expression you're checking is enclosed in the double square brackets. In this case, the `-f` checks if a file exists and the expression evaluates to true if it does. The `then` keyword starts the commands that need to be run if the statement is true. Here we're just printing to the terminal a string that confirms that the file named `$FILE` exists. The `fi` keyword ends the conditional. If the file doesn't exist, nothing happens.

> **Note:** you may see scripts that use `[` instead of `[[` for conditional expressions.
> This older syntax is standardized and more portable to other (non-bash) shells, though it supports only a subset of conditional expressions supported by `[[`.

An *exit status* is a small integer value returned returned by a command to its caller upon completion.
The `if` statement interprets an exit status of 0 for its command to mean "true", and non-zero to mean "false".
The `[[` command exits with status 0 if its conditional expression evaluates to true; otherwise, it exits with status 1.

> The shell variable `$?` contains the exit status of the last command executed.
> Try copying/pasting each of the following lines individually, noting the exit status echoed to the screen for each (note the use of semicolons instead of newlines to separate statements for brevity):

```bash

true; echo $?
false; echo $?
[[ -f bed_files.txt ]]; echo $?
[[ -f bed_files.txt.nonexistent ]]; echo $?

```

As observed in the above code block, the `true` and `false` shell commands silently exit with status 0 and non-zero, respectively.
For other commands, a zero exit status indicates "success", and a non-zero exit status indicates an error occurred.

```bash
if ls
then
  echo "ls succeeded (exit status 0)!"
fi

if ls some-nonexistent-file
then
  echo "should not see this!"
fi

# Note the use of the ! ("not") operator to negate the exit status of the command:
if ! ls some-nonexistent-file
then
  echo "uh oh, ls failed!"
fi
```

Some commands assign different exit statuses to different error conditions; see the program's documentation for details (e.g., issue `man ls` and check the "Exit status" section near the bottom).

> **Exercise**: Write a conditional statement that checks if the file `data3/poeFor_NW_006799939.vcf` exists and prints out the header. Write your solution in the code block below.

=== "Exercise"

    ```bash

    ## Write a conditional statement that checks if a VCF file exists and prints out the header
    # data3/poeFor_NW_006799939.vcf
    ```
=== "Solution"

    ```bash

    ## Write a conditional statement that checks if a VCF file exists and prints out the header
    FILE=data3/poeFor_NW_006799939.vcf

    if [[ -f "$FILE" ]]
    then
        bcftools view -h "$FILE"
    fi
    # if: a conditional statement which evaluates the expression contained in [[]] as true or false and executes the subsequent lines only if true

    ```

There are some particularly useful conditional tests built in to bash that let you check file properties (see the complete list [here](https://www.gnu.org/software/bash/manual/html_node/Bash-Conditional-Expressions.html)):

`-e filename`
: returns *True* if `filename` exists as a file or directory or symlink

`-f filename`
: returns *True* if `filename` exists and is a regular file, not a directory or symlink

`-s filename`
: returns *True* if `filename` exists and has a size > 0

`-d filename`
: returns *True* if `filename` is a directory

You can also check string properties:

`-z string`
: returns *True* if `string` is empty or null (0-length)

`-n string`
: returns *True* if `string` is not empty/null

## Why we might want conditionals

You might want to process a file only if it exists, or you might want to run different commands depending on the size or number of files. In a larger workflow, you can imagine that sometimes, you're cleaning a FASTQ file and all the reads get thrown out leaving you without an output cleaned FASTQ. You might want to be able to check for that condition and have the script report it to you and skip the subsquent steps. For the purposes of this workshops, we're going to be using conditionals for basic error checking in our `snp-density-5.sh` script. To do that, we will need to introduce if-else statements.

## if-else statements

The if-else statement is similar to the if statement, but it has an additional set of commands to run if the boolean value is false. Here's an example:

```bash

FILE="data3/poeFor_NW_006799939.vcf"

if [[ -f "$FILE" ]]; then
    echo "$FILE exists."
else 
    echo "$FILE does not exist. Skipping subsequent steps."
fi
# if: a conditional statement which evaluates the expression contained in [[]] as true or false and executes the subsequent lines only if true
# else: a conditional statement which follows an if statement and executes the subsequent lines only if that statement was false

```

> **Exercise**: Modify your `snp-density-5.sh` script to include an if-else statment so that it checks if the `.bed` file exists. If the file exists, the script should continue. If the file does not exist, the script should print a message saying it doesn't exist. Test your script by modifying `bed_files.txt` to include a file that doesn't exist. Write your solution in the code block below (and also modify it in your bash script).

=== "Exercise"

    ```bash

    ## Run the modified snp-density-5.sh script

    ```
=== "Solution"

    ```bash

    #!/bin/bash

    BEDFILES=$1
    VCF=$2

    for BEDFILE in $(cat $BEDFILES)
    do
        if [[ -f "$BEDFILE" ]]
        then
            echo "SNP density for $BEDFILE:"
            bedtools intersect -c -a $BEDFILE -b $VCF | awk 'BEGIN{snps=0; lens=0} {snps+=$4; lens+=$3-$2} END{if(lens > 0){print snps/lens}}'
            echo "---"
        else
            echo "$BEDFILE does not exist. Skipping this file."
        fi
    done

    ```

This is fine, but we aren't checking if the VCF file exists as well. We want to modify the script to check if the VCF file exists and then exit the script if it doesn't. We can do this using the `exit` command. The `exit` command exits the script and returns a status code. By convention, a status code of 0 means the script exited successfully and any other number means there was an error. Here is an example of using an exit command:

> Copy the below code into a file named `exit.sh`, make it executable with `chmod +x exit.sh` and run it with `bash exit.sh` to see how the exit command works. **(Do not copy and paste it directly into terminal or you will exit the current terminal session and respawn a new session)**:

```bash

#!/bin/bash

for i in 1 2 3 4 5
do
  if [[ $i -eq 3 ]]
  then
    echo "Exiting because i is $i"
    exit 1
  else
    echo "i is $i"
  fi
done

```

> **Exercise**: Modify your `snp-density-5.sh` script to check if the VCF file exists and exit the script if it doesn't. Test your script by giving running it like `bash snp-density-5.sh bed_files.txt fake_vcf.vcf` Write your solution in the code block below (and also modify it in your bash script). Hint: you may want to check if the VCF does NOT exist, which will save you an else statement. Also think about where you want to place this if statement to reduce the number of times the script performs the check. 

=== "Exercise"

    ```bash

    ## Run the modified snp-density-5.sh script

    ```
=== "Solution"

    ```bash
    #!/bin/bash

    BEDFILES=$1
    VCF=$2

    if [[ ! -f "$VCF" ]]
    then
        echo "$VCF does not exist. Exiting script."
        exit 1
    fi

    for BEDFILE in $(cat $BEDFILES)
    do
        if [[ -f "$BEDFILE" ]]
        then
            echo "SNP density for $BEDFILE:"
            bedtools intersect -c -a $BEDFILE -b $VCF | awk 'BEGIN{snps=0; lens=0} {snps+=$4; lens+=$3-$2} END{if(lens > 0){print snps/lens}}'
            echo "---"
        else
            echo "$BEDFILE does not exist. Skipping this file."
        fi
    done

    ```

# Putting it all together for a robust script

We've come a long way since the our first one-liner script `snp-density-1.sh`! Let's copy `snp-density-5.sh` to a new version called `snp-density-final.sh` where we'll put on the finishing touches that make the script easier to use, read, and monitor. 

## Using if statements to print helpful usage messages

Imagine you come back to this script 6 months later, vaguely recalling that by running it, you can generate a report on SNP densities. However, you don't remember exactly how it works so you just naively run `bash snp-density-final.sh`. You just get the uninformative error below:

```
 does not exist. Exiting script.
```

To save future you some confusion, we can use an if statement to print out how the script is to be used if no arguments are given to it. The syntax for checking if a variable is empty is `-z $VARIABLE`.

> **Exercise**: Use and `if` statement to check whether both `BEDFILE` and `VCF` are given as arguments. Modify your script to print out a usage message if they are not and exit the script. If they are, then proceed with the rest of the script. Write your solution in the code block below (and also modify it in your bash script).

=== "Exercise"

    ```bash

    ## Run the snp-density-final.sh script

    ```
=== "Solution"

    ```bash
    #!/bin/bash

    BEDFILES=$1
    VCF=$2

    if [[ -z $BEDFILES || -z $VCF ]]
    then
      echo "Usage: ./snp-density-final.sh <file of bed files to process> <vcf file>"
      exit 1
    fi

    if [[ ! -f "$VCF" ]]
    then
        echo "$VCF does not exist. Exiting script."
        exit 1
    else
        for BEDFILE in $(cat $BEDFILES)
        do
            if [[ -e $BEDFILE ]]
            then
                echo "SNP density for $BEDFILE:"
                bedtools intersect -c -a $BEDFILE -b $VCF | awk 'BEGIN{snps=0; lens=0} {snps+=$4; lens+=$3-$2} END{if(lens > 0){print snps/lens}}'
                echo "---"
            else
                echo "File $BEDFILE does not exist. Skipping!"
            fi
      done
    fi

    ```

**Bonus note** on `elif` statements. Sometimes, you may want to check for multiple exclusive conditions consecutively. In those cases, using only if else can get complicated because each `if` statement needs to be ended with a `fi` and those are hard to keep track of. Imagine a script that extracts certain metadata from different file types. If the file is a `.vcf`, you might want to use `bcftools` to process it. If the file is a `.bam`, you might want to use `samtools`, etc. If the file is neither, you might want to print an error message. Here is an example of how `elif` followed by an `else` to catch everything else can be used to manage that scenario:

> You do not need to run the following code, just observe how it is structured.

```bash

#!/bin/bash

FILE=$1

if [[ $FILE == *.vcf ]]
then
  echo "Processing VCF file with bcftools..."
  # bcftools commands here
elif [[ $FILE == *.bam ]]
then
  echo "Processing BAM file with samtools..."
  # samtools commands here
else
  echo "Unknown file type. Please provide a .vcf or .bam file."
  exit 1
fi

```

## Documenting your script

In the last section we made our script more user friendly by adding a usage message if not all of the variables were given as arguments. We can also make our script more readable by adding a detailed description of how the script works in the file itself using comments. We highly encourage everyong to annotate their code with comments. It makes it easier for others (and future you) to understand. In the case of a script, documentation typically means adding a description of what the script does, what the inputs are, what the outputs are, and the author of the script to the top of the file. Here's an example of what that might look like:

> **Exercise**: Add a description of what the script does, what the inputs are, what the outputs are, and the author of the script to the top of your `snp-density-final.sh` script. Write your solution in the code block below (and also modify it in your bash script).

```bash
#
# This script takes a file of bed files and a VCF file and calculates average SNPs per base for each bed file
# Usage: ./snp-density-final.sh <file of bed files to process> <vcf file>
#
```
