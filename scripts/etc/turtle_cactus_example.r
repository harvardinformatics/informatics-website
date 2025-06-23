library(tidyverse)
library(ggbeeswarm)
library(cowplot)

# library(tidyplots)

this.dir = dirname(parent.frame(2)$ofile)
setwd(this.dir)
source("lib/design.r")
# Set the working directory to be the directory of the script and source
# the design functions for the plots. Only works when sourcing the script.

saveplots = FALSE

turtle_file_url = "../data/tutorials/turtles-include-cactus.csv"
turtle_data = read.csv(turtle_file_url, header=T, comment.char="#")
# Read in the turtle data
# From https://github.com/gwct/turtle-genomics

turtle_data$mask.cputime = turtle_data$mask.cputime / 60 / 60
turtle_data$mask.runtime = turtle_data$mask.runtime / 60 / 60
turtle_data$mask.maxmem = substr(turtle_data$mask.maxmem,1,nchar(turtle_data$mask.maxmem)-1)
turtle_data$mask.maxmem= as.numeric(turtle_data$mask.maxmem)
turtle_data$mask.maxmem = turtle_data$mask.maxmem / 1024 / 1024

turtle_data$blast.cputime = turtle_data$blast.cputime / 60 / 60
turtle_data$blast.runtime = turtle_data$blast.runtime / 60 / 60
turtle_data$blast.maxmem = substr(turtle_data$blast.maxmem,1,nchar(turtle_data$blast.maxmem)-1)
turtle_data$blast.maxmem= as.numeric(turtle_data$blast.maxmem)
turtle_data$blast.maxmem = turtle_data$blast.maxmem / 1024 / 1024

turtle_data$align.cputime = turtle_data$align.cputime / 60 / 60
turtle_data$align.runtime = turtle_data$align.runtime / 60 / 60
turtle_data$align.maxmem = substr(turtle_data$align.maxmem,1,nchar(turtle_data$align.maxmem)-1)
turtle_data$align.maxmem= as.numeric(turtle_data$align.maxmem)
turtle_data$align.maxmem = turtle_data$align.maxmem / 1024 / 1024

turtle_data$convert.cputime = turtle_data$convert.cputime / 60 / 60
turtle_data$convert.runtime = turtle_data$convert.runtime / 60 / 60
turtle_data$convert.maxmem = substr(turtle_data$convert.maxmem,1,nchar(turtle_data$convert.maxmem)-1)
turtle_data$convert.maxmem= as.numeric(turtle_data$convert.maxmem)
turtle_data$convert.maxmem = turtle_data$convert.maxmem / 1024 / 1024
# Unit conversions

####################

turtle_data_runtime = turtle_data %>% select(name, mask.runtime, blast.runtime, align.runtime)
turtle_data_maxmem = turtle_data %>% select(name, mask.maxmem, blast.maxmem, align.maxmem)
# Select data for resources of interest

#print(paste("Avg. genome size:", mean(turtle_data$Size..Mb., na.rm=T)))

size_p = ggplot(data=turtle_data, aes(x="", y=Size..Mb.)) +
  geom_quasirandom(size=1.5, width=0.25, alpha=0.60, color=corecol(numcol=1)) +
  geom_boxplot(outlier.shape=NA, alpha=0.15, width=0.5, color="#666666") +
  xlab("") +
  ylab("Genome size (Mb)") +
  bartheme_web() +
  theme(axis.ticks.x=element_blank())
print(size_p)
# Display the figure

# turtle_data |>
#   tidyplot(x=1, y=Size..Mb.) |>
#   add_boxplot() |>
#   add_data_points_beeswarm() |>
#   adjust_y_axis_title("Genome size (Mb)")

####################

turtle_res_long <- turtle_data %>%
  select(cactus.node, ends_with(c("runtime", "maxmem"))) %>% # Select only the relevant columns for transformation
  pivot_longer(
    cols = ends_with(c("runtime", "maxmem")),
    names_to = c("step", ".value"),
    names_sep = "\\."
  ) %>% # Pivot data to longer format
  filter(step != "convert") %>% # Remove the convert step
  mutate(step = str_to_title(step)) %>% # Capitalize the first letter of the step names
  mutate(step = factor(step, levels = c("Mask", "Blast", "Align"))) # Ensure the factor levels are set correctly if needed

# turtle_res_long |>
#   tidyplot(x=step, y=runtime, color=step) |>
#   add_boxplot() |>
#   add_data_points_beeswarm() |>
#   remove_legend() |>
#   adjust_x_axis_title("") |>
#   adjust_y_axis_title("Runtime (hours)")
  
time_p = ggplot(data = turtle_res_long, aes(x = step, y = runtime, group = step)) +
  geom_quasirandom(size = 1.5, width = 0.25, alpha = 0.40, color = corecol(numcol = 1, offset = 1)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.15, width = 0.5, color = "#666666") +
  xlab("Cactus step") +
  ylab("Run time (hours)") +
  bartheme_web()
print(time_p)
# Display the figure

full_time_p = plot_grid(size_p, time_p, ncol=2, rel_widths=c(0.4,1))
title_grob <- ggdraw() +
  draw_label("Cactus run time on 22 turtle genomes", size=10, fontface = 'bold', x = 0.5, hjust = 0.5)
final_time_p = plot_grid(title_grob, full_time_p, ncol=1, rel_heights = c(0.1, 1) )

print(final_time_p)
if(saveplots){
  ggsave("../docs/resources/img/cactus-runtime-turtles.png", final_time_p, width=7, height=3, units="in")
}

####################

mem_p = ggplot(data = turtle_res_long, aes(x = step, y = maxmem, group = step)) +
  geom_quasirandom(size = 1.5, width = 0.25, alpha = 0.40, color = corecol(numcol = 1, offset = 2)) +
  geom_boxplot(outlier.shape = NA, alpha = 0.15, width = 0.5, color = "#666666") +
  xlab("Cactus step") +
  ylab("Max mem usage (GB)") +
  bartheme_web()
print(mem_p)
# Display the figure

full_mem_p = plot_grid(size_p, mem_p, ncol=2, rel_widths=c(0.4,1))
title_grob <- ggdraw() +
  draw_label("Cactus max memory usage on 22 turtle genomes", size=10, fontface = 'bold', x = 0.5, hjust = 0.5)
final_mem_p = plot_grid(title_grob, full_mem_p, ncol=1, rel_heights = c(0.1, 1) )

print(final_mem_p)
if(saveplots){
  ggsave("../docs/resources/img/cactus-maxmem-turtles.png", final_mem_p, width=7, height=3, units="in")
}
