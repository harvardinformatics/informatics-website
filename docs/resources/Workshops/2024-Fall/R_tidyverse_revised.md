---
title: "Harvard Informatics R Tidyverse Workshop"
date: "Fall, 2024"
author: "Lei Ma, Adam Freedman, Gregg Thomas"
output: 
  html_document:
    keep_md: true
---
<style>
    .md-sidebar--secondary { order: 0; }
    .md-sidebar--primary { display: none; }
    /* This hides the Navigation sidebar and moves the TOC sidebar to the left in HTML renders */
</style>

## R, RStudio, and R Markdown

Hello everyone. Let's get oriented to how today's tidyverse workshop is going to run. I will be sharing my screen in RStudio as I demonstrate the package tidyverse and various concepts. You all should also open up your RStudio and download and open this document, which you can find on our website (TBD Short link to download) and follow along. There will be exercises during the workshop to practice! 

For those who are not familiar with this file format, this is an RMarkdown file, which is a mixture of formatted text and **code blocks**. Code is written and executed in these code blocks, which are delineated by the backtick character (\`). Each code block can have a language specified (in our case we will exclusively use `r`) as well as options specific to that block. Here is an example of an R code block in this R Markdown file:


``` r
getwd()
```

``` r
print("hello world")
```

We will have exercises that are demarcated with a ">" symbol, like the one coming up!

> In the code block above, find the green triangle in the upper right hand corner and click it.

What happened? The output appeared right below the code block!

We can also use keyboard shortcuts to run code

> Run the code block above by placing your cursor in the code block and typing the *ctrl+shift+enter* (windows) or *cmd+shift+enter* (mac) key combination.

Using *ctrl+enter*/*cmd+enter* we can run only the line that the cursor is on.

## Tidy data

> Tabular data is tidy if each value is placed in its own “cell”, each variable in its own column, and each observation in its own row.
>
> -   Hadley Wickham (R for Data Science 2nd Edition)

In general tidy data is the format that is most conducive to data analysis and visualization. To that end, the "Tidyverse" is actually a collection of packages that share a similar design philosophy around how data and visualization is represented and interacted with in R. Let's load some data sets that are already tidy and see what kinds of transformations we can do using the tidyverse library.

### Downloading and loading tidyverse package

If you haven't already, you will need to install and load the tidyverse package. Once you load it, you will see all the libraries that are included. 


``` r
if(!require(tidyverse)){install.packages("tidyverse", quiet=TRUE)}
library(tidyverse)
```

### The tibble data structure

Today we will be working with the data structure known as tibble. A tibble is a data structure that is suitable for storing heterogenous data, that is, data that is a mix of numerical and categorical. Tibbles are 2D and you can think of them as similar to a spreadsheet in Excel. Below is a table comparing some different data structures in R and the types of data you can store in it. While we focus on tibbles, the functions we'll be using today can be used in any of the data structures that are listed alongside tibbles (e.g. data.frame, data.table).

| **Dimensions** | **Homogeneous** | **Heterogeneous**                |
|----------------|-----------------|----------------------------------|
| 1-D            | atomic vector   | list                             |
| 2-D            | matrix          | data.frame / tibble / data.table |
| n-D            | array           | ---                              |

Here is an example of a tibble:


``` r
mpg
```

```
## # A tibble: 234 × 11
##    manufacturer model      displ  year   cyl trans drv     cty   hwy fl    class
##    <chr>        <chr>      <dbl> <int> <int> <chr> <chr> <int> <int> <chr> <chr>
##  1 audi         a4           1.8  1999     4 auto… f        18    29 p     comp…
##  2 audi         a4           1.8  1999     4 manu… f        21    29 p     comp…
##  3 audi         a4           2    2008     4 manu… f        20    31 p     comp…
##  4 audi         a4           2    2008     4 auto… f        21    30 p     comp…
##  5 audi         a4           2.8  1999     6 auto… f        16    26 p     comp…
##  6 audi         a4           2.8  1999     6 manu… f        18    26 p     comp…
##  7 audi         a4           3.1  2008     6 auto… f        18    27 p     comp…
##  8 audi         a4 quattro   1.8  1999     4 manu… 4        18    26 p     comp…
##  9 audi         a4 quattro   1.8  1999     4 auto… 4        16    25 p     comp…
## 10 audi         a4 quattro   2    2008     4 manu… 4        20    28 p     comp…
## # ℹ 224 more rows
```

This tibble of different car specifications has 11 columns and each column holds either numerical or categorical data. The columns all have names, but the rows do not. You can access a column by using the `$` operator, like so:


``` r
mpg$manufacturer
```

```
##   [1] "audi"       "audi"       "audi"       "audi"       "audi"      
##   [6] "audi"       "audi"       "audi"       "audi"       "audi"      
##  [11] "audi"       "audi"       "audi"       "audi"       "audi"      
##  [16] "audi"       "audi"       "audi"       "chevrolet"  "chevrolet" 
##  [21] "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet" 
##  [26] "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet" 
##  [31] "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet"  "chevrolet" 
##  [36] "chevrolet"  "chevrolet"  "dodge"      "dodge"      "dodge"     
##  [41] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [46] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [51] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [56] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [61] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [66] "dodge"      "dodge"      "dodge"      "dodge"      "dodge"     
##  [71] "dodge"      "dodge"      "dodge"      "dodge"      "ford"      
##  [76] "ford"       "ford"       "ford"       "ford"       "ford"      
##  [81] "ford"       "ford"       "ford"       "ford"       "ford"      
##  [86] "ford"       "ford"       "ford"       "ford"       "ford"      
##  [91] "ford"       "ford"       "ford"       "ford"       "ford"      
##  [96] "ford"       "ford"       "ford"       "ford"       "honda"     
## [101] "honda"      "honda"      "honda"      "honda"      "honda"     
## [106] "honda"      "honda"      "honda"      "hyundai"    "hyundai"   
## [111] "hyundai"    "hyundai"    "hyundai"    "hyundai"    "hyundai"   
## [116] "hyundai"    "hyundai"    "hyundai"    "hyundai"    "hyundai"   
## [121] "hyundai"    "hyundai"    "jeep"       "jeep"       "jeep"      
## [126] "jeep"       "jeep"       "jeep"       "jeep"       "jeep"      
## [131] "land rover" "land rover" "land rover" "land rover" "lincoln"   
## [136] "lincoln"    "lincoln"    "mercury"    "mercury"    "mercury"   
## [141] "mercury"    "nissan"     "nissan"     "nissan"     "nissan"    
## [146] "nissan"     "nissan"     "nissan"     "nissan"     "nissan"    
## [151] "nissan"     "nissan"     "nissan"     "nissan"     "pontiac"   
## [156] "pontiac"    "pontiac"    "pontiac"    "pontiac"    "subaru"    
## [161] "subaru"     "subaru"     "subaru"     "subaru"     "subaru"    
## [166] "subaru"     "subaru"     "subaru"     "subaru"     "subaru"    
## [171] "subaru"     "subaru"     "subaru"     "toyota"     "toyota"    
## [176] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [181] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [186] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [191] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [196] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [201] "toyota"     "toyota"     "toyota"     "toyota"     "toyota"    
## [206] "toyota"     "toyota"     "volkswagen" "volkswagen" "volkswagen"
## [211] "volkswagen" "volkswagen" "volkswagen" "volkswagen" "volkswagen"
## [216] "volkswagen" "volkswagen" "volkswagen" "volkswagen" "volkswagen"
## [221] "volkswagen" "volkswagen" "volkswagen" "volkswagen" "volkswagen"
## [226] "volkswagen" "volkswagen" "volkswagen" "volkswagen" "volkswagen"
## [231] "volkswagen" "volkswagen" "volkswagen" "volkswagen"
```

You can index a tibble by row and column using square brackets, like so:


``` r
# mpg[ROW, COLUMN]
# Get the first row and first two columns
# : is used to create a range of values
mpg[1, 1:2]
```

```
## # A tibble: 1 × 2
##   manufacturer model
##   <chr>        <chr>
## 1 audi         a4
```


``` r
# mpg[ROW, COLUMNS]
# Use the c() function to create a vector of column names
mpg[1:10, c("manufacturer", "model", "year")]
```

```
## # A tibble: 10 × 3
##    manufacturer model       year
##    <chr>        <chr>      <int>
##  1 audi         a4          1999
##  2 audi         a4          1999
##  3 audi         a4          2008
##  4 audi         a4          2008
##  5 audi         a4          1999
##  6 audi         a4          1999
##  7 audi         a4          2008
##  8 audi         a4 quattro  1999
##  9 audi         a4 quattro  1999
## 10 audi         a4 quattro  2008
```

### Tidyverse syntax/conventions

If you have used R previously, you may be familiar with the typical way to call functions in R. For example, to call the `mean()` function, you would write `mean(x)`. This is a completely fine way of calling functions in tidyverse as well, but there is a new way to pass arguments to functions that helps with readability. This concept is called "piping" and is done using the `%>%` operator. When you "pipe" an object to a function `object %>% function()`, the object is passed as the first argument to the function. Because tidyverse functions are designed to do things with data objects, the first argument is typically the data you are working with. Additionally, because many of these functions **return** a data object, you can chain functions together to create a pipeline of operations. This makes the code more readable and easier to understand.

Below is the historical "base R" way of calling functions in R:


``` r
# filter some dataset
mpg_audi <- filter(mpg, manufacturer == "audi")
# count number of rows
nrow(mpg_audi)
```

```
## [1] 18
```

If we use pipes ` %>% `, we can rewrite the code in one line and avoid saving extra variables:


``` r
mpg %>% 
  filter(manufacturer == "audi") %>% 
  nrow()
```

```
## [1] 18
```

We will be using the pipe operator throughout the workshop to make our code more readable and concise.

### What makes data tidy?

Our definition of a tidy dataset is one in which all data is in a 2D table with rows representing observations and columns representing variables.

Here is an example of tidy data:


``` r
mpg
```

```
## # A tibble: 234 × 11
##    manufacturer model      displ  year   cyl trans drv     cty   hwy fl    class
##    <chr>        <chr>      <dbl> <int> <int> <chr> <chr> <int> <int> <chr> <chr>
##  1 audi         a4           1.8  1999     4 auto… f        18    29 p     comp…
##  2 audi         a4           1.8  1999     4 manu… f        21    29 p     comp…
##  3 audi         a4           2    2008     4 manu… f        20    31 p     comp…
##  4 audi         a4           2    2008     4 auto… f        21    30 p     comp…
##  5 audi         a4           2.8  1999     6 auto… f        16    26 p     comp…
##  6 audi         a4           2.8  1999     6 manu… f        18    26 p     comp…
##  7 audi         a4           3.1  2008     6 auto… f        18    27 p     comp…
##  8 audi         a4 quattro   1.8  1999     4 manu… 4        18    26 p     comp…
##  9 audi         a4 quattro   1.8  1999     4 auto… 4        16    25 p     comp…
## 10 audi         a4 quattro   2    2008     4 manu… 4        20    28 p     comp…
## # ℹ 224 more rows
```

In the dataset mpg, each row is a different model of car, and the columns are different variables that describe each car. By having data in this format, we can easily answer questions such as "What is the number of different car classes that each manufacturer creates?". Run the code below for a demonstration of the readability of tidy data analysis. (Don't worry about the actual functions for now, we'll cover them later)


``` r
mpg %>% 
  group_by(manufacturer) %>% 
  summarize(n_distinct(class))
```

```
## # A tibble: 15 × 2
##    manufacturer `n_distinct(class)`
##    <chr>                      <int>
##  1 audi                           2
##  2 chevrolet                      3
##  3 dodge                          3
##  4 ford                           3
##  5 honda                          1
##  6 hyundai                        2
##  7 jeep                           1
##  8 land rover                     1
##  9 lincoln                        1
## 10 mercury                        1
## 11 nissan                         3
## 12 pontiac                        1
## 13 subaru                         3
## 14 toyota                         4
## 15 volkswagen                     3
```

Here is an example of data that is not tidy:


``` r
billboard
```

```
## # A tibble: 317 × 79
##    artist     track date.entered   wk1   wk2   wk3   wk4   wk5   wk6   wk7   wk8
##    <chr>      <chr> <date>       <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
##  1 2 Pac      Baby… 2000-02-26      87    82    72    77    87    94    99    NA
##  2 2Ge+her    The … 2000-09-02      91    87    92    NA    NA    NA    NA    NA
##  3 3 Doors D… Kryp… 2000-04-08      81    70    68    67    66    57    54    53
##  4 3 Doors D… Loser 2000-10-21      76    76    72    69    67    65    55    59
##  5 504 Boyz   Wobb… 2000-04-15      57    34    25    17    17    31    36    49
##  6 98^0       Give… 2000-08-19      51    39    34    26    26    19     2     2
##  7 A*Teens    Danc… 2000-07-08      97    97    96    95   100    NA    NA    NA
##  8 Aaliyah    I Do… 2000-01-29      84    62    51    41    38    35    35    38
##  9 Aaliyah    Try … 2000-03-18      59    53    38    28    21    18    16    14
## 10 Adams, Yo… Open… 2000-08-26      76    76    74    69    68    67    61    58
## # ℹ 307 more rows
## # ℹ 68 more variables: wk9 <dbl>, wk10 <dbl>, wk11 <dbl>, wk12 <dbl>,
## #   wk13 <dbl>, wk14 <dbl>, wk15 <dbl>, wk16 <dbl>, wk17 <dbl>, wk18 <dbl>,
## #   wk19 <dbl>, wk20 <dbl>, wk21 <dbl>, wk22 <dbl>, wk23 <dbl>, wk24 <dbl>,
## #   wk25 <dbl>, wk26 <dbl>, wk27 <dbl>, wk28 <dbl>, wk29 <dbl>, wk30 <dbl>,
## #   wk31 <dbl>, wk32 <dbl>, wk33 <dbl>, wk34 <dbl>, wk35 <dbl>, wk36 <dbl>,
## #   wk37 <dbl>, wk38 <dbl>, wk39 <dbl>, wk40 <dbl>, wk41 <dbl>, wk42 <dbl>, …
```

In this billboard dataset example, each row is a different track, but the columns represent observations of their rank on the billboard chart in different weeks. So multiple observations are stored across multiple columns. Why is this a problem? It makes it difficult to analyze the data. For example, if we wanted to know how many weeks each song was on the billboard chart, we would have to write a lot of code to parse out the columns and count the number of weeks. Below is the code that is required to create a new data frame that counts the number of weeks each song was on the billboard chart.


``` r
# first we need to get just the columns for week
# it's messy because we need to use regular expression to parse out the columns
week_columns <- grep("^wk", names(billboard), value = TRUE)
print(week_columns)
```

```
##  [1] "wk1"  "wk2"  "wk3"  "wk4"  "wk5"  "wk6"  "wk7"  "wk8"  "wk9"  "wk10"
## [11] "wk11" "wk12" "wk13" "wk14" "wk15" "wk16" "wk17" "wk18" "wk19" "wk20"
## [21] "wk21" "wk22" "wk23" "wk24" "wk25" "wk26" "wk27" "wk28" "wk29" "wk30"
## [31] "wk31" "wk32" "wk33" "wk34" "wk35" "wk36" "wk37" "wk38" "wk39" "wk40"
## [41] "wk41" "wk42" "wk43" "wk44" "wk45" "wk46" "wk47" "wk48" "wk49" "wk50"
## [51] "wk51" "wk52" "wk53" "wk54" "wk55" "wk56" "wk57" "wk58" "wk59" "wk60"
## [61] "wk61" "wk62" "wk63" "wk64" "wk65" "wk66" "wk67" "wk68" "wk69" "wk70"
## [71] "wk71" "wk72" "wk73" "wk74" "wk75" "wk76"
```

``` r
# Make a new data frame that counts the number of weeks each song was on the billboard chart
# This is difficult to read and interpret
number_of_weeks <- apply(billboard[week_columns], 1, function(x) sum(!is.na(x)))
print(number_of_weeks)
```

```
##   [1]  7  3 53 20 18 20  5 20 32 20 11 21 22 24 20  5 29  3 20 32 20 20 31 20 24
##  [26] 15 20 20 21 15  9  3 15 17 20 29 15  9 23 12 20 37 20  3  3 20 19  6  8 11
##  [51] 10  7 20 15  7 11 20 17 12  6 19 20 57 47 13  5 17 21 20 11 18 20 20  3 28
##  [76] 32 32 14  6 28 10 20 15 20 20 20 13 28 14  2 20 21 15 19 10  4  1 20  5 16
## [101] 21 17 12 20 21  1  7  1 20 19 15 12 20 27 20 11  7 12 20 20  8 53 14 14  4
## [126] 13 19 11 28  9 20 12 18 20 17 17 20 20 17 15 20 24 24  8 20  9 15 21 19 44
## [151] 17 15 20 32  6 24 15 20 12  5 20  9 10  5  4  2  3 20  5  8 20 11  9 10  7
## [176] 13 11 18 17 55 20 20 17 14  7 19 22 12 18 20  9 24  5 18 18 20  1 20 13 20
## [201] 20 21 20 14  8 13 20 20 10  6 20  9 23 22 20 30 17 20 23 25 26 16 34 21 27
## [226]  5 13  9  9  4 20 20  6 27 32  8  4 20 20  5  5 14 20 20 19 22 20 20 25 20
## [251] 26 20 26 20 33  2 20  9  5 15 16  6 20 26 28 20 26  4 26 24 24 20 11 20  3
## [276] 12 26 13 17 20 20 20  7  6  5 12 22 20 20 11 20 27 11  4 22  2 16  7 19 20
## [301] 41 21 12  9 11 20  6 20 19 18 15 10  8  6 14  2 39
```

``` r
# merge the number of weeks to the columns for the song
songs_week <- cbind(billboard[,c("artist", "track")], number_of_weeks)

head(songs_week)
```

```
##         artist                   track number_of_weeks
## 1        2 Pac Baby Don't Cry (Keep...               7
## 2      2Ge+her The Hardest Part Of ...               3
## 3 3 Doors Down              Kryptonite              53
## 4 3 Doors Down                   Loser              20
## 5     504 Boyz           Wobble Wobble              18
## 6         98^0 Give Me Just One Nig...              20
```

Here is the same code after we've tidied the data. We use one line to tidy the data and then one line to extract the information we want. We'll go over exactly how to tidy the data shortly; this is just to compare the readability of this code vs the previous block. 


``` r
# This tidies the data
billboard_tidy <- billboard %>% 
  pivot_longer(cols = starts_with("wk"),
               names_to = "week",
               values_to = "ranking",
               values_drop_na = TRUE)

print(billboard_tidy)
```

```
## # A tibble: 5,307 × 5
##    artist  track                   date.entered week  ranking
##    <chr>   <chr>                   <date>       <chr>   <dbl>
##  1 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk1        87
##  2 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk2        82
##  3 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk3        72
##  4 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk4        77
##  5 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk5        87
##  6 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk6        94
##  7 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk7        99
##  8 2Ge+her The Hardest Part Of ... 2000-09-02   wk1        91
##  9 2Ge+her The Hardest Part Of ... 2000-09-02   wk2        87
## 10 2Ge+her The Hardest Part Of ... 2000-09-02   wk3        92
## # ℹ 5,297 more rows
```

``` r
# Once data is tidied, we just need two function calls to get the info we need
# This is much easier to read and interpret
billboard_tidy %>% 
  group_by(artist, track) %>% 
  summarize(number_of_weeks = n())
```

```
## `summarise()` has grouped output by 'artist'. You can override using the
## `.groups` argument.
```

```
## # A tibble: 317 × 3
## # Groups:   artist [228]
##    artist         track                   number_of_weeks
##    <chr>          <chr>                             <int>
##  1 2 Pac          Baby Don't Cry (Keep...               7
##  2 2Ge+her        The Hardest Part Of ...               3
##  3 3 Doors Down   Kryptonite                           53
##  4 3 Doors Down   Loser                                20
##  5 504 Boyz       Wobble Wobble                        18
##  6 98^0           Give Me Just One Nig...              20
##  7 A*Teens        Dancing Queen                         5
##  8 Aaliyah        I Don't Wanna                        20
##  9 Aaliyah        Try Again                            32
## 10 Adams, Yolanda Open My Heart                        20
## # ℹ 307 more rows
```

>**Exercise**: Load the `relig_income` dataset. Is this data tidy? Why or why not?


``` r
relig_income
```

```
## # A tibble: 18 × 11
##    religion `<$10k` `$10-20k` `$20-30k` `$30-40k` `$40-50k` `$50-75k` `$75-100k`
##    <chr>      <dbl>     <dbl>     <dbl>     <dbl>     <dbl>     <dbl>      <dbl>
##  1 Agnostic      27        34        60        81        76       137        122
##  2 Atheist       12        27        37        52        35        70         73
##  3 Buddhist      27        21        30        34        33        58         62
##  4 Catholic     418       617       732       670       638      1116        949
##  5 Don’t k…      15        14        15        11        10        35         21
##  6 Evangel…     575       869      1064       982       881      1486        949
##  7 Hindu          1         9         7         9        11        34         47
##  8 Histori…     228       244       236       238       197       223        131
##  9 Jehovah…      20        27        24        24        21        30         15
## 10 Jewish        19        19        25        25        30        95         69
## 11 Mainlin…     289       495       619       655       651      1107        939
## 12 Mormon        29        40        48        51        56       112         85
## 13 Muslim         6         7         9        10         9        23         16
## 14 Orthodox      13        17        23        32        32        47         38
## 15 Other C…       9         7        11        13        13        14         18
## 16 Other F…      20        33        40        46        49        63         46
## 17 Other W…       5         2         3         4         2         7          3
## 18 Unaffil…     217       299       374       365       341       528        407
## # ℹ 3 more variables: `$100-150k` <dbl>, `>150k` <dbl>,
## #   `Don't know/refused` <dbl>
```

>**Exercise**: Load the `ChickWeight` dataset. Is this data tidy? Why or why not?


``` r
tibble(ChickWeight)
```

```
## # A tibble: 578 × 4
##    weight  Time Chick Diet 
##     <dbl> <dbl> <ord> <fct>
##  1     42     0 1     1    
##  2     51     2 1     1    
##  3     59     4 1     1    
##  4     64     6 1     1    
##  5     76     8 1     1    
##  6     93    10 1     1    
##  7    106    12 1     1    
##  8    125    14 1     1    
##  9    149    16 1     1    
## 10    171    18 1     1    
## # ℹ 568 more rows
```

In the two code blocks above, `relig_income` is not tidy because the income brackets are spread out across the column. In the `ChickWeight` dataset, these data **are** tidy. Each row is a different chick, observed at a different time. 

The type of "untidy" data we've demonstrated so far is untidy because it is what we call "wide" data. In wide data, multiple observations are stored across multiple columns. Tidy data is typically "long" data, where each observation is stored in a single row. An important skill in using tidyverse is to pivot data from wide to long format.

### Pivoting tables between wide and long

To convert this data to a **long** format, we can use the `pivot_longer()` function. The syntax for `pivot_longer()` is as follows:

```
pivot_longer(data, cols, names_to, values_to)
```

* cols = the columns that you want to collapse into a single column
* names_to = the name of the new column that will hold the names of the columns you gathered
* values_to = the name of the new column that will hold the data of the columns you gathered

We start with the `data`, then specify the `cols` we want to gather together (the "wk" columns). This will then take all those column names and put it under a new variable named `names_to`. The values of those weeks, aka the rankings, we're going to pass to `values_to`. So all the data from the "wk" columns will be collapsed into two columns, one for "week" and one for "ranking". The rest of the data will be duplicated as needed to uniquely identify each observation.


``` r
billboard %>% pivot_longer(cols = starts_with("wk"),
                           names_to = "week",
                           values_to = "ranking")
```

```
## # A tibble: 24,092 × 5
##    artist track                   date.entered week  ranking
##    <chr>  <chr>                   <date>       <chr>   <dbl>
##  1 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk1        87
##  2 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk2        82
##  3 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk3        72
##  4 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk4        77
##  5 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk5        87
##  6 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk6        94
##  7 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk7        99
##  8 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk8        NA
##  9 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk9        NA
## 10 2 Pac  Baby Don't Cry (Keep... 2000-02-26   wk10       NA
## # ℹ 24,082 more rows
```

This looks a bit better, but we created a lot of extraneous columns due to the default behavior of `pivot_longer()` creating a row for every combination of the gathered variable (week) and the song. We can have it drop the NA values by adding the argument `values_drop_na = TRUE`. Run the below code and you'll see that our number of rows drops from 24 thousand to 5 thousand by excluding the empty weeks. 


``` r
billboard %>% pivot_longer(cols = starts_with("wk"),
                           names_to = "week",
                           values_to = "ranking",
                           values_drop_na = TRUE)
```

```
## # A tibble: 5,307 × 5
##    artist  track                   date.entered week  ranking
##    <chr>   <chr>                   <date>       <chr>   <dbl>
##  1 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk1        87
##  2 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk2        82
##  3 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk3        72
##  4 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk4        77
##  5 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk5        87
##  6 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk6        94
##  7 2 Pac   Baby Don't Cry (Keep... 2000-02-26   wk7        99
##  8 2Ge+her The Hardest Part Of ... 2000-09-02   wk1        91
##  9 2Ge+her The Hardest Part Of ... 2000-09-02   wk2        87
## 10 2Ge+her The Hardest Part Of ... 2000-09-02   wk3        92
## # ℹ 5,297 more rows
```

>**Exercise**: Look at the `relig_income` dataset. How would you pivot this data to make it tidy? Think of the function `pivot_longer(data, cols, names_to, values_to)`. What would be cols, names_to, and values_to?


``` r
# cols is every column except religion
# names_to would be income bracket, which we can shorten to "income"
# values_to would be the "count" of people in that religion and income bracket
relig_income %>% pivot_longer(cols = !religion,
                             names_to = "income",
                             values_to = "count")
```

```
## # A tibble: 180 × 3
##    religion income             count
##    <chr>    <chr>              <dbl>
##  1 Agnostic <$10k                 27
##  2 Agnostic $10-20k               34
##  3 Agnostic $20-30k               60
##  4 Agnostic $30-40k               81
##  5 Agnostic $40-50k               76
##  6 Agnostic $50-75k              137
##  7 Agnostic $75-100k             122
##  8 Agnostic $100-150k            109
##  9 Agnostic >150k                 84
## 10 Agnostic Don't know/refused    96
## # ℹ 170 more rows
```

In the above example, there are a few other ways to select the columns you want, such as `"<$10k":"Don't know/refused"` or listing them each out `c("<$10k", "$10-20k", ...)`.

>**Exercise**: Look at the dataset `table2`. Is this tidy data? 


``` r
table2
```

```
## # A tibble: 12 × 4
##    country      year type            count
##    <chr>       <dbl> <chr>           <dbl>
##  1 Afghanistan  1999 cases             745
##  2 Afghanistan  1999 population   19987071
##  3 Afghanistan  2000 cases            2666
##  4 Afghanistan  2000 population   20595360
##  5 Brazil       1999 cases           37737
##  6 Brazil       1999 population  172006362
##  7 Brazil       2000 cases           80488
##  8 Brazil       2000 population  174504898
##  9 China        1999 cases          212258
## 10 China        1999 population 1272915272
## 11 China        2000 cases          213766
## 12 China        2000 population 1280428583
```

The table2 dataset is an example of data that is not tidy. Although the data is in a "long" format, it is not tidy because the unit of observation here is the country in a specific year And the thing we are observing are the population and the cases (of disease). More specifically, a column should contain measurements of the same sort of observation, but in this case there are two types of measurements in the same column. This is true even though both measurements are on a count scale. To clean this up, we will need to `pivot` this data from "long" to "wide" using the `pivot_wider()` function. The syntax for `pivot_wider()` looks like this:

```r
pivot_wider(data, names_from, values_from)
```

* names_from = the column that contains the names of the new columns
* values_from = the column that contains the data for these new columns


``` r
table2 %>% pivot_wider(names_from = type, values_from = count)
```

```
## # A tibble: 6 × 4
##   country      year  cases population
##   <chr>       <dbl>  <dbl>      <dbl>
## 1 Afghanistan  1999    745   19987071
## 2 Afghanistan  2000   2666   20595360
## 3 Brazil       1999  37737  172006362
## 4 Brazil       2000  80488  174504898
## 5 China        1999 212258 1272915272
## 6 China        2000 213766 1280428583
```

How does this help us analyze the data? Think about the question "What is the rate of disease in each country?" The rate of the disease is the number of cases divided by the total population. In the long version of the data, we would need to divide rows against each other. In this version, we just need to divide the columns, which are easily accessed by the column names.


``` r
# long version of table2 disease incidence
table2 %>% 
  group_by(country) %>% 
  summarize(rate = sum(count[type == "cases"]) / sum(count[type == "population"]))
```

```
## # A tibble: 3 × 2
##   country          rate
##   <chr>           <dbl>
## 1 Afghanistan 0.0000841
## 2 Brazil      0.000341 
## 3 China       0.000167
```

This is the wide version of `table2`. 


``` r
# wide version of table2 disease incidence
table2_wider <- table2 %>% pivot_wider(names_from = type, values_from = count)

# just use the cases and population to calculate the rate
table2_wider$cases / table2_wider$population
```

```
## [1] 0.0000372741 0.0001294466 0.0002193930 0.0004612363 0.0001667495
## [6] 0.0001669488
```

``` r
# calculate the rate but tack it on to the parent dataset
table2_wider %>% 
  mutate(rate = cases / population)
```

```
## # A tibble: 6 × 5
##   country      year  cases population      rate
##   <chr>       <dbl>  <dbl>      <dbl>     <dbl>
## 1 Afghanistan  1999    745   19987071 0.0000373
## 2 Afghanistan  2000   2666   20595360 0.000129 
## 3 Brazil       1999  37737  172006362 0.000219 
## 4 Brazil       2000  80488  174504898 0.000461 
## 5 China        1999 212258 1272915272 0.000167 
## 6 China        2000 213766 1280428583 0.000167
```
Of course, this approach generates the disease incidence rate for each country for each year. To obtain overall rate across years, you would need to use `group_by()` and `summarize()`.

### Data spread out across multiple files

Another way in which data can be "untidy" is if you have observations spread out across multiple files. It's rare that all our data is already in one single table. Often, we take one type of measurement on one table and have another set of data in another table. For example, you might have visual measurements like color for a group of animals in one table and quantitative measurements like weight for the same animals in another table. 

We can merge tables by performing "mutating joins". In tidyverse, joins are performed one pair of tables at a time, such that, if you have tables x, y, and z, you must first join x and y to produce a new table xy, then join xy and z to create xyz. As we shall see below, a requirement of such joins is that any two tables to be joined contain unique observations on the same variable.


``` r
df1 <- tibble(
  name = c("Daffy", "Donald", "Mickey", "Goofy", "Tweety"),
  species = c("duck", "duck", "mouse", "dog", "bird")
)
df2 <- tibble(
  name = c("Daffy", "Donald", "Mickey", "Goofy", "Minnie"),
  weight = c(5, 6, 3, 10, 4)
)

df3 <- tibble(
  animal = c("duck", "mouse", "dog", "cat"),
  sound = c("quack", "squeak", "bark", "meow")
)
```

In the code block below, we have tables that relate Disney characters to the animal species they are, Disney characters and their weight, and animal species to the sound they make. We want to merge these tables together to get a table that has the Disney characters, their weight, and the sound they make. The set of functions do to this are called **joins**. There are 3 types of joins, inner, left/right, and full joins.

The syntax for all the joins we will be using is the same:

```r
join_function(df1, df2, by = "column_name")
```

The join function takes two tibbles, `df1` and `df2`, and joins them on the column `column_name`. The column name must be present in both tibbles.


#### Inner joins

The inner join only preserves rows that have matching data in both tables. 


``` r
inner_join(df1, df2, by = "name")
```

```
## # A tibble: 4 × 3
##   name   species weight
##   <chr>  <chr>    <dbl>
## 1 Daffy  duck         5
## 2 Donald duck         6
## 3 Mickey mouse        3
## 4 Goofy  dog         10
```

Here's what the three tables would look like if we chain joined them with `inner_join()`:


``` r
df1 %>% 
  inner_join(df2, by = "name") %>% 
  inner_join(df3, by = c("species" = "animal")) # this is what to do if the column names are different
```

```
## # A tibble: 4 × 4
##   name   species weight sound 
##   <chr>  <chr>    <dbl> <chr> 
## 1 Daffy  duck         5 quack 
## 2 Donald duck         6 quack 
## 3 Mickey mouse        3 squeak
## 4 Goofy  dog         10 bark
```

#### Left/right joins

In a `left_join()`, when given tables x and y, the result is to retain all rows in x, regardless if there is matching data in y: missing data in y will get returned as NAs in the new table.


``` r
left_join(df1, df2, by = "name")
```

```
## # A tibble: 5 × 3
##   name   species weight
##   <chr>  <chr>    <dbl>
## 1 Daffy  duck         5
## 2 Donald duck         6
## 3 Mickey mouse        3
## 4 Goofy  dog         10
## 5 Tweety bird        NA
```

Here's the result of chaining the three tables with `left_join()`:


``` r
df1 %>% 
  left_join(df2, by = "name") %>% 
  left_join(df3, by = c("species" = "animal"))
```

```
## # A tibble: 5 × 4
##   name   species weight sound 
##   <chr>  <chr>    <dbl> <chr> 
## 1 Daffy  duck         5 quack 
## 2 Donald duck         6 quack 
## 3 Mickey mouse        3 squeak
## 4 Goofy  dog         10 bark  
## 5 Tweety bird        NA <NA>
```

#### Full joins

In full joins, you keep all the data from both tables, and fill in missing data with NAs. Here's what a full join of all three tables looks like. 


``` r
df1 %>% 
  full_join(df2, by = "name") %>% 
  full_join(df3, by = c("species" = "animal"))
```

```
## # A tibble: 7 × 4
##   name   species weight sound 
##   <chr>  <chr>    <dbl> <chr> 
## 1 Daffy  duck         5 quack 
## 2 Donald duck         6 quack 
## 3 Mickey mouse        3 squeak
## 4 Goofy  dog         10 bark  
## 5 Tweety bird        NA <NA>  
## 6 Minnie <NA>         4 <NA>  
## 7 <NA>   cat         NA meow
```

You can also join by multiple columns, in cases where it takes two or more columns to uniquely identify an observation.

The key concept to understanding joins is the idea of **relational data**. In relational data, you have multiple tables that are related to each other by common variables/columns. In the examples above, one of the common columns was the name of the Disney character. Some sets of data might have multiple columns that are related to each other. 

Here is a more advanced example of joining multiple datasets together. The `nycflights13` package contains a set of tables relating to flights out of the three NYC airports. 


``` r
if(!require(nycflights13)){install.packages("nycflights13", quiet=TRUE)}
library(nycflights13)
```


``` r
glimpse(flights)
```

```
## Rows: 336,776
## Columns: 19
## $ year           <int> 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2…
## $ month          <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ day            <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ dep_time       <int> 517, 533, 542, 544, 554, 554, 555, 557, 557, 558, 558, …
## $ sched_dep_time <int> 515, 529, 540, 545, 600, 558, 600, 600, 600, 600, 600, …
## $ dep_delay      <dbl> 2, 4, 2, -1, -6, -4, -5, -3, -3, -2, -2, -2, -2, -2, -1…
## $ arr_time       <int> 830, 850, 923, 1004, 812, 740, 913, 709, 838, 753, 849,…
## $ sched_arr_time <int> 819, 830, 850, 1022, 837, 728, 854, 723, 846, 745, 851,…
## $ arr_delay      <dbl> 11, 20, 33, -18, -25, 12, 19, -14, -8, 8, -2, -3, 7, -1…
## $ carrier        <chr> "UA", "UA", "AA", "B6", "DL", "UA", "B6", "EV", "B6", "…
## $ flight         <int> 1545, 1714, 1141, 725, 461, 1696, 507, 5708, 79, 301, 4…
## $ tailnum        <chr> "N14228", "N24211", "N619AA", "N804JB", "N668DN", "N394…
## $ origin         <chr> "EWR", "LGA", "JFK", "JFK", "LGA", "EWR", "EWR", "LGA",…
## $ dest           <chr> "IAH", "IAH", "MIA", "BQN", "ATL", "ORD", "FLL", "IAD",…
## $ air_time       <dbl> 227, 227, 160, 183, 116, 150, 158, 53, 140, 138, 149, 1…
## $ distance       <dbl> 1400, 1416, 1089, 1576, 762, 719, 1065, 229, 944, 733, …
## $ hour           <dbl> 5, 5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6…
## $ minute         <dbl> 15, 29, 40, 45, 0, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 59, 0…
## $ time_hour      <dttm> 2013-01-01 05:00:00, 2013-01-01 05:00:00, 2013-01-01 0…
```


``` r
glimpse(airlines)
```

```
## Rows: 16
## Columns: 2
## $ carrier <chr> "9E", "AA", "AS", "B6", "DL", "EV", "F9", "FL", "HA", "MQ", "O…
## $ name    <chr> "Endeavor Air Inc.", "American Airlines Inc.", "Alaska Airline…
```


``` r
glimpse(planes)
```

```
## Rows: 3,322
## Columns: 9
## $ tailnum      <chr> "N10156", "N102UW", "N103US", "N104UW", "N10575", "N105UW…
## $ year         <int> 2004, 1998, 1999, 1999, 2002, 1999, 1999, 1999, 1999, 199…
## $ type         <chr> "Fixed wing multi engine", "Fixed wing multi engine", "Fi…
## $ manufacturer <chr> "EMBRAER", "AIRBUS INDUSTRIE", "AIRBUS INDUSTRIE", "AIRBU…
## $ model        <chr> "EMB-145XR", "A320-214", "A320-214", "A320-214", "EMB-145…
## $ engines      <int> 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, …
## $ seats        <int> 55, 182, 182, 182, 55, 182, 182, 182, 182, 182, 55, 55, 5…
## $ speed        <int> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, N…
## $ engine       <chr> "Turbo-fan", "Turbo-fan", "Turbo-fan", "Turbo-fan", "Turb…
```


``` r
glimpse(airports)
```

```
## Rows: 1,458
## Columns: 8
## $ faa   <chr> "04G", "06A", "06C", "06N", "09J", "0A9", "0G6", "0G7", "0P2", "…
## $ name  <chr> "Lansdowne Airport", "Moton Field Municipal Airport", "Schaumbur…
## $ lat   <dbl> 41.13047, 32.46057, 41.98934, 41.43191, 31.07447, 36.37122, 41.4…
## $ lon   <dbl> -80.61958, -85.68003, -88.10124, -74.39156, -81.42778, -82.17342…
## $ alt   <dbl> 1044, 264, 801, 523, 11, 1593, 730, 492, 1000, 108, 409, 875, 10…
## $ tz    <dbl> -5, -6, -6, -5, -5, -5, -5, -5, -5, -8, -5, -6, -5, -5, -5, -5, …
## $ dst   <chr> "A", "A", "A", "A", "A", "A", "A", "A", "U", "A", "A", "U", "A",…
## $ tzone <chr> "America/New_York", "America/Chicago", "America/Chicago", "Ameri…
```


``` r
glimpse(weather)
```

```
## Rows: 26,115
## Columns: 15
## $ origin     <chr> "EWR", "EWR", "EWR", "EWR", "EWR", "EWR", "EWR", "EWR", "EW…
## $ year       <int> 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013,…
## $ month      <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,…
## $ day        <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,…
## $ hour       <int> 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, …
## $ temp       <dbl> 39.02, 39.02, 39.02, 39.92, 39.02, 37.94, 39.02, 39.92, 39.…
## $ dewp       <dbl> 26.06, 26.96, 28.04, 28.04, 28.04, 28.04, 28.04, 28.04, 28.…
## $ humid      <dbl> 59.37, 61.63, 64.43, 62.21, 64.43, 67.21, 64.43, 62.21, 62.…
## $ wind_dir   <dbl> 270, 250, 240, 250, 260, 240, 240, 250, 260, 260, 260, 330,…
## $ wind_speed <dbl> 10.35702, 8.05546, 11.50780, 12.65858, 12.65858, 11.50780, …
## $ wind_gust  <dbl> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, 20.…
## $ precip     <dbl> 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,…
## $ pressure   <dbl> 1012.0, 1012.3, 1012.5, 1012.2, 1011.9, 1012.4, 1012.2, 101…
## $ visib      <dbl> 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10,…
## $ time_hour  <dttm> 2013-01-01 01:00:00, 2013-01-01 02:00:00, 2013-01-01 03:00…
```

In this complex dataset, we have a table of flights, airlines, planes, airports, and weather. They all share some common columns, though the columns may not be named the same. For example, the `flights` table has `carrier` column that directly corresponds to the `airlines` table's `carrier` column. But the `origin` and `dest` columns in the `flights` table correspond to the `faa` column in the `airports` table.

[Here](https://r4ds.hadley.nz/joins.html#fig-flights-relationships) is a graphic of how these tables are related. (This is from the R4DS book, which is a great resource for learning tidyverse).

>**Exercise**: By looking at this table, can you see how we would go about joining these tables together? If you wanted to know which airlines were the most delayed, which tables would you need to join together? What if you want to know the relationship between the age of a plane and its delay time?


>**Exercise**: Compare the two code blocks below. What is different between the results?


``` r
flights %>% 
  left_join(planes) %>% 
  glimpse()
```

```
## Joining with `by = join_by(year, tailnum)`
```

```
## Rows: 336,776
## Columns: 26
## $ year           <int> 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2…
## $ month          <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ day            <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ dep_time       <int> 517, 533, 542, 544, 554, 554, 555, 557, 557, 558, 558, …
## $ sched_dep_time <int> 515, 529, 540, 545, 600, 558, 600, 600, 600, 600, 600, …
## $ dep_delay      <dbl> 2, 4, 2, -1, -6, -4, -5, -3, -3, -2, -2, -2, -2, -2, -1…
## $ arr_time       <int> 830, 850, 923, 1004, 812, 740, 913, 709, 838, 753, 849,…
## $ sched_arr_time <int> 819, 830, 850, 1022, 837, 728, 854, 723, 846, 745, 851,…
## $ arr_delay      <dbl> 11, 20, 33, -18, -25, 12, 19, -14, -8, 8, -2, -3, 7, -1…
## $ carrier        <chr> "UA", "UA", "AA", "B6", "DL", "UA", "B6", "EV", "B6", "…
## $ flight         <int> 1545, 1714, 1141, 725, 461, 1696, 507, 5708, 79, 301, 4…
## $ tailnum        <chr> "N14228", "N24211", "N619AA", "N804JB", "N668DN", "N394…
## $ origin         <chr> "EWR", "LGA", "JFK", "JFK", "LGA", "EWR", "EWR", "LGA",…
## $ dest           <chr> "IAH", "IAH", "MIA", "BQN", "ATL", "ORD", "FLL", "IAD",…
## $ air_time       <dbl> 227, 227, 160, 183, 116, 150, 158, 53, 140, 138, 149, 1…
## $ distance       <dbl> 1400, 1416, 1089, 1576, 762, 719, 1065, 229, 944, 733, …
## $ hour           <dbl> 5, 5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6…
## $ minute         <dbl> 15, 29, 40, 45, 0, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 59, 0…
## $ time_hour      <dttm> 2013-01-01 05:00:00, 2013-01-01 05:00:00, 2013-01-01 0…
## $ type           <chr> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ manufacturer   <chr> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ model          <chr> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ engines        <int> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ seats          <int> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ speed          <int> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ engine         <chr> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
```


``` r
flights %>% 
  left_join(planes, by="tailnum") %>% 
  glimpse()
```

```
## Rows: 336,776
## Columns: 27
## $ year.x         <int> 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2013, 2…
## $ month          <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ day            <int> 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1…
## $ dep_time       <int> 517, 533, 542, 544, 554, 554, 555, 557, 557, 558, 558, …
## $ sched_dep_time <int> 515, 529, 540, 545, 600, 558, 600, 600, 600, 600, 600, …
## $ dep_delay      <dbl> 2, 4, 2, -1, -6, -4, -5, -3, -3, -2, -2, -2, -2, -2, -1…
## $ arr_time       <int> 830, 850, 923, 1004, 812, 740, 913, 709, 838, 753, 849,…
## $ sched_arr_time <int> 819, 830, 850, 1022, 837, 728, 854, 723, 846, 745, 851,…
## $ arr_delay      <dbl> 11, 20, 33, -18, -25, 12, 19, -14, -8, 8, -2, -3, 7, -1…
## $ carrier        <chr> "UA", "UA", "AA", "B6", "DL", "UA", "B6", "EV", "B6", "…
## $ flight         <int> 1545, 1714, 1141, 725, 461, 1696, 507, 5708, 79, 301, 4…
## $ tailnum        <chr> "N14228", "N24211", "N619AA", "N804JB", "N668DN", "N394…
## $ origin         <chr> "EWR", "LGA", "JFK", "JFK", "LGA", "EWR", "EWR", "LGA",…
## $ dest           <chr> "IAH", "IAH", "MIA", "BQN", "ATL", "ORD", "FLL", "IAD",…
## $ air_time       <dbl> 227, 227, 160, 183, 116, 150, 158, 53, 140, 138, 149, 1…
## $ distance       <dbl> 1400, 1416, 1089, 1576, 762, 719, 1065, 229, 944, 733, …
## $ hour           <dbl> 5, 5, 5, 5, 6, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 5, 6, 6, 6…
## $ minute         <dbl> 15, 29, 40, 45, 0, 58, 0, 0, 0, 0, 0, 0, 0, 0, 0, 59, 0…
## $ time_hour      <dttm> 2013-01-01 05:00:00, 2013-01-01 05:00:00, 2013-01-01 0…
## $ year.y         <int> 1999, 1998, 1990, 2012, 1991, 2012, 2000, 1998, 2004, N…
## $ type           <chr> "Fixed wing multi engine", "Fixed wing multi engine", "…
## $ manufacturer   <chr> "BOEING", "BOEING", "BOEING", "AIRBUS", "BOEING", "BOEI…
## $ model          <chr> "737-824", "737-824", "757-223", "A320-232", "757-232",…
## $ engines        <int> 2, 2, 2, 2, 2, 2, 2, 2, 2, NA, 2, 2, 2, 2, NA, 2, 2, 2,…
## $ seats          <int> 149, 149, 178, 200, 178, 191, 200, 55, 200, NA, 200, 20…
## $ speed          <int> NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA, NA,…
## $ engine         <chr> "Turbo-fan", "Turbo-fan", "Turbo-fan", "Turbo-fan", "Tu…
```

In the first code block the tables were joined by "year" and "tailnum". But this is **incorrect** because the `year` column in the `flights` table is the year of the flight, while the `year` column in the `planes` table is the year the plane was manufactured. In the second code block, the tables were joined only by `tailnum` and the two columns for year were renamed `year.x` and `year.y`, corresponding to the year of the flight and the year the plane was manufactured, respectively. It's important to be aware of the columns you are joining on and what they represent. 

### Data transformation with tidyverse

Now that we've covered the two major aspects of tidying data, that is, transforming data from wide to long and merging data from multiple tables, we can talk briefly about data transformation. In this section, we will be working with already tidy data and using various functions to pull out different information from the table. This is not meant as an exhaustive list of functions, but rather a demonstration of the types of things you can do with tidy data. 

### Filtering data

You can select certain rows of a table based on boolean conditions using the `filter()` function. 


``` r
mpg %>% filter(manufacturer == "audi")
```

```
## # A tibble: 18 × 11
##    manufacturer model      displ  year   cyl trans drv     cty   hwy fl    class
##    <chr>        <chr>      <dbl> <int> <int> <chr> <chr> <int> <int> <chr> <chr>
##  1 audi         a4           1.8  1999     4 auto… f        18    29 p     comp…
##  2 audi         a4           1.8  1999     4 manu… f        21    29 p     comp…
##  3 audi         a4           2    2008     4 manu… f        20    31 p     comp…
##  4 audi         a4           2    2008     4 auto… f        21    30 p     comp…
##  5 audi         a4           2.8  1999     6 auto… f        16    26 p     comp…
##  6 audi         a4           2.8  1999     6 manu… f        18    26 p     comp…
##  7 audi         a4           3.1  2008     6 auto… f        18    27 p     comp…
##  8 audi         a4 quattro   1.8  1999     4 manu… 4        18    26 p     comp…
##  9 audi         a4 quattro   1.8  1999     4 auto… 4        16    25 p     comp…
## 10 audi         a4 quattro   2    2008     4 manu… 4        20    28 p     comp…
## 11 audi         a4 quattro   2    2008     4 auto… 4        19    27 p     comp…
## 12 audi         a4 quattro   2.8  1999     6 auto… 4        15    25 p     comp…
## 13 audi         a4 quattro   2.8  1999     6 manu… 4        17    25 p     comp…
## 14 audi         a4 quattro   3.1  2008     6 auto… 4        17    25 p     comp…
## 15 audi         a4 quattro   3.1  2008     6 manu… 4        15    25 p     comp…
## 16 audi         a6 quattro   2.8  1999     6 auto… 4        15    24 p     mids…
## 17 audi         a6 quattro   3.1  2008     6 auto… 4        17    25 p     mids…
## 18 audi         a6 quattro   4.2  2008     8 auto… 4        16    23 p     mids…
```

You can use multiple conditions by separating them with a comma. This is equivalent to using & to join two boolean expressions together. 


``` r
mpg %>% filter(manufacturer == "audi", year < 2000)
```

```
## # A tibble: 9 × 11
##   manufacturer model      displ  year   cyl trans  drv     cty   hwy fl    class
##   <chr>        <chr>      <dbl> <int> <int> <chr>  <chr> <int> <int> <chr> <chr>
## 1 audi         a4           1.8  1999     4 auto(… f        18    29 p     comp…
## 2 audi         a4           1.8  1999     4 manua… f        21    29 p     comp…
## 3 audi         a4           2.8  1999     6 auto(… f        16    26 p     comp…
## 4 audi         a4           2.8  1999     6 manua… f        18    26 p     comp…
## 5 audi         a4 quattro   1.8  1999     4 manua… 4        18    26 p     comp…
## 6 audi         a4 quattro   1.8  1999     4 auto(… 4        16    25 p     comp…
## 7 audi         a4 quattro   2.8  1999     6 auto(… 4        15    25 p     comp…
## 8 audi         a4 quattro   2.8  1999     6 manua… 4        17    25 p     comp…
## 9 audi         a6 quattro   2.8  1999     6 auto(… 4        15    24 p     mids…
```

### Selecting columns

You can select a subset of the columns in a table using the `select()` function and specifying the columns you want. 


``` r
mpg %>% select(manufacturer, model, year)
```

```
## # A tibble: 234 × 3
##    manufacturer model       year
##    <chr>        <chr>      <int>
##  1 audi         a4          1999
##  2 audi         a4          1999
##  3 audi         a4          2008
##  4 audi         a4          2008
##  5 audi         a4          1999
##  6 audi         a4          1999
##  7 audi         a4          2008
##  8 audi         a4 quattro  1999
##  9 audi         a4 quattro  1999
## 10 audi         a4 quattro  2008
## # ℹ 224 more rows
```

Another way to get the columns you want is to use the `starts_with()`, `ends_with()`, `contains()`, and `matches()` functions. 


``` r
weather %>% select(starts_with("wind"))
```

```
## # A tibble: 26,115 × 3
##    wind_dir wind_speed wind_gust
##       <dbl>      <dbl>     <dbl>
##  1      270      10.4         NA
##  2      250       8.06        NA
##  3      240      11.5         NA
##  4      250      12.7         NA
##  5      260      12.7         NA
##  6      240      11.5         NA
##  7      240      15.0         NA
##  8      250      10.4         NA
##  9      260      15.0         NA
## 10      260      13.8         NA
## # ℹ 26,105 more rows
```

``` r
billboard %>% select(contains("wk"))
```

```
## # A tibble: 317 × 76
##      wk1   wk2   wk3   wk4   wk5   wk6   wk7   wk8   wk9  wk10  wk11  wk12  wk13
##    <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
##  1    87    82    72    77    87    94    99    NA    NA    NA    NA    NA    NA
##  2    91    87    92    NA    NA    NA    NA    NA    NA    NA    NA    NA    NA
##  3    81    70    68    67    66    57    54    53    51    51    51    51    47
##  4    76    76    72    69    67    65    55    59    62    61    61    59    61
##  5    57    34    25    17    17    31    36    49    53    57    64    70    75
##  6    51    39    34    26    26    19     2     2     3     6     7    22    29
##  7    97    97    96    95   100    NA    NA    NA    NA    NA    NA    NA    NA
##  8    84    62    51    41    38    35    35    38    38    36    37    37    38
##  9    59    53    38    28    21    18    16    14    12    10     9     8     6
## 10    76    76    74    69    68    67    61    58    57    59    66    68    61
## # ℹ 307 more rows
## # ℹ 63 more variables: wk14 <dbl>, wk15 <dbl>, wk16 <dbl>, wk17 <dbl>,
## #   wk18 <dbl>, wk19 <dbl>, wk20 <dbl>, wk21 <dbl>, wk22 <dbl>, wk23 <dbl>,
## #   wk24 <dbl>, wk25 <dbl>, wk26 <dbl>, wk27 <dbl>, wk28 <dbl>, wk29 <dbl>,
## #   wk30 <dbl>, wk31 <dbl>, wk32 <dbl>, wk33 <dbl>, wk34 <dbl>, wk35 <dbl>,
## #   wk36 <dbl>, wk37 <dbl>, wk38 <dbl>, wk39 <dbl>, wk40 <dbl>, wk41 <dbl>,
## #   wk42 <dbl>, wk43 <dbl>, wk44 <dbl>, wk45 <dbl>, wk46 <dbl>, wk47 <dbl>, …
```

### Adding new columns/variables with `mutate()`

The `mutate()` function is a useful tool for adding a new column to the end of your table, usually after performing some operation where you calculate a value from existing variables. The syntax is as follows:

```r
mutate(data, new_column_name = operation)
```

When you perform operations on existing columns, you don't need to use the `$` operator to access the columns. 


``` r
flights %>% 
  mutate(avg_speed = distance / air_time * 60,
         gain = dep_delay - arr_delay)
```

```
## # A tibble: 336,776 × 21
##     year month   day dep_time sched_dep_time dep_delay arr_time sched_arr_time
##    <int> <int> <int>    <int>          <int>     <dbl>    <int>          <int>
##  1  2013     1     1      517            515         2      830            819
##  2  2013     1     1      533            529         4      850            830
##  3  2013     1     1      542            540         2      923            850
##  4  2013     1     1      544            545        -1     1004           1022
##  5  2013     1     1      554            600        -6      812            837
##  6  2013     1     1      554            558        -4      740            728
##  7  2013     1     1      555            600        -5      913            854
##  8  2013     1     1      557            600        -3      709            723
##  9  2013     1     1      557            600        -3      838            846
## 10  2013     1     1      558            600        -2      753            745
## # ℹ 336,766 more rows
## # ℹ 13 more variables: arr_delay <dbl>, carrier <chr>, flight <int>,
## #   tailnum <chr>, origin <chr>, dest <chr>, air_time <dbl>, distance <dbl>,
## #   hour <dbl>, minute <dbl>, time_hour <dttm>, avg_speed <dbl>, gain <dbl>
```

>**Exercise**: Read the code below and see if you can work out what each line is doing


``` r
mpg %>% 
  filter(manufacturer == "audi") %>% 
  mutate(avg_mpg = (cty + hwy) / 2) %>%
  select(manufacturer, model, year, avg_mpg)
```

```
## # A tibble: 18 × 4
##    manufacturer model       year avg_mpg
##    <chr>        <chr>      <int>   <dbl>
##  1 audi         a4          1999    23.5
##  2 audi         a4          1999    25  
##  3 audi         a4          2008    25.5
##  4 audi         a4          2008    25.5
##  5 audi         a4          1999    21  
##  6 audi         a4          1999    22  
##  7 audi         a4          2008    22.5
##  8 audi         a4 quattro  1999    22  
##  9 audi         a4 quattro  1999    20.5
## 10 audi         a4 quattro  2008    24  
## 11 audi         a4 quattro  2008    23  
## 12 audi         a4 quattro  1999    20  
## 13 audi         a4 quattro  1999    21  
## 14 audi         a4 quattro  2008    21  
## 15 audi         a4 quattro  2008    20  
## 16 audi         a6 quattro  1999    19.5
## 17 audi         a6 quattro  2008    21  
## 18 audi         a6 quattro  2008    19.5
```

### Grouping and summarizing data

One of the most common things we want to do is summarize data by groups. For example, we might want to know the number of car models for each manufacturer. We will use a combination of the functions `group_by()` and `summarize()` to do this. The `group_by` function adds metadata to the table that indicates which group each row belongs to. Then, when we apply operations using the `summarize()` function, those operations are performed separately for each group. In this way, we can calculate summary statistics for each unique value of a variable. 

In the code below, we want to calculate for each unique value of `manufacturer`, the number of unique values of `model`. So we group by `manufacturer` and then summarize the number of distinct values of `model`. The operation we perform inside the `summarize` function is `n_distinct()`, which counts the number of unique values in a column. 


``` r
mpg %>% 
  group_by(manufacturer) %>%
  summarize(n_distinct(model))
```

```
## # A tibble: 15 × 2
##    manufacturer `n_distinct(model)`
##    <chr>                      <int>
##  1 audi                           3
##  2 chevrolet                      4
##  3 dodge                          4
##  4 ford                           4
##  5 honda                          1
##  6 hyundai                        2
##  7 jeep                           1
##  8 land rover                     1
##  9 lincoln                        1
## 10 mercury                        1
## 11 nissan                         3
## 12 pontiac                        1
## 13 subaru                         2
## 14 toyota                         6
## 15 volkswagen                     4
```

This is what it would look like if we didn't group_by first. We get the total number of unique values of `model` in the entire dataset. 


``` r
mpg %>% summarise(n_distinct(model))
```

```
## # A tibble: 1 × 1
##   `n_distinct(model)`
##                 <int>
## 1                  38
```

Here is another example where we calculate the average departure delay for each airline. We also use the `left_join()` function to merge the `airlines` table with the `flights` table. 


``` r
flights %>% 
  group_by(carrier) %>% 
  summarize(avg_delay = mean(dep_delay, na.rm = TRUE)) %>% 
  left_join(airlines, by = c("carrier" = "carrier"))
```

```
## # A tibble: 16 × 3
##    carrier avg_delay name                       
##    <chr>       <dbl> <chr>                      
##  1 9E          16.7  Endeavor Air Inc.          
##  2 AA           8.59 American Airlines Inc.     
##  3 AS           5.80 Alaska Airlines Inc.       
##  4 B6          13.0  JetBlue Airways            
##  5 DL           9.26 Delta Air Lines Inc.       
##  6 EV          20.0  ExpressJet Airlines Inc.   
##  7 F9          20.2  Frontier Airlines Inc.     
##  8 FL          18.7  AirTran Airways Corporation
##  9 HA           4.90 Hawaiian Airlines Inc.     
## 10 MQ          10.6  Envoy Air                  
## 11 OO          12.6  SkyWest Airlines Inc.      
## 12 UA          12.1  United Air Lines Inc.      
## 13 US           3.78 US Airways Inc.            
## 14 VX          12.9  Virgin America             
## 15 WN          17.7  Southwest Airlines Co.     
## 16 YV          19.0  Mesa Airlines Inc.
```

>**Exercise**: Assuming that any flight with `NA` in the `dep_time` column is a cancelled flight, how would you calculate the number of cancelled flights for each airport? What would you group by and what would you summarize? (don't worry about the actual function names)


``` r
flights %>% 
  group_by(origin) %>% 
  summarize(n_cancelled = sum(is.na(dep_time))) %>% 
  left_join(airports, by = c("origin" = "faa"))
```

```
## # A tibble: 3 × 9
##   origin n_cancelled name                  lat   lon   alt    tz dst   tzone    
##   <chr>        <int> <chr>               <dbl> <dbl> <dbl> <dbl> <chr> <chr>    
## 1 EWR           3239 Newark Liberty Intl  40.7 -74.2    18    -5 A     America/…
## 2 JFK           1863 John F Kennedy Intl  40.6 -73.8    13    -5 A     America/…
## 3 LGA           3153 La Guardia           40.8 -73.9    22    -5 A     America/…
```

## Putting it all together

As a summary, here is an example of how you might use all the functions we've learned today to find out differences in weather conditions for cancelled flights out of JFK. 


``` r
# Find out the weather condition of cancelled flights from JFK
flights %>% 
  filter(origin=="JFK") %>% 
  left_join(weather, by = c("origin", "time_hour")) %>% 
  mutate(cancelled = is.na(dep_time)) %>%
  group_by(cancelled) %>% 
  summarize(n = n(), wind_speed = mean(wind_speed, na.rm = TRUE), wind_gust = mean(wind_gust, na.rm = TRUE), precip = mean(precip, na.rm = TRUE))
```

```
## # A tibble: 2 × 5
##   cancelled      n wind_speed wind_gust  precip
##   <lgl>      <int>      <dbl>     <dbl>   <dbl>
## 1 FALSE     109416       12.2      27.5 0.00357
## 2 TRUE        1863       15.8      32.5 0.0144
```

