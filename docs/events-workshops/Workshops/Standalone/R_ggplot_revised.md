---
title: "Harvard Informatics R ggplot Workshop"
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

Hello everyone. Let's get oriented to how today's ggplot workshop is going to run. I will be sharing my screen in RStudio as I demonstrate plotting with ggplot. You all should also open up your RStudio and download and open this document, which you can find on our website (TBD Short link to download) and follow along.

For those who are not familiar with this file format, this is an RMarkdown file, which is a mixture of formatted text and **code blocks**. Code is written and executed in these code blocks, which are delineated by the back tick character (\`). Each code block can have a language specified (in our case we will exclusively use `r`) as well as options specific to that block. Here is an example of an R code block in this R Markdown file:


``` r
getwd()
```

``` r
print("hello world")
```

In the code block above, we can run the code by clicking the green triangle in the upper right.

We can also use keyboard shortcuts to run code using *ctrl+enter*/*cmd+enter*.

## This workshop: What to expect

Because this is a short workshop, we're going to focus on the underlying design principles of ggplot so that you can develop an intuition of how plots are put together and how to customize them. We won't be showcasing every type of plot you can make or every function you can use with ggplot. Instead, we'll give you the tools to be able to switch between different plot types and customize them to your liking.

Specifically, we'll learn how:

1.  A core principle of ggplot is separation between how the input *data* is mapped to visuals (called 'aesthetics' in ggplot lingo), and the *non-data elements* of these visuals. Figuring out how to modify an aspect of a plot requires understanding whether it is a *data* or *non-data* element.
2.  ggplot builds plots by combining different aspects of the plot as *layers* (some of which are referred to as *geoms* in ggplot lingo).

We'll guide you in depth in creating a single type of plot (scatter plot) while emphasizing these principles, which are generalizable to any other type of plot you can make in ggplot. After this workshop, we want you to know how to build a basic plot and know where to look for customization options.

## Introduction to ggplot

[ggplot](https://ggplot2.tidyverse.org/) is a **package** (library of code with various functions) that is part of the **tidyverse**. It uses a somewhat standardized 'grammar of graphics' ([book](https://id.lib.harvard.edu/alma/990082021020203941/catalog); [paper](https://hollis.harvard.edu/permalink/f/1mdq5o5/TN_cdi_informaworld_taylorfrancis_310_1198_jcgs_2009_07098)) in its syntax to make almost every aspect of a plot customizable. The input to ggplot are **data frames** and **tibbles**, and the best way to organize your data so that it is easily plotted is by ggplot is following the **tidy** principles, which is why it's part of the tidyverse.

If you haven't already, download and install the tidyverse bundle of packages and load it. ggplot2 is one of the packages bundled with it. We'll also install and load the `palmerpenguins` package, which contains the sample dataset we're working with.

Do so by running this code block (by clicking the green triangle in the upper right, or by placing the cursor in the code block and using *ctrl+enter*/*cmd+enter*.)


``` r
installed_packages <- rownames(installed.packages())

for (pkg in c("tidyverse", "palmerpenguins")) {
  if (!pkg %in% installed_packages) {
    install.packages(pkg, quiet = TRUE)
  }
  library(pkg, character.only = TRUE)
}
```

As noted above, we're going to be working with the `penguins` data set. This is a dataset of mixed data, meaning some variables are categorical and some are numerical, collected about penguins at a research station. It is organized so that each row is a single penguin and each column are the measurements taken of the penguins. You can view the data set by running the following code block:


``` r
glimpse(penguins)
```

```
## Rows: 344
## Columns: 8
## $ species           <fct> Adelie, Adelie, Adelie, Adelie, Adelie, Adelie, Adel…
## $ island            <fct> Torgersen, Torgersen, Torgersen, Torgersen, Torgerse…
## $ bill_length_mm    <dbl> 39.1, 39.5, 40.3, NA, 36.7, 39.3, 38.9, 39.2, 34.1, …
## $ bill_depth_mm     <dbl> 18.7, 17.4, 18.0, NA, 19.3, 20.6, 17.8, 19.6, 18.1, …
## $ flipper_length_mm <int> 181, 186, 195, NA, 193, 190, 181, 195, 193, 190, 186…
## $ body_mass_g       <int> 3750, 3800, 3250, NA, 3450, 3650, 3625, 4675, 3475, …
## $ sex               <fct> male, female, female, NA, female, male, female, male…
## $ year              <int> 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007, 2007…
```

## Building a basic plot: aesthetics and layers

What goes into constructing a plot? Let's begin by going over two important concepts of ggplot: **aesthetics** and **layers**.

A ggplot starts by defining a graphical object (or **grob**) with the `ggplot()` function and telling it the source of the data for the plot, like this:


``` r
ggplot(penguins)
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-5-1.png)<!-- -->

