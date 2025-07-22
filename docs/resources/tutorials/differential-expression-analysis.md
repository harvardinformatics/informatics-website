---
title: "[Tutorial] Differential analysis of bulk RNA-seq data"
description: "A page explaining how to perform differential expression analysis of bulk RNA-seq data using limma."
authors: 
    - Adam Freedman
---

# Differential expression analysis of bulk RNA-seq data

{{ author_row(page) }}

Bulk RNA-seq involves generating estimates of gene expression for samples consisting of large pools of cells, for example a section of tissue, an aliquot of blood, or a collection of cells of particular interest, such as those obtained via fluorescence-activated cell sorting (FACS). The two primary pillars of bulk RNA-seq analysis are the estimation of abundance, at either the gene or isoform level (or both), and statistical analysis to identify genes or isoforms that show different levels of expression between a set of conditions or treatments of interest. This tutorial provides a brief review of expression quantification, but mostly focuses on how to perform tests for differential expression with *limma*. See [Ritchie et al. 2015](https://academic.oup.com/nar/article/43/7/e47/2414268) for more details. *Limma* is built on a linear-modeling framework and is available as a [*Bioconductor* package](https://bioconductor.org/packages/release/bioc/html/limma.html) in R.   

## Quantifying expression: a brief review
### Alignment-based
Quantification of gene (or transcript) abundance requires determining the transcript of origin for the RNA-seq reads in a fastq file for a given sample, and then counting the number of reads that are assigned to a transcipt, and summing those counts over constituent transcripts of a gene to obtain gene-level estimates of expression. A long-standing approach for quantification begins with formally aligning sequencing reads to either a genome or a set of transcripts derived from a genome annotation. In both of these instances, a [*sam*](https://samtools.github.io/hts-specs/SAMv1.pdf) or a binary versions (bam format) output file is produced that describes where reads aligned to, assigns a score to each alignment, etc. Alignment directly to a genome requires using a splice-aware aligner to accommodate alignment gaps due to introns, with [STAR](https://github.com/alexdobin/STAR) being the most popular of these, while tools like [bowtie2](https://github.com/BenLangmead/bowtie2) can be used to map reads to a set of transcript sequences. Once bam files are generated, these can be supplied to tools like [RSEM](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-12-323) to generate expression estimates.

### Pseudo-alignment
A more recent set of approaches uses something called "pseudo-alignment", where formal sequence alignment is not undertaken, but instead uses substring matching to probabilistically determines locus of origin without obtaining base-level precision of where any given read came from. Tools such as [Salmon](https://github.com/COMBINE-lab/salmon) and [kallisto](https://github.com/pachterlab/kallisto) employ this approach. The pseudo-alignment approach is much quicker, and in addition both tools output expression estimates at the same time as figuring out where reads come from, saving end users from having to perform quantification separately.  

### The middle path
Salmon has the ability to take bam files as input, and use sequence alignments to make probabilistic assignments of reads to loci (and count those assignments). For this "alignment-based" mode, Salmon requires that reads be mapped to a set of transcript sequences rather than splice-mapped to the genome. Because bam files contain a lot of information that are useful for performing quality checks on your data, we believe it is worthwhile to perform sequence alignment. Our specific recommendation follows immediately below.

## Quantifying expression best practice
In order to obtain a comprehensive set of quality control metrics on our fastq files, while also obtaining gene and isoform-level count matrices from Salmon's (isoform-level) quantification machinery, we use nf-core's RNA-seqe pipeline, found [here](https://nf-co.re/rnaseq/3.19.0). [nf-core] is a collection of *Nextflow* workflows for automating analyses of high-dimensional biological data. The RNA-seq workflow has a variety of option to choose from, but we specifically use the "STAR-salmon" option. This option performs spliced alignment to the genome with *STAR*, projects those alignments onto the transcriptome, and performs alignment-based quantification from the projected alignments with Salmon. The workflow requires as input a specifically formatted sample sheet, a genome fasta, and either a gtf or a gff annotation file.

### nf-core sample sheet format
The sample sheet has to be in comma-separated format, with specific column headers, e.g.:
```
sample,fastq_1,fastq_2,strandedness
sample1,fastq/sample1_R1_fastq.gz,fastq/sample1_R2_fastq.gz,auto
sample2,fastq/sample2_R1_fastq.gz,fastq/sample2_R2_fastq.gz,auto
```

While strand configuration can be manually specified, we prefer to use Salmon's auto-detect function, which will also account for cases when the set of samples include data where the strandedness is unknown (e.g. SRA accessions without detailed metadata), mistakenly specified, or where issues with reagents led to a strand-specific kit producing a library without strand specificity. This workflow is only appropriate for paired-end data. Locations of R1 and R2 can be paths relative to the location where the workflow is being launched or absolute paths. Fastq files should be gzipped. In cases where a sample id occurs in more than one row of the table, the workflow assumes these are separate sequencing runs of the same sample and counts estimation will be aggregated across rows with the same value for sample.

### the gtf/gff annotation file
The nf-core ecosystem was built to work optimally with annotation files from Ensembl. In most cases, it will work with NCBI annotation files. However, for both Ensembl and NCBI the gtf versions of the annotation files are preferred. For NCBI, the gff version will occasionally fail because there are subset of (typically manually curated) features for which there isn't a value for *gene_id* in the attributes (9th) column of the file. In addition, warnings, or in some cases job failure will occur if there is a value for *gene_biotype*, so we use an additional argument in our workflow that skips a biotype-based expression QC metric.

### executing the nf-core RNA-seq workflow
An example execution script to launch the workflow, where the parent job for the workflow is deployed on a cluster that uses the SLURM job scheduler is as follows:

```bash
#SBATCH -J nfcorerna
#SBATCH -N 1
#SBATCH -c 1
#SBATCH -t 23:00:00  # time in hours, minutes and seconds           
#SBATCH -p         # add partition name here 
#SBATCH --mem=12000              
#SBATCH -e nf-core_star_salmon_%A.err
#SBATCH -o nf-core_star_salmon_%A.out
module load python
mamba activate nfcore-rnaseq

nextflow run nf-core/rnaseq \
    --input nfcore_samplesheet.csv \
    --outdir $(pwd)/star_salmon \
    --skip_biotype_qc \
    --gtf genome/mygenome.gtf \
    --fasta genome/mygenome.fna.gz \
    --aligner star_salmon \
    -profile singularity \
    --save_reference \
    -c rnaseq_cluster.config
```

* Launching nfcore/rnaseq automatically downloads the workflow from the GitHub repository, and installs all dependencies
* The genome needs to be gzipped
* The annotation file should be uncompressed. If you opt to use a gff file then, `--gtf` should be changed to `--gff`
* A config file should be provided that specifies compute resources for various workflow child processes (see below)

#### The config file
A config file needs to be supplied that specifies the type of computational resources that get allocated for jobs that are labelled in the workflow by their memory requirements. The config file we have successfully deployed on Harvard's Cannon HPC cluster can be found [here](https://github.com/nf-core/rnaseq/blob/master/conf/base.config). By default, this config will have jobs run locally on the computer/node where the job is launched. To use HPC resources, you need to specify a line at the beginning of the *process* block indicating the executor, and an additional line below with partition names to use. In the case of the Cannon cluster, on which jobs are scheduled by SLURM, and where we use the partitions named "sapphire" and "shared", we modify the beginning of the config file to look like this:

```bash
process {
    executor = 'slurm'
    // TODO nf-core: Check the defaults for all processes
    cpus   = { 1      * task.attempt }
    memory = { 6.GB   * task.attempt }
    time   = { 4.h    * task.attempt }
    queue = 'sapphire,shared'
``` 

where the order of queues indicates the order of prioritization for partition selection.

## Differential expression analysis: a worked example
This tutorial performs differential expression analysis with R, and for the purposes of making debugging and visualization/plotting easier, we recommend using [RStudio], and interactive environment that can downloaded from [here](https://posit.co/download/rstudio-desktop/). It will require that a version of R is already installed on your computer. If it isn't you can obtaine R from [https://cran.r-project.org/]. If all of this seems very new to you, it may be tricky to get an understanding for what the R code is doing. If that is the case, we recommend attending an Informatics Group R workshop, the next one of which will be offered in the Fall of 2025. Assuming R isn't entirely foreign to you, we will assume that you will be loading the commands explained below into a script (or an R markdown file), the lines of which you will execute in sequence. 


If you want to reproduce the workflow explained below, the R markdown (Rmd) file for it can be found [here](data/de_tutorial_exampleworkflow_2025.07.22.Rmd). The sample sheet that relates sample IDs to experimental conditions can be found at [sample_sheet](data/dme_elev_samples.tsv), and the gene-level count matrix can be found at [count_matrix](data/salmon.merged.gene_counts.tsv).

### Example data
Our sample data comprises 12 paired-end RNA-seq libraries for whole body samples of *Drosophila melanogaster* from two geographic regions (Panama and Maine), with two temperature treatments ("low" ane "high") for each region, featuring three biological replicates for each region x treatment combination. Previously, these data were used to look for parallel gene expression patterns between high and low latitude populations (Zhao et al, 2015, *PLoS Genetics*). Fastq files were downloaded from NCBI's Short Read Archive, and were processed using the *nf-core/rnaseq* workflow. To demonstrate a differential expression analysis using limma, we use the gene-level tab-separated count table *salmon.merged.gene_counts.tsv*. The column header includes "gene_id" and	"gene_name" for the first two columns, and the sample names from the sample sheet for the remaining column labels. In other words, each row consists of a gene id, and putative gene symbol for that gene, and the estimated counts for each of the samples. For a differential expression analysis to be performed, one needs to know the experimental condition for each of the samples. The sample sheet supplied to *nf-core/rnaseq* does not include this information, so we need to generate a sample sheet that can be supplied to *limma*. Our example sample sheet is called *dme_elev_samples.tsv*, and looks like this:

```bash
sample population temp
SRR1576457 maine low
SRR1576458 maine low
SRR1576459 maine low
SRR1576460 maine high
SRR1576461 maine high
SRR1576462 maine high
SRR1576463 panama low
SRR1576464 panama low
SRR1576465 panama low
SRR1576514 panama high
SRR1576515 panama high
SRR1576516 panama high
```

### 1. Expression analysis in R: preliminaries
The differential expression analysis we demonstrate requires a number of R packages, which can be installed as follows:

```
install.packages("tidyverse")

if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")

BiocManager::install("limma","edgeR")
```

*Tidyverse* is a data science packages that facilitates the manipulation of tabular data, and plotting visualizations. *edgeR* and *limma* are bioinformatics packages for analyzing bulk RNA-seq data.

### 2. Load gene-level abundance data
The first two columns of *salmon.merged.gene_counts.tsv* are "gene_id", the original gene id in the annotation, and "gene_name", the gene symbol. There may be cases in which a gene symbol is not unique among gene ids, such that it is useful to concatenate these two columns into a new label, which we do here. To manipulate the data into a matrix format that limma expects, we also need to remove the id and name information from the data table, and set the new concatenated label as row names. We do basic table manipulation by loading the table as a tibble via tidyverse, but then, since tidyverse doesn't accomodate row names, convert back to a data frame.

```bash
expression_data <-read_table("salmon.merged.gene_counts.tsv") %>%
                  mutate(gene_id_symbol=paste(gene_id,gene_name,sep="_")) %>%
                  select(!c(gene_id,gene_name)) %>%
                  relocate(gene_id_symbol)

new_ids=expression_data$gene_id_symbol
expression_data <- expression_data %>% select(!c(gene_id_symbol))
expression_data <-as.data.frame(expression_data)
row.names(expression_data)=new_ids

```

### 3. Load sample information
We not only load the sample info, but also create a new variable, *pop_temp*, that is the concatenation of the two categorical variables. We will use this concatenated variable to filter out lowly expressed genes, to insure that retained genes have sufficient counts for performing data analysis across samples consisting of each combination of temperature and population.

```bash
sample_info <- read.table("expression_data/dme_elev_samples.tsv",header = TRUE, stringsAsFactors=FALSE)
sample_info$pop_temp<-paste(sample_info$population,sample_info$temp,sep="_")
```

### 4. Create Digital Gene Expression (DGE) object
*Limma* and *edgeR* store and analyze bulk RNA-seq data in a digital gene expression object. Thus, we need to load the count data into one of these data structures, which contains both the expression matrix and information on individual samples with respect to their experimental condition(s) as obtained from the sample sheet.

```bash
DGE=DGEList(expression_data,samples=sample_info$sample,group=c(sample_info$sample_info$pop_temp))
```

### 5. Filtering out lowly expressed genes
A number of transcripts/genes will be not expressed at all in any sample, or may only be expressed in a small number of samples. In the latter case, testing for differential expression is noisy and under-powered. 

```bash
keep.exprs <- filterByExpr(DGE, group=DGE$samples$group)
DGE <- DGE[keep.exprs,, keep.lib.sizes=FALSE]
```

### 6. TMM normalization
The next step is conducting normalization of the counts across samples so that library size differences and the effects of genes that are highly expressed and sample specific are accounted for. Regarding the latter, we want to avoid having a few genes take up expression sequencing "real estate" given the overall number of reads generated by a sample, such that it reduces the reads in other transcripts in a way that would lead to false positive DE. To do this, we use the trimmed mean of M-values (TMM)  of Robinson and Oshlack (2010) available in edgeR. Note, one can use other normalization schemes, and I have seen some evidence that conditional quantile normalizartion (CQN) mignt be worth considering as an alternative.

```bash
DGE=calcNormFactors(DGE,method =c("TMM"))
```

### 7. Examine data for outliers
We do this to make sure there are no outliers with respect to a particular experimental variable, suggesting a potential issue with an RNA-seq library, and to also check for sample swaps. This can be done with a multidimensional scaling (MDS) plot using the top 500 highest expressed genes. 

We can color-code samples by level of the temperature factor:

```bash
tempvals<-sample_info$temp
plotMDS(DGE,top=500,col=ifelse(tempvals=="low","blue","red"),gene.selection="common")
```
<center>
    <img src="../../../../img/tutorials/de_temp_mds.png" alt="MDS plot on expression data: temperature" width="75%" />
</center>

Or by the levels of the population factor:

```bash
popvals<-sample_info$population
plotMDS(DGE,top=500,col=ifelse(popvals=="maine","darkgreen","dodgerblue"),gene.selection="common")
```
<center>
  <img src="../../../../img/tutorials/de_pop_mds.png" alt="MDS plot on expression data: population" width="75%" />
</center>

As expected, there is clear separation between temeprature regimes and geographic locations, but no outliers indicating bad samples or potential label swaps.

### 8. Create design matrix
At the heart of linear modeling are design matrices that specify boolean variables for the intercept, and additional factors, and limma requires such a matrix for performing differential expression analysis. Our first analysis is going to focus on a one-factor model, in which we ignore geography and look at the effects of low and high temperature treatments. We make a design matrix for this analysis as follows:

```bash
design_temp=model.matrix(~temp, data=sample_info)
design_temp
```

### 9a. Running limma
After creating the design matrix object, the standard approach is to next run limma voom on the DGE object, e.g.:
```{r,echo=TRUE,eval=FALSE}
v <- voom(DGE, design=design_temp, plot=TRUE)
```
**However** ... while this works fine under an ideal scenario, it becomes a problem if there is variation in sample quality, or more generally, there is some indication that a subset of samples appear as outliers via MDS, PCA, etc. Particularly for RNA-seq experiments where researchers may only have a few repicates per sample, discarding outlier samples is not feasible because it may lead to few if any biological replicates for some subset of treatments. 

A better solution to this problem is to apply weights to samples such that outlier samples are down-weighted during differential expression calculations. Limma voom does this by calculating "empirical quality weights" for each sample. Note that we don't specify a normalization method becaues the data have already been normalized with TMM.

### 9b. Run limma voom with sample quality weights

```bash
vwts <- voomWithQualityWeights(DGE, design=design_temp,normalize.method="none", plot=TRUE) 
```
Most bulk RNA-seq differential expression analysis packages need to fit a mean-variance relationship--which is used to adjust estimated variances-- and the *voomWithQualityWeights* command generates a plot of this relationship as well as a bar plot of the weights assigned to each sample. 

*Note:** we have already applied TMM normalization, thus can set the normalization argument to none. This above command will also generate a plot with two panels showing the mean-variance relationship fit on the left, and a barplot of weights assigned to individual samples.

### 10. Run the linear model fitting procedure 1st step

```bash
fit=lmFit(vwts,design_temp)
``` 

### 11. Then apply the empirical bayes procedure:
```bash
fit=eBayes(fit,robust=TRUE)
```

We use the robust=TRUE setting to leverage the quality weights such that the analysis is robust to outliers.

### 12. Get summary table
One can then get a quick and dirty summary of how many genes are differentially expressed, setting the FDR threshold,where the "fdr" and "BH" methods are synonymous for Benjamini Hochberg adjusted p-values.

```bash
summary(decideTests(fit,adjust.method="fdr",p.value = 0.05))

(Intercept) templow
Down           250    1589
NotSig         511    9990
Up           12546    1728

```


One piece of important info is the factor relative to which logfold change is being calculated, i.e. low will be the numerator for logfold change calculations.

Overall, (1589+1728)/13307 or ~ 24.9% of genes are differentially expressed as a function of temperature treatment, without considering the effect of population.

### 13. Explore top 10 DE genes (ordered by p-value):

```bash
topTable(fit, adjust="BH",resort.by="P")

                               logFC  AveExpr         t      P.Value    adj.P.Val        B
FBgn0038819_Cpr92F          2.473527 6.201774  24.28881 1.306910e-13 1.739105e-09 21.29258
FBgn0028544_Vajk3           1.675184 4.029281  21.90298 6.069753e-13 3.524528e-09 19.66813
FBgn0267681_lncRNA:CR46017 -3.974938 1.044005 -21.50807 7.945880e-13 3.524528e-09 16.80878
FBgn0031940_CG7214          2.198970 7.945664  20.75054 1.349821e-12 4.490516e-09 19.14847
FBgn0038702_CG3739         -2.869172 6.514652 -20.49734 4.414988e-12 1.175005e-08 18.01975
FBgn0014454_Acp1            2.231834 7.638125  17.79441 2.089853e-11 3.997808e-08 16.54909

```
There are several columns in the output:
* the gene name (the row name)
* log-fold change
* t the t-statistic for the underlying t-test
* *P.value*, the raw P-value
* *adj.P.Val*, the Benjamini-Hochberg FDR-adjusted p-value, aka a q value
* *B* is the B-statistic, i.e. the log-odds that the gene is differentially expressed.



### 14. Create full table
The full table will be useful for many purposes, such as creating custom MA or volcano plots with color-coding and symbols to meet your needs. **NOTE:** we must explicitly specify the coefficient for the factor of interest. In this case, as revealed in the summary table above, it is *templow*.

```bash
all_genes<-topTable(fit, adjust="BH",coef="templow", p.value=1, number=Inf ,resort.by="P")
```

where:
coeff = the coefficient or contrast you want to extract  
number = the max number of genes to list  
adjust = the P value adjustment method  
resort.by determines what criteria with which to sort the table  


## DE analysis: a more complicated, 2-factor design
Extending limma to analyze more complex designs, such as when considering two factors, temperature and population, is relatively straightforward. A key part is to specify the design matrix properly. For the 2-factor design, one would do this as follows.

### 15. build design matrix for 2-factor model

```bash
population <- factor(sample_info$population,levels=c("maine","panama"))
temperature <- factor(sample_info$temp, levels=c("high","low"))
design_2factor<- model.matrix(~population+temperature)
design_2factor
```

Then, you would proceed with DE analysis in a similar fashion as with the single factor experiment described above. Notice that we have specified the levels of temperature such that low is second, which results in "templow" being the dummy variable with which to fit the coefficient for temperature. 

### 16. run voom with quality weights with 2-factor design matrix

```bash
vwts_2factor <- voomWithQualityWeights(DGE, design=design_2factor,normalize.method="none", plot=TRUE)
fit_2factor=lmFit(vwts_2factor,design_2factor)
fit_2factor=eBayes(fit_2factor,robust=TRUE)
summary(decideTests(fit_2factor,adjust.method="fdr",p.value = 0.05))

(Intercept) populationpanama temperaturelow
Down           249              765           2259
NotSig         565            11625           8646
Up           12493              917           2402
```

There are now (2259+2402)/13307 or ~ 36.4% of genes are differentially expressed as a function of temperature after partitioning variation among temperature and population-level effects. In essence, accounting for population-level variation provided greater power in detecting the effects of temperature, as in the above 1-factor test, only 24.9% of genes were differentially expressed with respect to temperature.

### 17. Get full results table
As before, we can get the entire table (including those that do not show significant DE). **NOTE:** when we fit models with limma with a multi-factor design there are now two possible coefficients to select. Because we are interested in the effects of temperature, we specify *temperaturelow*. If we wanted to look at genes with differential regulation with respect to population, we would have to specify *populationpanama*.

```bash
all_genes<-topTable(fit_2factor, adjust="BH",coef="temperaturelow", p.value=1, number=Inf ,resort.by="P")
all_genes$geneid<-row.names(all_genes)
```


---

<!-- --------------------------------- -->
<!-- Page specfic CSS -->

<style>
    /* ----- */
    /* Section headers */
    h2 {
        text-align: center !important;
        border-bottom: 2px solid #333333 !important;
        border-top: 2px solid #333333 !important;
        font-weight: 500 !important;
    }
    
    /* ----- */
    /* For the admonitions, so they have an entry in the toc that doesn't show up on the page */
    details > h5 {
        font-size: 0.01em !important;       /* almost invisible but still present! */
        color: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* ----- */
    /* Hide all 2nd-level navs */
    .md-nav--secondary .md-nav__item .md-nav {
        display: none !important;
    }

    /* Show when parent has .expanded class, which is added by js/collapse_toc.js */
    .md-nav--secondary .md-nav__item.expanded > .md-nav {
        display: block !important;
    }    
</style>
