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

### Example data
Our sample data comprises 12 paired-end RNA-seq libraries for whole body samples of *Drosophila melanogaster* from two geographic regions (Panama and Maine), with two temperature treatments ("low" ane "high") for each region, featuring three biological replicates for each region x treatment combination. Previously, these data were used to look for parallel gene expression patterns between high and low latitude populations (Zhao et al, 2015, *PLoS Genetics*). Fastq files were downloaded from NCBI's Short Read Archive, and were processed using the *nf-core/rnaseq* workflow. To demonstrate a differential expression analysis using limma, we use the gene-level tab-separated count table *salmon.merged.gene_counts.tsv*. The column header includes "gene_id" and	"gene_name" for the first two columns, and the sample names from the sample sheet for the remaining column labels. In other words, each row consists of a gene id, and putative gene symbol for that gene, and the estimated counts for each of the samples. For a differential expression analysis to be performed, one needs to know the experimental condition for each of the samples. The sample sheet supplied to *nf-core/rnaseq* does not include this information, so we need to generate a sample sheet that can be supplied to *limma*, which looks like this:



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
