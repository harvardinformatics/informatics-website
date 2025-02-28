library(tidyverse)
library(hms)
library(ggbeeswarm)
library(cowplot)

# library(tidyplots)

this.dir = dirname(parent.frame(2)$ofile)
setwd(this.dir)
source("lib/design.r")
# Set the working directory to be the directory of the script and source
# the design functions for the plots. Only works when sourcing the script.

saveplots = T

####################

turtle_file = "../data/tutorials/turtle-jobres.csv"
turtle_data = read.csv(turtle_file, header=T, comment.char="#")
# Read in the turtle data

turtle_data = turtle_data %>%
  mutate(runtime.seconds = as.numeric(as_hms(ElapsedTime)),
         runtime.minutes = runtime.seconds / 60)
# Convert time to a numeric in minutes

####################

size_p = ggplot(turtle_data, aes(x="", y=Genome.size.mb)) +
  geom_quasirandom(size=1, width=0.25, alpha=0.60, color=corecol(numcol=1)) +
  geom_boxplot(outlier.shape=NA, alpha=0.15, width=0.5, color="#666666", size=0.25) +
  xlab("") +
  ylab("Genome size (Mb)") +
  bartheme_web() +
  theme(axis.ticks.y=element_blank(),
        axis.line.y=element_blank()) +
  coord_flip()

print(size_p)
if(saveplots){
  ggsave("../docs/resources/img/turtles-genome-sizes.png", size_p, width=600, height=300, units="px")
}

####################

lines_data <- data.frame(
  Rule = c("Mask", "Blast", "Align"),
  runtime_y = c(720, 720, 60),     # Hypothetical y-intercepts for the lines
  maxmem_y = c(450, 400, 100),
  x = c(0.75, 1.75, 2.75),   # Start slightly left of each category center
  xend = c(1.25, 2.25, 3.25), # End slightly right of each category center
  label = factor("Requested Amount")  # Factor for legend
)

####################

runtime_p = turtle_data %>%
  filter(Rule %in% c("mask", "blast", "align")) %>%
  mutate(Rule = str_to_title(Rule)) %>%
  mutate(Rule = factor(Rule, levels = c("Mask", "Blast", "Align"))) %>%
  ggplot(aes(x=Rule, y=runtime.minutes)) +
    geom_quasirandom(size = 0.75, width = 0.25, alpha = 0.40, color = corecol(numcol = 1, offset = 1)) +
    geom_boxplot(outlier.shape = NA, alpha = 0.15, width = 0.5, color = "#666666", size=0.25) +
    # geom_segment(data = lines_data, 
    #              aes(x = x, xend = xend, y = runtime_y, yend = runtime_y, color = label), 
    #              linetype = "dashed", size = 0.25) +
    # scale_color_manual(name = "Legend", 
    #                    values = "red",
    #                    labels = "Requested Amount") +
    xlab("Cactus step") +
    ylab("Run time (minutes)") +
    bartheme_web() #+
    # theme(    legend.position = "bottom",
    #           legend.margin = margin(t = -10)          # Adjust top margin to bring the legend closer
    #           #plot.margin = margin(t = 10, r = 5, b = 2, l = 5)  # Adjust plot margins as needed
    # )

print(runtime_p)
if(saveplots){
  ggsave("../docs/resources/img/turtles-cactus-runtime.png", runtime_p, width=700, height=450, units="px")
}
              
####################
              
maxmem_p = turtle_data %>%
  filter(Rule %in% c("mask", "blast", "align")) %>%
  mutate(Rule = str_to_title(Rule)) %>%
  mutate(Rule = factor(Rule, levels = c("Mask", "Blast", "Align"))) %>%
  ggplot(aes(x=Rule, y=MaxMemory.GB.)) +
    geom_quasirandom(size = 0.75, width = 0.25, alpha = 0.40, color = corecol(numcol = 1, offset = 2)) +
    geom_boxplot(outlier.shape = NA, alpha = 0.15, width = 0.5, color = "#666666", size=0.25) +
    # geom_segment(data = lines_data, 
    #              aes(x = x, xend = xend, y = maxmem_y, yend = maxmem_y, color = label), 
    #              linetype = "dashed", size = 0.25) +
    # scale_color_manual(name = "Legend", 
    #                    values = "red",
    #                    labels = "Requested Amount") +  
    xlab("Cactus step") +
    ylab("Max mem usage (GB)") +
    bartheme_web()
    # theme(    legend.position = "bottom",
    #           legend.margin = margin(t = -10)          # Adjust top margin to bring the legend closer
    #           #plot.margin = margin(t = 10, r = 5, b = 2, l = 5)  # Adjust plot margins as needed
    # )

print(maxmem_p)
if(saveplots){
  ggsave("../docs/resources/img/turtles-cactus-maxmem.png", maxmem_p, width=700, height=450, units="px")
}

####################
