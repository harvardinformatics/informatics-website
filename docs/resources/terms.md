---
title: Terminology
hide:
    - navigation
---

<style>
    .md-sidebar--secondary {
        order: 0;
    }
</style>

# Helpful terminology

Here's some helpful terminology that we use throughout our trainings. Let us know if there is something we should add!

## Definitions of general data science terms

| Term | Definition |
| --- | --- |
| Command | An instruction given to the computer to perform an operation (such as opening a file, adding a row to a data table, etc.). The way a command is given to the computer is often dictated by the programming language in which it is to be interpreted (known as that language's syntax). |
| Script | A set of commands written in a particular programming language's syntax that are stored as plain text in a file. When interpreted by that programming language, the commands will be executed in order. |
| Text editor | A graphical program on a computer that displays plain text files on the screen and allows them to be edited. |
| Integrated Development Environment (IDE) | A graphical program on a computer that contains tools to aid development in a specific programming language (e.g. RStudio for R). |

## Definitions of general programming terms

| Term | Definition |
| --- | --- |
| Syntax | The way a particular programming language expects its code to be written. |
| Variable | The name of a piece of information stored into memory in a computer program. This name can be referred to later in the program and used to manipulate the information. |
| Data type | The way data is encoded on the computer. Different operations can be performed on different data types. |
| Data structure | The way data is organized within a programming language. Different operations can be performed on different data structures. |
| Function | A generalized chunk of code that can be easily inserted into new code. In R, functions can also be run as commands, and are passed arguments (data or variables) within parentheses (e.g. my_function(parameter=2) will execute the code in my_function with the parameter variable set to 2). |
| Operator | In programming, operators are special functions that are denoted by specific symbols and can be used to manipulate and compare information in the program. Sometimes the way an operator works depends on the data type being used with it. |
| Assignment operator | In many programming languages, a variable can be ASSIGNED a value with the equals sign (=); e.g. var_name = 1. Note that in R, <- is also an assignment operator. |
| Algebraic operators | Many programming languages have basic algebraic operators to manipulate numeric data types, like + for ADDITION, - for SUBTRACTION, * for MULTIPLICATION, and / for DIVISION. Note that in some programming languages, these symbols can be used as operators for other data types with different outcomes, for example in Python, the + operator can also concatenate two strings together. |
| Logical operators | Logical operators allow comparisons of CONDITIONS. Common logical operators are AND (represented as && or &) and OR (represented as || or |). |
| Comparative operators | Logical comparisons of numbers include EQUALITY (==), GREATER THAN (>), GREATER THAN OR EQUAL TO (>=), LESS THAN (<), LESS THAN OR EQUAL TO (<=). |
| Inclusion operators | Some languages use another operator to check whether a certain value is INCLUDED within a larger data structure, sometimes denoted as in or %in%. |
| Negation operator | For any comparison or logical operation, a NEGATION can be made, represented in many programming languages as ! or not, e.g. !TRUE is equivalent to FALSE. |

## Definitions of terms related to R and RStudio

| Term | Definition |
| --- | --- |
| R | A functional programming language with an emphasis on statistical analysis and data visualization. |
| RStudio | An IDE for R. |
| Environment | The set of scripts, packages, and data currently loaded into memory in RStudio. |
| Console | An interactive command line in RStudio that accepts one R command at a time to be executed when the ENTER key is pressed. |
| Package | A set of code available to be installed to perform specific tasks. |
| Markdown | A syntax for formatting plain text and interleaving code blocks that can be run when the document is generated. |
| Code block | In a markdown document, separate blocks of text that are interpreted as code when the document is generated. |
| <- | An assignment operator in R that can be used to assign values to operators, e.g. x <- 10 assigns the variable x the value of 10. |
| Object | Data of any type that has been stored as a variable in the current environment. |
| Character | A data type of one or more alpha-numeric characters. |
| Numeric | A data type of numbers. |
| Logical | A data type with two possible values, either TRUE or FALSE. |
| Vector | A data structure that contains multiple objects stored as a collection. |
| Data frame | A data structure that is a collection of vectors stored as a table with rows and columns, with the columns being the vector names. |
| Tibble | A data structure that is the tidyverse implementation of a data frame. |
| List | A data structure made up of a collection of any type of objects. |