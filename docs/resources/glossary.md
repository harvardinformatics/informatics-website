---
title: Glossary
---

<style>
    .md-sidebar--secondary {
        order: 0;
    }
	.md-main {
		width: 100% !important;
	}
	.md-main__inner {
		width: 66% !important;
		max-width: 66% !important;
	}
    .md-sidebar--primary {
        display: none;
    }
    code {
        color:#000099 !important;
        /* font-weight:bold; */
    }
</style>

Like any specific domain, the way we talk about computing and programming is almost its own language. Words in this context may have different meaning than in other contexts. 
As programmers ourselves, we are so used to using words in the context of programming that we sometimes forget others aren't used to it. This is one of the biggest roadblocks
to teaching and learning.

Here we have compiled a long list of computer and programming related terms in (hopefully) plain language as a resource for anyone learning about programming to look up if they
don't understand a term that they heard or read.

Please feel free to suggest additions or edits.

## General computing terms

\* These terms are used somewhat interchangeably colloquially

{{ read_csv('data/tables/general.csv') }}

## General programming terms

{{ read_csv('data/tables/programming-general.csv') }} 

### Programming constructs

{{ read_csv('data/tables/programming-constructs.csv') }} 

### Data representation

{{ read_csv('data/tables/programming-data.csv') }} 

### Functions

{{ read_csv('data/tables/programming-functions.csv') }} 

### Operators

{{ read_csv('data/tables/programming-operators.csv') }} 

### Errors

{{ read_csv('data/tables/programming-errors.csv') }} 

### Programming tools

{{ read_csv('data/tables/programming-tools.csv') }} 

## Python terms

*Note that while we give some examples of syntax, the format of these tables does not lend itself to exact typing, so please read further documentation if needed and for more information on Python's syntax.* 

{{ read_csv('data/tables/python.csv') }}

\* Note: While R is primarily a functional programming language and not inherently object-oriented, the subsequent tables use OOP terms and provide R examples because R can emulate OOP behavior.

### Python data types

{{ read_csv('data/tables/python-data-types.csv') }}

### Python data structures

{{ read_csv('data/tables/python-data-structures.csv') }}

### Python operators

\* See below the table for examples of update operator usage in Python. 

{{ read_csv('data/tables/python-operators.csv') }}

\* Update operators are shortcuts to re-assign a variable to a new value based on the old one. For example, in Python one could add 3 to a number stored in a variable as follows:

```python
my_variable = 5
my_variable = my_variable + 3
print(my_variable)
```

At which point the current value of `my_variable` would print to the screen: `8`

Or, as a shortcut, one could type:

```python
my_variable = 5
my_variable += 3
print(my_variable)
```

And `my_variable` would have the same value as above: `8`

This works for the other arithmetic operators as well. See the table for all arithmetic and update operators.

## R terms

*Note that while we give some examples of syntax, the format of these tables does not lend itself to exact typing, so please read further documentation if needed and for more information on R's syntax.*

{{ read_csv('data/tables/r.csv') }}

### R data types

*Note: While these individual data types are not **iterable** in R, vectors made up of any data type inherit that type (*i.e.* a vector of numerics is itself numeric in type) and are iterable (see below)*

{{ read_csv('data/tables/r-data-types.csv') }}

### R data structures

{{ read_csv('data/tables/r-data-structures.csv') }}

### R operators  

*Note that R does not have **update operators** like Python does (see above).*

{{ read_csv('data/tables/r-operators.csv') }}

## High performance computing (HPC) terms

For more information related to Harvard's cluster, see <a href="https://docs.rc.fas.harvard.edu/" target="_blank">FASRC's documentation</a>, 
particularly their page on <a href="https://docs.rc.fas.harvard.edu/kb/running-jobs/" target="_blank">running jobs</a>.

They also provide a <a href="https://docs.rc.fas.harvard.edu/kb/glossary/" target="_blank">more extensive glossary</a> for more term definitions.

{{ read_csv('data/tables/hpc.csv') }}   

## Installing software

Installing software is a notoriously troublesome task, especially for beginners and when working on a server on which you don't have accsess to the **root** of the file system.

A couple of strategies have evolved to make this easier:

    1. Environments: Portions of the *user's file system* that are adjusted so they can install and run software, giving the user full control.
    2. Containers: Executable files that internally emulate the file system of the developer's computer, allowing the software in the container to be run without being explicitly installed on the user's computer.

There are several ways to create environments and containers which are covered below. Additionally, different environment management systems may work with different package repositories and managers, so we go over some of those as well.

{{ read_csv('data/tables/installing-software.csv') }}  

## Git terms  

<a href="https://git-scm.com/" target="_blank">Git</a> is a program that stores the history of files in any directory that has been initialized as a git repository. Used in conjunction with web-based platforms this makes for a powerful collaboration tool.
However, there are many terms associated with Git that may be confusing. In essence, many of these terms are simply other words for "a copy" or "copying" a directory, however with slight distinctions.
This table tries to define these terms clearly.

{{ read_csv('data/tables/git.csv') }}