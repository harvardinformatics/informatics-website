---
title: "Harvard Informatics R Workshop"
subtitle: "Part 1: R Basics"
date: "October 18, 2023"
author: "Adam Freedman, Gregg Thomas, and Lei Ma"
output: 
    html_document:
      keep_md: true
---

<style>
    .md-sidebar--secondary { order: 0; }
    .md-sidebar--primary { display: none; }
    /* This hides the Navigation sidebar and moves the TOC sidebar to the left in HTML renders */
</style>

Welcome to the first part of the [FAS Informatics](https://informatics.fas.harvard.edu/) [Intro to R workshop](https://harvardinformatics.github.io/workshops/2023-fall/r/)! 

If you're viewing this file on the website, you are viewing the final, formatted version of the workshop. The workshop itself will take place in the RStudio program and you will *edit and execute the code in this file*. Please download the raw file [here](https://harvardinformatics.github.io/workshops/2023-fall/r/R-workshop-2023-Part1-student.Rmd)

## What is R?

R is a functional programming language, which means that most of what one does is apply functions to objects. Functions perform various operations on the objects, with particular functions constructed to work with particular kinds of objects. For example, the *sum()* function works with numeric data. 

# Using R within RStudio

#### R is not RStudio and vice versa.

Though you cannot have RStudio without R. So what the heck is RStudio?

First, a little motivation.

## Plain text data tables and text editors

A central task in data science is the need to interact with and analyze *plain text formatted data tables*. Sometimes these tables will be nice, but often times they will be incomplete or mis-formatted in some way, so we need to be able to edit them on the spot. Oftentimes these tables, in plain text, indicate rows of data by lines and columns of data with some designated separator character, commonly comma (`,`) with files that have `.csv` **extensions** or a tab (encoded as `\t` but literally `   `) with files that have `.tsv` or `.tab` **extensions**. Though note that the **extension** does not necessarily define how the data is formatted -- the agreement between the file's extension and its format is not enforced by the machine and is only meant to be descriptive. You may sometimes find a tab delimited file with the `.txt` extension, or even with `.csv`! Best practices dictate that the extension match the formatting, but best practices are not always followed.

So, since tables are how we store our data, we need some way to load them into memory to view, manipulate, and analyze them. That's where R comes in handy. However, the default R interface leaves much to be desired. A **text editor** is the main way to interact with data and code, and there are many of them out there. For other data analysis software or programming languages, there is no general consensus on which text editor to use to view files. However, for R, RStudio's utility is unparalleled.

## RStudio is an IDE

RStudio is actually more than a text editor. It is an integrated development environment (IDE), that integrates the R programming language and allows one to simultaneously execute R commands, view the objects available for processing with R commands, build and execute R scripts (sets of commands), view plots generated from data, and has additional features that can increase one's productivity when using R and generally make life easier. 

The RStudio interface is divided into 4 *panes* or windows. Sometimes some of these are minimized, so if you don't see all 4, let us know and we can help get them to show up.

At the top of the window, you will see a set of menu items like **File**, **Edit**, **Help**, etc. that should be roughly familiar to you as they are likely used by programs across your OS. For instance if we click on **File**, we see some typical *New File*, *Save*, *Save as...*. However, there are also some RStudio specific menu items, like **Code** or **Plots** that will have functions specific for RStudio. In general we won't worry too much about these today.

Below that you'll see some of the common functions found in those menus represented as graphical buttons. For instance, the white rectangle with a green circle and white + sign are the same as the *New File* command found under the **File** menu.

1. Below this, we come to the first of the 4 **panes** of the RStudio interface in the upper left, the **text editor**. This is where we can open **plain text** files to view and edit them. These files could be raw data (though R has a better way to View these) or scripts that contain code to process data. We'll get more into this in a bit -- you'll be spending a lot of time in this **text editor** in these workshops.

2. Below that, on the lower left is the **R Console** panel. This contains an interactive interface for the current session. What that means is that you can type R commands here and they will be executed immediately. You may also see a tab labeled **Terminal** which is an instance of your operating system's command line and allows you to run OS commands from RStudio.

3. In the top right you should see the RStudio environment panel, which contains several tabs, most importantly the **Environment** tab. This shows all objects, data, and functions currently loaded into memory and available to manipulate in the current session. The graphical buttons also allow for some basic manipulation of the environment.

4. Finally, in the lower right you will see a panel that contains several often-used and helpful tabs tabs (as well as some never used; not sure what to call this panel). Here is a summary of the important tabs:

- **Files** is a graphical file browser that displays the files on your computer. We will not use this very often as we will load data and files into RStudio programmatically.
- **Plots** will display any plots that you generate in the current session.
- **Packages** shows the list of **packages** (third-party code repositories) currently available to load, and indicates which ones are loaded with a check. Here you can also install and update packages.
- **Help** will display help information for any function or package you have in RStudio. This is a really great tool for when you need a quick (though often technical) reminder of what something does. You can search for a function or package from this panel, or you can type it in the **Console** in the lower left to have it displayed here by using the `?` and `??` operators followed by the function name.

> In fact, let's look up a function's help documentation from the console now. It's ok if we don't know the function yet, this is just to demonstrate running a command in the console. So select the **Console** so your cursor is blinking and type the following and hit enter:

```r
?mean
```

**Note that whenever you see the > character followed by green text, this is an exercise or action to be done by you!** 

Great, your first R command of the day!

In general, R has very good built-in documentation that describes what functions do.

To get help about a particular function, use `?` command followed by the function name, like so:

```r
?ls
```

This shows that, in R, the function `ls()` returns a character vector with the names of all the objects in a specified environment (by default, the set of user-defined objects and functions). This can be especially helpful if you need to reproduce your R environment later one.

> In the **Console** below, the `ls()` function and display every object currently loaded in the RStudio session:

If you are not exactly sure of the function name, you can perform a search with double question marks, `??`:

```r
??mean
```

# A note on terminology

So in the section above and throughout this workshop we use a lot of context dependent terms. For instance, you probably know what the word "command" means in general usage, but in the context of programming it has a specific meaning that may not be obvious. This brings up an important point I try to remember when teaching. When learning a new skill or set of skills there's usually a whole new vocabulary to learn that goes along with it. What makes it difficult is that those teaching the new skill will use this vocabulary, and since they are so familiar with it they oftentimes won't even realize people don't know what the words they're using mean in the context of the new skillset. 

In an attempt to offset this unintentional language barrier we provide tables with some contextual definitions of terms we may use throughout the workshop at the following link: 

https://harvardinformatics.github.io/workshops/2023-fall/r/terms.html 

If you see hear any terms you think should be added to these tables, please let us know.

# R is a **functional** programming language

Great. So what is a function?

A **function** is a generalized piece of code that takes **arguments**, which are pieces of information or data. The function acts on the input information and then **returns** some other piece of information or data. Sometimes what is **returned** is completely different than what was input to the function as an argument, and sometimes it is just another version of the input.

In R, most functions are indicated by trailing parentheses, `()`, which is where **arguments** are provided to the function. For example, a **function** with no arguments given may look something like this:

```r
my_function()
```

**Arguments** are provided either by the order they are input or by the argument name. For instance, some functions may take any arguments in any order, like this:

```r
my_function(value1, value2, value3)
```

While some functions may require the input value to be **assigned** to a specific argument with the equals sign `=`:

```r
my_function(argument1=value1, argument2=value2)
```

# Functions take **objects** as input arguments

In programming, we often store pieces of information in our program as **variables** that can be manipulated later in the program. R calls these pieces of information **objects**. 

In R, we create objects by assigning arbitrary variable names with values with the following syntax:

```r
<object name> <- <value(s) we are assigning to object name>
```

For instance, we may type:

```r
x <- 10
```

which means we now have an **object** called `x` and that object has a value of the number `10`. We can now refer to `x` elsewhere in our environment or program to access the numeric value `10`

Knowing this, a better description of a **function call** than above would be the following:

```r
my_function(argument1=object1, argument2=object2)
```

Here we've simply replaced the word "value" with "object" to give a clearer example of what R functions are working with.

# Functions also **return** objects

Given some input objects, a function will perform some operations on them and this oftentimes results in a **return** value. That is, the function has manipulated the input information which results in a **new object** containing the new information.

The default action when a function is called in the **Console** is to simply **print**, or display, the new information to the screen. Let's try running a very simple function to see this in action.

> In the **Console** below, run the `getwd()` function. What happens when you do this? 
> How many arguments did the function take?

So this should simply print out the directory in which the R session currently exists (not necessarily the directory of this file).

What if we want to refer to this directory later in our program? Well, **functions return objects** and we know how to **assign objects to variable names** with the `<-` operator, so let's do that with the `getwd()` function.

> In the **Console** below, run the following command:

```r
cur_dir <- getwd()
```

What happened? Instead of **printing**, or displaying, the new object to the screen we have now saved the object as `cur_dir`. Now if we need it later in our program we can simply refer to `cur_dir`!

Ok, well what if we want to display it now? If you're working in the **Console** you can simply type the name of the object to display it. But we can use the `print()` function and provide our `cur_dir` object as an **argument**.

> In the **Console** below, run the following command:

```r
print(cur_dir)
```

# Data Types

**One of the most important things I can tell you when programming is to always remember what data types your objects are!**

Why is this important? Because the **functions** you use will depend on **the data type of your objects!** In many cases, if you provide a function with an incorrect data type, you will see an error and your code will not execute. If you do get an error while running a function and ask for help, I can almost guarantee my first question to you will be, *"What data type is this object, and what data type does the function expect?"*

In R, to begin with, we really only need to learn about two data types: **numeric** and **character**.

## Numeric types

- Numeric data types are numbers and are defined simply by typing the number.

> In the **Console** below, assign an object name `x` to the numeric value of `10`.

In general, **numeric** objects are manipulated by algebraic operators to perform math.

> In the **Console** below, run the following command:

```r
x + 10
```

Other basic algebraic operators include `-` for subtraction, `*` for multiplication, and `/` for division.

## Character types

- Character data types are any *string of alphanumeric characters*. Characters are defined by typing the characters within `"double"` or `'single'` quotes. 

> In the **Console** below, assign an object name `my_char` to the character string of `"Hello world!"`, then display the value of the new object with the `print()` function.

**Character** objects can be used to label or group data into categories.

**Note that the character "1" is different from the numeric 1!!**

> In the **Console** below, run the following command:

```r
my_char + 10
```

What happened? Why?

## Ascertaining types with the `class()` function

Like we learned about above, an R object has a **type**, depending upon the contents of the object. For example, we can determine what **type** x is by using the `class()` function. 

> In the **Console** below, run the following command:

```r
class(x)
```

In this case, `x` is numeric.

## Manipulating objects and storing the result

Again, we can manipulate objects as well with operations depending on their **type**. 

> In the **Console** below, run the following commands:

```r
x
x+5
x*2
x
```

Note that the value of `x` is not modified here. **We did not save the output to a new object, so it is simply displayed on the screen.**

If we want to **update** the value of `x`, we need to use our assignment operator. 

> In the **Console** below, run the following commands:

```r
x
x <- x+5
x
```

# Data structures

Oftentimes, especially when working with large datasets, it is inefficient to refer to and perform operations on a single piece of data as a single object at a time. In other words, we want to organize our data such that multiple pieces of information can be manipulated at once. To do this we use **data structures**, which are simply methods for organizing multiple pieces of information.

In R, **data structures are also objects** and we can assign them to variables as we would with a single piece of information with the `<-` operator.

# Vectors

The most basic data structure we'll learn about is the **vector**. A vector is just a one dimensional compilation of information **of the same type**.

We can create a **vector of numeric values** as follows. 

> In the **Console** below, run the following command:

```r
v1 <- c(1,2,3,4,5)
```

The v1 object now represents the output of the *function* `c(1,2,3,4,5)` (c, for **c**ombined, combines elements into a vector)

In this case, the vector is comprised of numeric elements, and if you check the class of v1 it should say as much. 

> In the **Console** below, run the following command:

```r
class(v1)
```

Let's display the contents of v1. 

> In the **Console** below, run the following command:

```r
print(v1)
```

It is important to remember that while vectors can contain multiple pieces of information, all of those individual pieces must be of the **same type**. R has some default behaviors when a vector with multiple **types** is defined.

> Run the following command in the **Console** to create a new vector and then run the `class()` function on it:

```r
new_vec <- c(1, 2, "hello")
```

> What **type** are the individual elements we input to the vector? What **type** is this vector? Why?

### Vectors have **length**

Importantly, vectors have a **length** attribute, which is simply the number of individual pieces of data contained in them. The **length** of a vector can be ascertained by the `length()` function.

> What does the `length()` function return when our vector `v1` is given as an argument?

# Running R commands in scripts

Thus far we've executed our R commands interactively through the **R Console** in the panel of RStudio below the text editor. Using the **Console** is a great way to quickly manipulate or view data or objects, but it isn't conducive to executing a lot of commands, or executing commands more than once (though you can cycle through your command history with the up arrow).

In order to reproducibly run R commands we would want to write a **script**. A **script** is a plain text file that contains multiple commands for a given programming language, one per line. When the script is **executed** or **run**, all the commands within it are executed in order by the specified programming language (in this case R).

Let's take all the commands we've executed in the console so far and instead put them in a script and execute them there.

> 1. First, click on the **New File** button in the upper left (the white rectangle with the white + sign in a green circle) or click the **File** menu and select **New File**. In either instance, a list of file types that RStudio is familiar with will pop up. Select **R Script**. This should bring up a blank file in the text editor (that will obscure your view of this file). You can switch between open text files in the text editor panel by clicking on the tabs near the top of the panel.

> 2. Next, copy the commands we've run up until now and paste them into the new file. Here are the commands in one chunk for convenience (you don't need to copy the triple ticks [```] for the script):

```r
getwd()
x<-10
class(x)
x
x+5
x*2
x
x<-x+5
x
v1<-c(1,2,3,4,5)
class(v1)
print(v1)
```

> 3. Now click the **Source** button in the top right of the text editor panel. 

What happens? You should see in the **Console** that all of the commands have been executed in order, with commands that display output printing that output to the Console below the command. Note that when output is displayed a *line number* is also displayed (e.g. `[1]`) to help keep track of multi-line output. We don't have any multi-line output, so we only ever see `[1]`.

> 4. Another way to execute the commands in the script is to highlight them with your cursor and clicking the **Run** button in the top right of the text editor panel. Try it!

> 5. Finally, the main benefit of scripts is that you can save your scripts and execute them again in the exact same way later. To do this, you can either click the **File** menu and then **Save As...**, click the image of the disk below the Menu, OR type *ctrl+s*. Any of these should bring up your computer's file browser to save the file, similar to how you would save a document in another program. Save this file somewhere as *first_script.r*.

With a saved file, you also have the option to **Source on Save**. This means that anytime you save this file (e.g. with *ctrl+s*), the script will also be **executed**. This is the easiest way to run scripts in RStudio, though be careful: if you simply want to save your progress on a large script that takes a long time to run, un-check this box before you save. 

> 6. For now, check the box and save the file with *ctrl+s*. What happened?

The behavior now should be slightly different. The only output we see is from the `print(v1)` command. That's because, while executing commands interactively in RStudio simply typing the object name displays it to the screen, when executing a script a `print()` statement is necessary.

> 7. Add `print()` statements to the other lines of the script we want to display output when executed. For example, replace `get()` with `print(getwd())`, or `x` with `print(x)`. Source the script again by saving the file. Now what happens? You should see more output in the **Console**.

Congratulations on writing your first R script (of this workshop, at least)!

# RMarkdown and code blocks

The above file is a pure R script. It will only take R commands and execute them all at once.

This file, and the other files we'll be using in this workshop, are **R Markdown** files. You'll notice several things about this file that differ from the R script we just made. First, the file extension is **.Rmd** rather than **.r**. You'll also see that this text has some different formatting and coloring that the R script. This is because an **R Markdown** file is capable of formatting plain text for viewing and writing and executing code. This makes it a great file format for keeping a lab notebook for reproducible science or even for teaching a workshop! **R Markdown** files can also be **knit**, meaning the text will be formatted and the code will be run and output displayed and formatted and everything will be compiled into a single file, either HTML, PDF, or LaTeX. Conceivably, one could write a whole paper or book with **RMarkdown**. Check out more about R Markdown formatting [here](https://r02pro.github.io/rmd-text-formating.html).

Code is written and executed in R Markdown with **code blocks**, which are delineated by the backtick character (\`). Each code block can have a language specified (in our case we will exclusively use `r`) as well as options specific to that block. Here is an example of an R code block in this R Markdown file:


```r
getwd()
```

```
## [1] "/Users/leima/Github/workshops/2023-fall/r"
```

```r
x<-10
class(x)
```

```
## [1] "numeric"
```

```r
x
```

```
## [1] 10
```

```r
x+5
```

```
## [1] 15
```

```r
x*2
```

```
## [1] 20
```

```r
x
```

```
## [1] 10
```

```r
x<-x+5
x
```

```
## [1] 15
```

```r
v1<-c(1,2,3,4,5)
class(v1)
```

```
## [1] "numeric"
```

```r
print(v1)
```

```
## [1] 1 2 3 4 5
```

These are the same commands we ran before, and that we put in our script. Notice how, within the **code block** the text coloring is the same as it was in our script. This tells us that RStudio knows that this block should be interpreted as code.

The great thing about R Markdown is that this code can be executed right here, within the document. 

> In the code block above, find the green triangle in the upper right hand corner and click it. 

What happened? The output appeared right below the code block!

We can also run this code block by placing our cursor in the code block and typing *ctrl+shift+enter*. Try it! 

> Run the code block above by placing your cursor in the code block and typing the *ctrl+shift+enter* key combination.

Using *ctrl+enter* we can run only the line that the cursor is on.

There are also many options for running code blocks under the **Run** button in the top right of the text editor.

**From now on in these workshops, we'll be executing our code in *R Markdown code blocks* like this, so if you have any questions please let us know now.**

# REMINDER: Objects have types

When constructing objects, it is important to remember, as we have demonstrated above that all objects have a **type**. Object types are a complex topic and we are only going to scratch the surface today. To slightly simplify, all data objects in R are either atomic vectors (contain only a single type of data), or data structures that combine atomic vectors in various ways. It is also important to note that there are restrictions as to what R functions can be applied to which types. For example, we cannot perform mathematical operations on **mixed numeric and character types**.

> What happens when you try to run the code blocks below?


```r
a <- "A"
a * x
```

nor can we perform addition **character** types.


```r
b <- "B"
a + b
```

There are in fact R functions for "pasting" together characters, for example if you wanted to take two variables in a data set representing different experimental treatment types, and combine them into a composite variable. But more about that later...

# Mathematical operations with vectors

One of the main advantages of R is its ability to perform operations and run functions **on data structures like vectors** (without needing to write a loop). 

Let's create a few objects objects to demonstrate this.

> Run the code in the block below to store several pieces of data as objects:


```r
x <- 10
x
```

```
## [1] 10
```

```r
w <- c(1,2,3,4)
w
```

```
## [1] 1 2 3 4
```

> 1. What **data type** is `x`?
> 2. What kind of **data structure** is `w`?
> 3. What **data type** is `w`?

One can easily perform mathematical operations with *numeric* objects.

> Run the code block below to do some math between a single number (`x`), referred to as a "scalar", and a vector:


```r
vector_plus_scalar <- w + x
vector_plus_scalar
```

```
## [1] 11 12 13 14
```

```r
vector_times_scalar <- w * x
vector_times_scalar
```

```
## [1] 10 20 30 40
```

Notice what happens when performing operations with objects of different **lengths**. R is **recycling the shorter object (in this case `x`) to perform element-wise operations with w**. The above demonstrates this with a single numeric value `x` (essentially a numeric vector of length 1) and a vector with length > 1, `w`. However, we can also perform operations on vectors of different lengths with this **recycling** behavior.

> In the code block below, create a new vector, `q`, such that the result of the operation `q * w` will be `c(-1, 2, -3, 4)`:


```r
## Create a new vector with c()
q <- c(-1,1)
## Create a new vector with c()  
  
q * w
```

```
## [1] -1  2 -3  4
```

In this case, q is being recycled, first being multiplied element-wise to the first two elements in w, then to the second two. 

If the length of the longer vector isn't a factor of the shorter vector, this type of operation will produce an error. Be aware of this recycling behavior, as sometimes it can lead to data analysis mistakes that don't cause errors!

> Run the code block below to demonstrate the error that arises when operations on vectors of lengths that are not factors of one another is attempted


```r
i <- c(1, 1, 1)
length(w)
length(i)
i + w
```

When the vectors are of the same length, element-wise operations are **performed between pairs with the same position in the respective objects**. 

> 1. Define a vector in the code block below called `w2` that has **the same length as `w`** and consists only of the numeric value `1` repeated.

> 2. Then add `w` and `w2` together.


```r
## 1. Create a new vector with c()
w2 <- c(1,1,1,1)
## 1. Create a new vector with c()


## 2. Add the w and w2 vectors together  
w + w2
```

```
## [1] 2 3 4 5
```

```r
## 2. Add the w and w2 vectors together
```

# Character vectors

We can also produce vectors of **characters**.

> Run the code block below to define a vector of characters:


```r
some_letters <- c("a", "b", "c", "d")
```

With this last variable, we had to use double quotes, `""`, to specify that we want to create a character vector. Otherwise it thinks we are looking for variables to combine called a, b, c, and d.

> What happens when you run the code block below? Why?


```r
some_letters <- c(a,b,c,d)
```

Note that such vectors are of the type **character**.

> Run the code block below to display the **class** of the object `some_letters`:


```r
class(some_letters)
```

```
## [1] "character"
```

While it is technically possible to create a vector that mixes numeric and character elements, we typically don't work with these, **because R performs different operations on different object types**. If in the data sheet for an experiment we observe mixed types, it is typically either a typo, a non-data entry, or some custom notation for missing data, e.g. `?` or `NA` (we will discuss the handling of missing values in a little bit)

# Other helpful vector functions

> 1. In the code block below, create a new vector, called `nums` that contains any 5 numbers you like.

There are a number of functions that operate on vectors, including `length()`, `max()`, `min()`, and `mean()`, all of which do exactly what they sound like they do. So for example `length(nums)` should return 5, because `nums` is a 5-element vector. 

> 2. In the code block below, use these functions to get the minimum, maximum, and mean value for the `nums` vector you created.


```r
## 1. create a new vector, called `nums` that contains any 5 numbers you like
nums <- c(33, 22, 41, 54, 91)
## 1. create a new vector, called `nums` that contains any 5 numbers you like


## 2. Pass the nums object to the length, min, max, and mean functions
length(nums)
```

```
## [1] 5
```

```r
min(nums)
```

```
## [1] 22
```

```r
max(nums)
```

```
## [1] 91
```

```r
mean(nums)
```

```
## [1] 48.2
```

```r
## 2. Pass the nums object to the length, min, max, and mean functions
```

# The logical (TRUE/FALSE) data type

**Numeric** and **character** data types are two of the most common we'll encounter, and are just what they sound like. Another useful type is **logical** data, as in *TRUE* or *FALSE*. We can create a logical vector directly like so. The words `TRUE` and `FALSE` (typed in all capital letters) are understood by R to be their own **values** of this data type. Note that you can still have strings of these words, as long as you use quotes around them, e.g. `"TRUE"` and `"FALSE"`. With quotes, R treats these as character strings for those words rather than the logical values.

Like **numeric** or **character** data, we can create objects of type **logical**.

> Run the code block below to create a logical vector:


```r
logic1 <- c(TRUE, TRUE, FALSE, FALSE)
logic1
```

```
## [1]  TRUE  TRUE FALSE FALSE
```

```r
class(logic1)
```

```
## [1] "logical"
```

As we did above with **numeric vectors** when we performed mathematical operations on them, we can use special **comparison operators** to perform operations and return **logical vectors**:

> Run the code block below to **test a condition** of a vector we previously defined:


```r
v1
```

```
## [1] 1 2 3 4 5
```

```r
logic2 <- v1 > 2
logic2
```

```
## [1] FALSE FALSE  TRUE  TRUE  TRUE
```

Note that the logical test here (whether an element in the vector is > 2) is applied independently to each element in the vector. 

Another important feature of logical data is that the numeric values of `1` and `0` correspond and act as `TRUE` and `FALSE` logical values, respectively. This can be helpful if we want to figure out how many values meet a logical statement criterion.

> Run the code block below to count how many elements in vector V1 meet the condition we tested for above:


```r
v1
```

```
## [1] 1 2 3 4 5
```

```r
sum(logic2)
```

```
## [1] 3
```

The `sum()` function simply sums the elements of a vector. In this case, 3 elements of v1 are > 2 and the sum function interprets logic2 as `c(0,0,1,1,1)`.

Here is a brief summary of the logical operators in R:

**Operator** | **Interpretation**   |
-------------|----------------------|
==           |equal to              |
>            |greater than          |
<            |less than             |
>=           |greater or equal to   |
<=           |less than or equal to |
!=           |not equal to          |

> 1. In the code block below, construct a logical vector with the same number of elements as the vector nums `nums <- c(33, 22, 41, 54, 91)` that is TRUE if the corresponding element in the nums vector is GREATER THAN the mean of the nums vector, and FALSE otherwise. Call this vector big_nums


```r
## 1. Create logical vector
big_nums <- nums > mean(nums)
## 1. Create logical vector
```


# Subsetting and Logical Vectors

Recall that vectors are a gathering of multiple different individual pieces of information. We learned that the vector itself has a **length** attribute that can be found with the `length()` function. Well the  pieces of information within the vector can also be accessed individually.

We can extract portions of vectors that we've created using the square brackets, `[]`, following the vector, with the positions in the vector (or the **index**) we wish to extract. For example, we can extract portions of the `nums` vector.

> Run the following code block to see different ways to extract elements by **index**:


```r
nums[1]
```

```
## [1] 33
```

```r
nums[1:5]
```

```
## [1] 33 22 41 54 91
```

```r
nums[c(1,4,5)]
```

```
## [1] 33 54 91
```

> 2. In the code block below, subtract 10 from each element of the `nums` vector and then display only the last element of the vector.


```r
## 2. Subtract 10 from nums and print the last element of a vector
new_nums = nums - 10
new_nums[length(new_nums)]
```

```
## [1] 81
```

```r
## 2. Subtract 10 from nums and print the last element of a vector
```

Now it can be useful to specify which positions you would like to include, but often it is more useful to create new objects based on some sort of rule. That is where logical vectors come in, and really how you will mostly be using logical vectors going forward.

For example, in the last exercise, we constructed a logical vector that was the same length as our nums vector that was `TRUE` with if the corresponding element in the nums vector is less than the mean of the nums vector, and `FALSE` otherwise.

Let's take a look at both of these vectors again.

> Run the following code block to view the previously created vectors, `nums` and `big_nums`:


```r
nums
```

```
## [1] 33 22 41 54 91
```

```r
big_nums
```

```
## [1] FALSE FALSE FALSE  TRUE  TRUE
```

Let's say we actually want to extract all of the numbers that are bigger than the mean (so all of the `TRUE`) values. All we have to do is put the logical vector in brackets.

> Run the following code block to extract values from a vector based on a logical vector of the same length:


```r
nums[big_nums]
```

```
## [1] 54 91
```

We don't necessarily have to define this vector ahead of time, but can put the rule in the brackets as well.

> Run the following code block to extract values from a vector based on a logical test statement:


```r
nums[nums > mean(nums)]
```

```
## [1] 54 91
```

# Data Frames

So far we've been talking about atomic **vectors**, which only contain a single data type (every element is **logical**, or **character**, or **numeric**). However, data sets will usually have multiple different data types: numeric for continuous data, character for categorical data and sample labels. Depending on how underlying types are combined, we can have four different "higher-level" data structures in R:

**Dimensions** | **Homogeneous** | **Heterogeneous**
---------------|-----------------|-------------------
1-D            | atomic vector   | list
2-D            | matrix          | data frame / tibble

We'll focus on data frames for today, but lists and matrices can also be very powerful. 

A **data frame** is a collection of vectors, which can be (but don't have to be) different types, but all have to have the same length. Later on we will introduce *tidyverse*, an R module the goal of which is to make data "tidy", i.e. clean and easy to use. The tidyverse version of a data frame is a *tibble*, which we will introduce tomorrow. For now, let's make a couple of toy data frames.

One way to do this is to manually initialize and object with the `data.frame()` function.

> Run the code block below to create a data frame from scratch with the `data.frame()` function:


```r
df1 <- data.frame(label=c("rep1", "rep2", "rep3", "rep4"), data=c(23, 34, 15, 19))
df1
```

```
##   label data
## 1  rep1   23
## 2  rep2   34
## 3  rep3   15
## 4  rep4   19
```

```r
class(df1)
```

```
## [1] "data.frame"
```

In some sense, its best to think of a data frame as a table (or a spreadsheet). It consists of rows and columns. Rows contain data for one observation in the dataset and columns contain different features or variables being observed.

In the code block above, we've created a data frame with *4 rows* and *2 columns*. The *column headers* or **names** are `label` and `data`. The first *row* of data has the label "rep1" and the data "23". As you can see, we've simply defined each *column* as a separate **vector**, but as a **data frame** we ensure that the vectors are associated with each other.

The `str()` gives lots of information about the data type of the constituent parts of a data frame.

> Run the code block below to print information about the object types in the data frame:


```r
str(df1)
```

```
## 'data.frame':	4 obs. of  2 variables:
##  $ label: chr  "rep1" "rep2" "rep3" "rep4"
##  $ data : num  23 34 15 19
```

A related function, to see the actual dimensions of your data frame (the number of rows and columns) is the `dim` function.

> Run the code block below to view the dimensions of the data fram with `dim()`:


```r
dim(df1)
```

```
## [1] 4 2
```

We can use the function `head()` to look at part of a data frame (or any R object). This can be very useful if you have a very large or long dataframe. You also can control how many lines of the dataframe you view with ```n=#```, although the default is 6.

> Run the code block below to view the top of the data frame with `head()`:


```r
head(df1)
```

```
##   label data
## 1  rep1   23
## 2  rep2   34
## 3  rep3   15
## 4  rep4   19
```

```r
head(df1, n=2)
```

```
##   label data
## 1  rep1   23
## 2  rep2   34
```

The `summary()` function can also be very useful to get a snapshot of the data in your dataframe.

> Run the code block below to see the `summary()` of the data frame:


```r
summary(df1)
```

```
##     label                data      
##  Length:4           Min.   :15.00  
##  Class :character   1st Qu.:18.00  
##  Mode  :character   Median :21.00  
##                     Mean   :22.75  
##                     3rd Qu.:25.75  
##                     Max.   :34.00
```

## Accessing elements of a data frame

Much like elements in a vector can be accessed using square brackets `[]` and indices, we can also access elements of a **data frame** with `[]`, but this time the indices are two dimensional, with one coordinate for the row and one for the column position, e.g. `[1,2]`.

> Run the code block below to display different elements of the data frame by index:


```r
df1[1,2]
```

```
## [1] 23
```

This displays the element in the first row and second column of the data frame, which is 23.

> Run the code block below to display different elements of the data frame by index:


```r
df1[2,1]
```

```
## [1] "rep2"
```

This displays the element in the second row and first column of the data frame, which is "rep1".

By leaving one index off, we can retrieve entire rows or columns from the data frame.

> Run the code block below to display the whole first row of the data frame and the whole second column of the data frame:


```r
df1[1,]
```

```
##   label data
## 1  rep1   23
```

```r
df1[,2]
```

```
## [1] 23 34 15 19
```

**Columns** can also be accessed by their *name* and the dollar sign operator, `$`.

> Run the code block below to display the whole second column of the data frame with the `$` operatoe:


```r
df1$data
```

```
## [1] 23 34 15 19
```

>1. Create a new vector, (called `my_product`), that consists of the `data` column of `df1` multiplied by `10`.


```r
## 1. Create new vector based on column in a data frame
my_product <-df1$data*10
## 1. Create new vector based on column in a data frame
```

# Reading files into R

So far we have been working with small objects we created by hand. A more common way to create **data frames** is by **reading tables from a file**. There are a few functions to do this in R. The old school way of doing this it by using the `read.table()` and `read.csv()` functions, with the latter being a generic file loader for which you can specify what delimits the columns: comma, space, tab, or some other character.

For this workshop, we are going to read the [and_vertebrates](https://lter.github.io/lterdatasampler/reference/and_vertebrates.html) data set from LTER, which stands for Long Term Ecological Research network. This data set is comprised of sampling data for cutthroat trout and two salamander species in different habitats, for different years, with weight and body size measurements, as well as unique individual identifiers. It is a rather large data set, consisting of over 32,209 rows and 16 columns.

Today, we will load files into **data frames** in the standard, older way. In tomorrow's workshop, we will introduce you to *tidyverse* and teach you how loading files as **tibbles** can offer a number of advantages. For now, let's try the standard way:

> Run the following code block to read data from a file into an object in R (in this case, as a **data frame**) with the `read.csv()` function:


```r
vertebrates <- read.csv(file="https://harvardinformatics.github.io/workshops/2023-fall/r/data/LTER_andvertebrates.csv", sep=",", header=TRUE)
```

As with manually constructed data frames, we can access *rows* and *columns* within it. 

Let's see how many unique sampling dates there are, regardless of species. The `sampledate` column is the date variable. We can use the `length()` and `unique()` function, where the latter returns unique values as a vector, and the former returns the length of that vector.

> Run the code block below to count the sampling dates in the data set:


```r
length(unique(vertebrates$sampledate))
```

```
## [1] 99
```

Loaded in this manner, if you type `vertebrates` in the R console, it will return a large number of columns before print a "reached max" statement and telling you how many columns it didn't print. But for a quick view, analogous to unix, you can use the head function, as above.

> Run the code block below to view the first 10 lines of the data set:


```r
head(vertebrates,10)
```

```
##    year sitecode section reach pass unitnum unittype vert_index pitnumber
## 1  1987 MACKCC-L      CC     L    1       1        R          1        NA
## 2  1987 MACKCC-L      CC     L    1       1        R          2        NA
## 3  1987 MACKCC-L      CC     L    1       1        R          3        NA
## 4  1987 MACKCC-L      CC     L    1       1        R          4        NA
## 5  1987 MACKCC-L      CC     L    1       1        R          5        NA
## 6  1987 MACKCC-L      CC     L    1       1        R          6        NA
## 7  1987 MACKCC-L      CC     L    1       1        R          7        NA
## 8  1987 MACKCC-L      CC     L    1       1        R          8        NA
## 9  1987 MACKCC-L      CC     L    1       1        R          9        NA
## 10 1987 MACKCC-L      CC     L    1       1        R         10        NA
##            species length_1_mm length_2_mm weight_g clip sampledate notes
## 1  Cutthroat trout          58          NA     1.75 NONE 1987-10-07  <NA>
## 2  Cutthroat trout          61          NA     1.95 NONE 1987-10-07  <NA>
## 3  Cutthroat trout          89          NA     5.60 NONE 1987-10-07  <NA>
## 4  Cutthroat trout          58          NA     2.15 NONE 1987-10-07  <NA>
## 5  Cutthroat trout          93          NA     6.90 NONE 1987-10-07  <NA>
## 6  Cutthroat trout          86          NA     5.90 NONE 1987-10-07  <NA>
## 7  Cutthroat trout         107          NA    10.50 NONE 1987-10-07  <NA>
## 8  Cutthroat trout         131          NA    20.60 NONE 1987-10-07  <NA>
## 9  Cutthroat trout         103          NA     9.55 NONE 1987-10-07  <NA>
## 10 Cutthroat trout         117          NA    13.00 NONE 1987-10-07  <NA>
```

In Rstudio, we can also use the `View()` (notice the capital "V") function to open the whole dataset in another tab of the *text editor*. RStudio nicely formats **data frames** as human-readable tables.

> Run the following command in the R **Console** below to open the data set in a new tab in the text editor:

```
View(vertebrates)
```

A word of caution with `View()`: be careful `View`ing large datasets, since they can be difficult for RStudio to display and may slow down the program.

> 1. Can you guess what the R function is to see the last n columns? Try `tail()` to get the last 10 columns of the *vertebrates* data frame:


```r
## 1. View last 10 lines of the data frame with tail()
tail(vertebrates, n=10)
```

```
##       year sitecode section reach pass unitnum unittype vert_index pitnumber
## 32200 2019 MACKOG-U      OG     U    2      16        C         17        NA
## 32201 2019 MACKOG-U      OG     U    2      16        C         18        NA
## 32202 2019 MACKOG-U      OG     U    2      16        C         19        NA
## 32203 2019 MACKOG-U      OG     U    2      16        C         20        NA
## 32204 2019 MACKOG-U      OG     U    2      16        C         21        NA
## 32205 2019 MACKOG-U      OG     U    2      16        C         22        NA
## 32206 2019 MACKOG-U      OG     U    2      16        C         23   1043503
## 32207 2019 MACKOG-U      OG     U    2      16        C         24   1043547
## 32208 2019 MACKOG-U      OG     U    2      16        C         25   1043583
## 32209 2019 MACKOG-U      OG     U    2      16        C         26   1043500
##                        species length_1_mm length_2_mm weight_g clip sampledate
## 32200 Coastal giant salamander          33          63      1.6 NONE 2019-09-05
## 32201 Coastal giant salamander          38          68      1.6 NONE 2019-09-05
## 32202 Coastal giant salamander          51          98      5.0 NONE 2019-09-05
## 32203 Coastal giant salamander          50          93      5.3 NONE 2019-09-05
## 32204 Coastal giant salamander          58         101      6.4 NONE 2019-09-05
## 32205 Coastal giant salamander          58         108      7.9 NONE 2019-09-05
## 32206 Coastal giant salamander          65         115      8.7 NONE 2019-09-05
## 32207 Coastal giant salamander          67         120      9.6 NONE 2019-09-05
## 32208 Coastal giant salamander          74         131     14.3 NONE 2019-09-05
## 32209 Coastal giant salamander          73         128     11.6 NONE 2019-09-05
##             notes
## 32200        <NA>
## 32201        <NA>
## 32202        <NA>
## 32203        <NA>
## 32204        <NA>
## 32205        <NA>
## 32206        <NA>
## 32207        <NA>
## 32208        <NA>
## 32209 Terrestrial
```

```r
## 1. View last 10 lines of the data frame with tail()
```

Another useful function is `summary()` which provides basic summary statistics on the values of each column.

> 2. What is the average weight in grams of the observed animals?


```r
## 2. Use any method to get the average weight of the animals
summary(vertebrates$weight_g)
```

```
##    Min. 1st Qu.  Median    Mean 3rd Qu.    Max.    NA's 
##   0.090   1.510   6.050   8.903  11.660 134.590   13268
```

```r
mean(vertebrates$weight_g, na.rm=T)
```

```
## [1] 8.902859
```

```r
## 2. Use any method to get the average weight of the animals
```

# End of Part 1

In tomorrow's workshop, we will teach you how to load data in the [tidyverse](https://www.tidyverse.org/) way, how to select and filter a data set using certain criteria, how to construct new variables, and how to write the resulting outputs to new files.