However, in the above example, only a grey box is displayed. This is because, while we've told ggplot *which* dataset to use (`penguins`), we haven't told it what *parts of the data* to plot yet. To do so, we need to specify the variables to plot along each axis as **aesthetics**.

For example, if I wanted to plot two columns from the `penguins` dataset called `bill_length_mm` and `bill_depth_mm` that I wanted to use in my plot, I would do the following:


``` r
ggplot(penguins, aes(x = bill_depth_mm, y = bill_length_mm))
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-6-1.png)<!-- -->

Now, it looks like we have added axes on our white box, but nothing else. At this point, we've told ggplot the dataset to use (`penguins`) and which parts of that dataset to use (`bill_length_mm` and `bill_depth_mm`), but now *how* to display the data.

We need to tell ggplot how to interpret the aesthetics as a graphical representation, i.e. do we want points, lines, bars, etc. We do this by adding **layers** onto the plot with the `+` operator. Each `+` indicates a new layer in the specified ggplot object and many layers can be added to a single plot in order to display the data in different ways. Every aspect of a plot can be controlled with different layers. The layer we add when telling ggplot how to plot the aesthetics (data) is usually called a **geom** (short for geometry).

There are many types of geoms depending on what relationship you are trying to plot. A list of geoms can be found [here](https://ggplot2.tidyverse.org/reference/#geoms). For example, let's say we want to visualize the distribution of the penguins' body mass. Single distributions are typically plotted as histograms or density plots. So to generate the histogram, we would follow these steps:

1.  Specify the dataset (in our case, `penguins`)
2.  Identify the variables in the dataset to plot and specify them as aesthetics. This will require you to look at your data! For our first example, it will be `body_mass_g`
3.  Add a geom layer with the `+` operator that tells ggplot how to display the specified data:

Here's what that looks like. Run the following code block:


``` r
ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram()
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-7-1.png)<!-- -->

A great feature of ggplot is that it does calculations and data transformations for you under the hood. In this code, we only specified that we want the x axis to be body mass and `geom_histogram()` automatically inferred that we want the counts of the body mass to be plotted on the y. It also calculated how wide each bin should be given a default bin number of 30.

Importantly, each layer itself is a function that can take **arguments** (or **parameters**/**options**) as input within the `()` to further customize how the data is handled and displayed. For example, `bins` and `bindwidth` are parameters you can give to the geom_histogram() function to customize the calculations ggplot does under the hood.

Let's use this information to now plot a histograms of the penguin `body_mass_g` variable with different bin parameters:


``` r
ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram(binwidth=50)
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-8-1.png)<!-- -->

``` r
ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram(bins=10)
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-8-2.png)<!-- -->

### Mapping vs setting aesthetics

Different **geoms** have different visual properties (aesthetics) that can be assigned to variables. Here's a list of the most common properties. Underlined are the ones that are valid for this `geom_histogram()`:

-   [color]{.underline}: this changes the color of the line or points
-   [fill]{.underline}: if the shape is filled, this changes the fill color. Filled shapes are used in bar plots, box plots, and histograms. Points are generally not filled.
-   shape: if your geom is a point, this changes the shape of the point. (Some shapes are filled, some aren't)
-   size: this changes the size of the point or line
-   [linetype]{.underline}: If the geom has a line, including if it's an outline, this changes the type of line (dotted, dashed, etc)
-   [alpha]{.underline}: this changes the transparency of the geom

Let's change some of the mapping properties of the histogram plot we made by using these aesthetics inside the `geom_histogram()` function:


``` r
ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram(color = "black", fill = "blue", linetype="dashed", alpha=0.6)
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-9-1.png)<!-- -->

In the above code, we used aesthetic mappings to change the visual properties of all the histogram bars at once. This is called **setting** the aesthetic property. Another thing we can do is **mapping** the aesthetic property to a variable in the data. This is done by putting the aesthetic inside the `aes()` function. This is useful when you want to color the bars by a variable in the data, like the species of the penguin:


``` r
ggplot(penguins, aes(x = body_mass_g, fill = species)) +
  geom_histogram(color="black")
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-10-1.png)<!-- -->

In the above code, we have **mapped** the fill aesthetic to the species variable in the data. By mapping an aesthetic property to a variable, the bars are colored by that variable and ggplot automatically generates a legend that matches.

Also notice how we have **set** the color of the outline of all the bars to be black. This is because the color aesthetic is not placed inside the `aes()` function, so it applies to every piece of data. Here's what happens if you put `color="black"` inside the `aes()` function:


``` r
ggplot(penguins, aes(x = body_mass_g, fill = species, color = "black")) +
  geom_histogram()
```

```
## `stat_bin()` using `bins = 30`. Pick better value with `binwidth`.
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-11-1.png)<!-- -->

And here's what happens when I try to put `fill=species` outside of the `aes()` function.


``` r
ggplot(penguins, aes(x = body_mass_g)) +
  geom_histogram(color="black", fill=species)
```

```
## Error: object 'species' not found
```

R is throwing an error because it is only inside the `aes()` function that you can directly reference a variable in the data.

To sum, in this section, we learned that you can set an aesthetic property to be constant across all data by putting it outside the `aes()` function or you can map it to a variable by putting it inside. Later, we will learn that you can override the aesthetic by putting an `aes()` function inside the `geom` function.

### Inheriting aesthetics

But first, we'll see how we can add another geom layer to the plot.

In the below code, we will display data as a scatter plot using `geom_point()` layer. Since scatter plots require an x and y axis, in our `aes()` call we'll have to specify both. Let's compare the penguins' body mass with their bill lengths. We used `body_mass_g` and bill length is stored in the `bill_length_mm` column of our data. We will also add another geom layer, `geom_smooth()`, which is a function that will calculate and add a linear fit to the points.


``` r
ggplot(penguins, aes(x = body_mass_g, 
                     y = bill_length_mm, 
                     color=species)) +
  geom_point() +
  geom_smooth(method = "lm", se=FALSE) # add linear fit, without confidence interval
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-13-1.png)<!-- -->

You can see that the linear fit is done to each species separately. This is because geoms by default **inherit** the aesthetics (and the data) from the `ggplot()` function. This is a very useful feature of ggplot that allows you to easily add layers to your plot without having to specify the data and aesthetics again.

What happens when we put the `aes(color=species)` inside the `geom_point()` function?


``` r
ggplot(penguins, aes(x = body_mass_g, y = bill_length_mm)) +
  geom_point(aes(color=species)) +
  geom_smooth(method = "lm", se=FALSE)
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-14-1.png)<!-- -->

In the above figure, now the `geom_smooth()` function ONLY inherits the x and y aesthetic options and knows nothing about the species, which is why you only see a single linear fit across all the data. When you are layering multiple geoms together, you can more finely control how the aesthetics are mapped by putting them inside the `geom` function.

To sum up this section, we learned that you can layer geoms on the same graph to show different relationships in the data. Each geom can inherit the aesthetics from the `ggplot()` function, but you can also override these aesthetics by specifying them in the `geom` function.

Here's some vocabulary to tie it together:

| Term/Function | Definition/Description                                                                               |
|---------------------|---------------------------------------------------|
| tidy data     | Data where variables are in columns and observations are in rows. Easiest for plotting               |
| `ggplot()`    | Function that initializes a ggplot object                                                            |
| `aes()`       | Function that specifies the aesthetics of the plot                                                   |
| aesthetics    | Graphical properties governing how the data is displayed/mapped, e.g. x, y, color, fill, shape, etc. |
| `geom_*()`    | Function that specifies the type of plot to be drawn                                                 |
| layer         | A layer is a function that adds a new element to the plot, such as labels or new geoms               |
| `+`           | Operator that adds a new layer to a ggplot object                                                    |
| map/mapping   | Make an aesthetic property of a plot dependent on a variable in the data                             |
| set           | Make an aesthetic property of a plot constant                                                        |

## Customizing non-data aspects plots: lab(el)s, scales, and themes

We've now learned how to use the `aes()` function to control how are variables are represented in the plot. Each geom has a set of aesthetics that can be mapped to the data or set as constant across all the data in the plot. By default, the ggplot package decides everything else about the plot, such as the axis labels, the colors, the background color, the legend position and size, etc. However, you can customize all of these things. The tricky part is knowing what kind of function to use to customize each aspect of the plot.

Here is the big design principle behind ggplot:

> **A ggplot (the object) is composed of data elements and non-data elements, and the key to figuring out how to change something is identifying whether that thing depends on the data or not.**

Let's define some terms:

A **data element** is something that was drawn onto the plot that is directly based on the data. These include things we've already talked about like:

-   bars in a bar plot
-   points in a scatter plot
-   all the aesthetic mappings of the geoms (shape, color, etc)
    -   everything about them, including the labels, the values, the order

But it also includes more subtle things like:

-   the labels on the tick marks of x and y axes and their order
-   the location of the x and y tick marks
-   the exact icon that the legend uses
-   the content of the text of the labels in the legend

A **non-data element** is something that is not directly based on the data, but is still part of how the plot looks visually. These include things like:

-   the font, font size, color, etc of text labels
    -   (except when you're plotting text with `geom_label`/`geom_text`)
-   the background color of the plot panel
-   the grid marks in the plot panel
-   the position of the legend
-   whether a legend appears at all
-   the position of any of the axis labels (both ticks and titles)
-   whether the axis lines are drawn at all
-   the margins of the plot
-   so much more!

The reason why understanding the difference between data and non-data elements is important is because there are different sets of functions that control each of these things. We are not going to cover every set of functions that governs visual appearance in ggplot, but hopefully by understanding this concept, when you see new code "in the wild", you will be able to understand how that worked and then make it your own.

In this next section, we will go through the steps to recreate a more complex plot. There will be BONUS sections that I will skip, but are in the text for your own reference later to expand on the function we introduce.

Often, we have an idea in our minds about what we want the graph to look like. For example, let's pretend this is what we want our graph to look like:

### Example plot

![](R_ggplot_revised_files/palmer_penguins.png)

### Base plot

Right now, this is our code based on what we've learned so far about mapping and setting aesthetics and layering geoms. We know where to put the `color` aesthetic and where to put the `shape` aesthetic, and how to prevent the legend from `geom_smooth` from showing. From a data perspective, all the same information is there, but it just looks not so great.

So, since we want to experiment, we can save this plot to an object with the syntax `g <- ggplot()` . This creates an object called `g` in our environment that contains all the information to recreate this base plot. The nice thing is, as we will see, you can directly add layers with `+` to the plot object `g` as you experiment with changing the visual elements.


``` r
g <- ggplot(data=penguins, aes(x = bill_length_mm, 
                               y = bill_depth_mm, 
                               color = species)) + 
  geom_point(aes(shape = species)) +
  geom_smooth(method = "lm", se = FALSE, show.legend = F)
g
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-15-1.png)<!-- -->

### Base plot with labels

The first thing we want to do is to add a title, subtitle, x an y axis labels, and also a better legend title. All this can be accomplished with another layer called `labs()`. In the below code block, we are using our saved ggplot object called `g` from above so we don't have to type everything again to create the base plot. Using `g + blah()` allows us to add another layer without modifying the base plot.

Notice how we added a title to the `color` aesthetic and it separated out that aesthetic from the `shape` aesthetic! This is because now `shape` and `color` now have two different names, one derived from the data and one provided by the `labs()` function.


``` r
g + 
  labs(title = "Penguin bill dimensions",
       subtitle = "Bill length and depth for Adelie, Chinstrap and Gentoo Penguins at Palmer Station LTER",
       x = "Bill length (mm)",
       y = "Bill depth (mm)",
       color = "Penguin species")
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-16-1.png)<!-- -->

To fix this, we need to set both aesthetics to the same name. We could save this as our new base plot, but as we'll see later, the order of how we add layers matters, so we'll hold off for now.


``` r
g + 
  labs(title = "Penguin bill dimensions",
       subtitle = "Bill length and depth for Adelie, Chinstrap and Gentoo Penguins at Palmer Station LTER",
       x = "Bill length (mm)",
       y = "Bill depth (mm)",
       color = "Penguin species",
       shape = "Penguin species")
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-17-1.png)<!-- -->

### Adding color scale

Let's keep working from the base plot. The next major difference between our current plot and our ideal plot that we're going to tackle is the color, transparency, and the size of the shapes. All of these are aesthetic qualities, which mean it is about how the data are presented. So we'll need to modify the `geom` function and use a new type of function called a `scale` function. First let's modify the `geom_point` to change the size and transparency of the points.

Remember that due to inheritance, we will need to re-specify that we want the geom_point's `aes` to assign `shape=species`. Also we will be setting the size and transparency (aka **alpha**) for all points so it goes outside the `aes` .


``` r
g + 
  geom_point(aes(shape=species), size=3, alpha = 0.8)
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-18-1.png)<!-- -->

Now what about the difference in color? We can use a function of the class `scale_color_*`. The `scale_*_something` functions are a class of functions that customize how aesthetics are mapped. The word after scale is the aesthetic you want to customize and the third word is usually either `continuous/discrete/manual/brewer` depending on whether you are plotting a numerical or categorical variable or whether you want full control over everything. So you can have `scale_fill_manual()` to manually map the fill aesthetic, `scale_color_discrete()` and `scale_color_continuous()` to map discrete or continuous values from your variable onto a color scale, etc.

R has built-in color names and that we can input that to `scale_color_manual`. There are 657 built in color names in R. You can see a list of them using the `colors()` function, type `demo("colors")` for an interactive tour of all of them, or simply search for an image of all the colors online. For now, we will cheat and I will provide that the original plot was made with the colors "darkorange", "purple" and "cyan4". These can be entered in order to the `values` parameter of `scale_color_manual`.


``` r
g + 
  geom_point(aes(shape=species), size=3, alpha = 0.8) +
  scale_color_manual(values = c("darkorange", "purple", "cyan4"))
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-19-1.png)<!-- -->

BONUS: Read about pre-made color palettes

We can use `scale_color_brewer` to take advantage of pre-made discrete color palettes. To see all the options type `RColorBrewer::display.brewer.all()` in your console. For more information on how to generate custom palettes, use rgb values to specify colors, and more, see chapter 12 "Using Colors in Plots" in the [R Graphics Cookbook](https://r-graphics.org/CHAPTER-COLORS).


``` r
g + 
  geom_point(aes(shape=species), size=3, alpha = 0.8) +
  scale_color_brewer(palette = "Dark2")
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-20-1.png)<!-- -->

BONUS: Read for more things you can control with scales for aesthetics

The other things you can change in `scale_color_manual` is how each color is mapped to each discrete value and also how each discrete value is labeled. We can explicitly set key:value pairs inside this to control which penguin gets which color. The keys must be how they are stored in the data. But if how they are stored in the data is not what we want to display, like common name instead of scientific name, we can then label these penguins whatever we want using the `label` parameter.


``` r
g + 
  geom_point(aes(shape=species), size=3, alpha = 0.8) +
  scale_color_manual(values = c("Chinstrap"="darkorange", "Adelie"="purple", "Gentoo"="cyan4"), labels = c("Chinstrap"="P.antarcticus", "Gentoo"="P.papua", "Adelie"="P.adeliae"))
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-21-1.png)<!-- -->

### Adding X/Y axis scale

One of the other differences between what we have now and the example plot are the X and Y axis tick marks. You will notice that in the example plot, there are many tick marks on the Y axis and a few additional ones on the X axis as well. Is this element of the plot a data-driven visual element or a non-data element?

If you guessed data-driven, you are correct! The spacing (or, **scaling**) of X and Y axes is typically automatically decided by ggplot based on the distribution of your data. This is how you always end up with a plot that shows all your data and not a ton of empty space to either side.

The way we can customize the X and Y axis scaling is with the set of functions `scale_x/y_something`. The "something" can be a transformation, like `log10`, or `continuous()`/`discrete()`. We are plotting continuous variables on both axes so we will use `scale_x/y_continuous()`

The arguments for these functions include

-   name: another way to set the axis label

-   breaks: the positions where there will be tick marks and text labels

-   n.breaks: alternatively, tell ggplot how many breaks you want

-   labels: how you want to label the tick marks

-   limits: the min and max value of the axis

The below code demonstrates how to manually set the breaks and limits for the x axis to match the example plot. We use `seq()` to create a vector of numbers from 30 to 60 with a step size of 10. Those are the breaks - where the tick marks will be. We also make sure that the limits include those breaks, as the base plot had slightly narrower x limits.


``` r
g + 
  scale_x_continuous(breaks=seq(30,60,10), limits = c(30,60))
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-22-1.png)<!-- -->

In the code block below, we will use the `n.breaks` argument in `scale_y_continuous` to add the number of breaks we want without having to manually create them. Now our axes look just like the example!


``` r
g + 
  scale_x_continuous(breaks=seq(30,60,10), limits = c(30,60)) +
  scale_y_continuous(n.breaks = 10)
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-23-1.png)<!-- -->

BONUS: scaling the axes works for discrete values as well

There are many more options for the scale functions. You can even use them with discrete variables to change the order of the labels or the colors of the bars. Here's an example of how you can change the order of the species in the legend. In the below code, I reordered the bars and also used the `position` argument to move the x axis to the top of the plot.


``` r
ggplot(penguins, aes(x = species, fill=species)) +
  geom_bar()
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-24-1.png)<!-- -->

``` r
ggplot(penguins, aes(x = species, fill=species)) +
  geom_bar() +
  scale_x_discrete(limits = c("Chinstrap", "Gentoo", "Adelie"), position ="top")
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-24-2.png)<!-- -->

### Base plot with all data elements

In the last sections we learned how to use `labs()`, `scale_color_manual()` , and `scale_x/y_continuous()` to affect change on the visual elements of the plot that depend on data. Let's put those together and see how close we are to the example plot.


``` r
g + 
  geom_point(aes(shape = species),
             size = 3,
             alpha = 0.8) +
  scale_color_manual(values = c("darkorange","purple","cyan4")) +
  scale_x_continuous(breaks=seq(30,60,10), limits = c(30,60)) + 
  scale_y_continuous(n.breaks=10) + 
  labs(title = "Penguin bill dimensions",
       subtitle = "Bill length and depth for Adelie, Chinstrap and Gentoo Penguins at Palmer Station LTER",
       x = "Bill length (mm)",
       y = "Bill depth (mm)",
       color = "Penguin species",
       shape = "Penguin species")
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-25-1.png)<!-- -->

![](R_ggplot_revised_files/palmer_penguins.png)

### Theme

The remaining differences between this plot and our current plot are all due to the **non-data elements** of the plot. These include: the italicized font of the subtitle, the background color of the plot panel, the position and color of the legend. All these non-data elements can be edited using the `theme()` function.

Themes govern practically everything that isn't about how your data is presented, and it can be hyper-specific. For example, here is a diagram of the most common theme elements covering things you would never have thought could be customized. Changing an element of a plot generally entails first finding out what it is called in the theme. This is definitely **NOT** something you need to memorize.

![](https://isabella-b.com/blog/ggplot2-theme-elements-reference/ggplot2-theme-elements-reference-v2_hu8994090e1960a0a71878a3756da20076_580819_2000x2000_fit_lanczos_2.png)

In the below code, we've assembled all of our previous layers and added on the theme elements that need to be changed to create, finally, the look of the example plot. The adjustments made are:

-   place the legend inside the plot panel

-   adjust position of inside legend to the lower right

-   italicized the plot subtitle

-   changed the plot panel background color to "linen"

-   removed the default white legend background color (you'll see what this means if you remove this line)


``` r
g_final <- ggplot(data = penguins, 
       aes(x = bill_length_mm,
           y = bill_depth_mm,
           color = species)) +
  geom_point(aes(shape = species), 
             size = 3, 
             alpha = 0.8) +
  geom_smooth(method = "lm", 
              se = FALSE, 
              show.legend = FALSE) +
  scale_color_manual(values = c("darkorange","purple","cyan4")) +
  scale_x_continuous(breaks=seq(30,60,10), 
                     limits = c(30,60)) + 
  scale_y_continuous(n.breaks=10) + 
  labs(title = "Penguin bill dimensions",
       subtitle = "Bill length and depth for Adelie, Chinstrap and Gentoo Penguins at Palmer Station LTER",
       x = "Bill length (mm)",
       y = "Bill depth (mm)",
       color = "Penguin species",
       shape = "Penguin species") +
  theme(legend.position = c(.85,.15),
        plot.subtitle = element_text(face= "italic"),
        plot.subtitle.position = "plot",
        plot.title.position = "plot",
        panel.background = element_rect(fill="linen"),
        legend.background = element_blank())
g_final
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-26-1.png)<!-- -->

BONUS: Read about how you can change the look of the whole plot with just one line

ggplot has many built-in complete themes that overhaul plots to look differently. Here's a few of them. See how the same plot can look really differen by just picking a bundled theme.


``` r
g_final + theme_dark()
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-27-1.png)<!-- -->

``` r
g_final + theme_minimal()
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-27-2.png)<!-- -->

``` r
g_final + theme_void()
```

```
## `geom_smooth()` using formula = 'y ~ x'
```

![](R_ggplot_revised_files/figure-html/unnamed-chunk-27-3.png)<!-- -->

### Plots that ggplot doesn't do well

Despite all the things ggplot can do, there are some plots that it doesn't do well. Here's a list of plot types you might want to make but would be served by using a different package:

-   heatmaps (base R, ggheatmap, pheatmap)
-   venn diagrams (VennDiagram, ggvenn)
-   dendrograms (ggtree)
-   graphs (igraph, ggraph, tidygraph)

# Where to read more

The ggplot package has a lot more than just histograms, scatter plots, and linear fits. However, an exhaustive tour of the different geoms is a bit outside the scope of this workshop. Instead, we'll go over how to read the documentation of ggplot to figure out how to make the plot you want.

The first place I like to look is on the ggplot cheatsheet, created by Posit. To see the cheatsheet, click [this link](https://rstudio.github.io/cheatsheets/html/data-visualization.html) and then click "Download pdf" on the right side. Here you can visually pick out the plot type you want and find the corresponding geom function, as well as a list of the aesthetics that can be mapped to variables in the data.

Because of the way ggplot functions are standardized, as long as you know the geom, you can follow the same pattern to create the plot you want. The syntax is:

``` r
ggplot(data, aes(x=variable1, ...)) + 
  geom_*()
```

From there, you can go to the documentation page of that geom or look up examples of how to use it.
