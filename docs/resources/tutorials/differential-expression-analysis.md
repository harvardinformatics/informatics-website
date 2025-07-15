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






 


## Three major approaches to genome annotation

### 1. Model-based approaches

The current state-of-the-art tools for genome annotation can be divided into three categories. The first of these is the model-based approach that uses a Hidden Markov Model (HMM) to scan a genome sequence, classify particular segments as protein-coding, group these coding sequence (*i.e.* CDS) intervals into transcripts, and to aggregate those transcripts into genes. Among the several tools that use this approach, the most well-known and widely used is [AUGUSTUS :octicons-link-external-24:](https://github.com/Gaius-Augustus/Augustus){:target="_blank"}, the first version of which was published in 2003. Widely used optimized versions of AUGUSTUS are implemented in [BRAKER :octicons-link-external-24:](https://github.com/Gaius-Augustus/BRAKER){:target="_blank"}, which can take as input evidence in the form of protein sequences or RNA-seq data which are aligned to the genome to provide hints as to where splicing takes place, and to parameterize the underlying HMMs; BRAKER also generates annotations with [Genemark :octicons-link-external-24:](https://github.com/gatech-genemark){:target="_blank"}.
Model-based approaches typically only predict protein-coding features, such that non-coding RNAs and UTRs are not included in their output. 

#### Input data requirements for model-based approaches

* A **FASTA file** of proteins that can be aligned to the genome to generate splice hints and tune HMM parameters. For BRAKER, it is recommended to use a taxonomically appropriate set of sequences from [OrthoDB :octicons-link-external-24:](https://www.orthodb.org/){:target="_blank"}, and/or
* Spliced alignment of paired-end RNA-seq reads (derived from your species) to your genome in bam format. Our Snakemake workflow for BRAKER (see below) allow you to provide the RNA-seq data in **FASTQ** format, as one variant of the workflow can take those reads and align them to the genome with [STAR :octicons-link-external-24:](https://github.com/alexdobin/STAR){:target="_blank"}.

### 2. Assembly of RNA-seq reads

The second general approach is evidence-forward, with transcript and gene models being constructed from splice graphs that are built from spliced alignments of RNA-seq reads to the genome. Given a minimal amount of read coverage over a genomic interval, tools that implement this approach will assemble transcripts. The current state-of-the-art methods for this approach are [Stringtie :octicons-link-external-24:](https://ccb.jhu.edu/software/stringtie/){:target="_blank"} and [Scallop :octicons-link-external-24:](https://github.com/Kingsford-Group/scallop){:target="_blank"}. These methods do not classify exons as protein-coding (CDS), such that, in order to add CDS annotations to their output, one must use a tool that detects and annotates open reading frames (ORFs) such as [TransDecoder :octicons-link-external-24:](https://github.com/TransDecoder/TransDecoder){:target="_blank"}.

#### Input data requirements for RNA-seq assembly

* Paired-end RNA-seq reads in **FASTQ** format. 
* If you are using a downstream tool to predict CDS and UTRs, most likely you will also need a [BLAST :octicons-link-external-24:](https://blast.ncbi.nlm.nih.gov/Blast.cgi){:target="_blank"} database of proteins from closely related species.

### 3. Annotation transfer

Annotation transfer or _**"liftover"**_ is an approach where, through a whole genome alignment between a high-quality genome assembly (that has a similarly high-quality annotation) and an unannotated target genome assembly, annotations are transferred to homologous intervals in the target genome. One top-performing approach is [TOGA :octicons-link-external-24:](https://github.com/hillerlab/TOGA){:target="_blank"}, which transfers (only) protein-coding annotations in an exon-aware fashion, making adjustments to maximize the retention of complete ORFs. Another is [Liftoff :octicons-link-external-24:](https://github.com/agshumate/Liftoff){:target="_blank"} which transfers both coding and non-coding annotations. The quality of annotations output for the target genome depends on the completeness and quality of the source annotation and the quality of the whole-genome alignment. The latter of these is determined in large part by the extent of evolutionary divergence between the source and target genomes, such that performance declines with increasing divergence and it is recommended to use, when possible, a closely related source genome. The quality of the whole-genome alignment is also impacted by genome complexity and organization, such that liftover tools may run into problems with large, complex genomes (like some plants) that contain a large proportion of repeat elements.

#### Input data requirements for annotation transfer

* A **whole genome alignment** of your species' genome, and the genome of your reference species.
* An annotation file (in **gff3** format) for your reference species, *i.e.* the annotations that will be transferred through the genome alignment.

## Choosing an annotation method

How to choose a genome annotation method should be based upon three factors:

1. Your research objectives. For example, are you only interested protein coding genes, or even just extracting the CDS portion of transcripts, or are you also interested in ncRNAs and the UTRs of protein-coding transcripts? In other words, are you intersted in the entire transcriptome, or is your primary focus the proteome (either in nucleodide or amino acid space).  

2. Availability or ability to generate paired-end RNA-seq data.

3. Availability of a high quality genome and annotation from a reasonably closely related species (relative to your target genome) 

4. Annotation method performance, with respect to your research objectives .

While the first of these points is dependent upon your research program, the second depends upon the feasibility of obtaining RNA-seq data, and the third depends upon the history of past genomic research in the portion of the tree of life where your research program is focused. We have answered the fourth of these with a comprehesive review of genome annotation method performance. An earlier version of the manuscript resulting from this work is on bioRxiv at ["Building better genome annotations across the tree of life" :octicons-link-external-24:](https://www.biorxiv.org/content/10.1101/2024.04.12.589245v1){:target="_blank"}, and the final version (that includes two additional methods) will appear in the May 2025 issue of *Genome Research*. Our findings have led us to recommend the following tools depending upon the factors described above:

| Tool | Approach | Genomic compartment | Evidence/input type |
| ---------------------- | -------- | ------------------- | ------------------- |
| Stringtie-TransDecoder | transcriptome | RNA-seq assembly | paired-end RNA-seq reads, and a protein BLAST database | 
| BRAKER3                | HMM | proteome | OrthoDB protein fasta and paired-end RNA-seq reads |
| BRAKER2                | HMM | proteome | OrthoDB protein fasta |
| TOGA                   | annotation transfer | proteome | high quality genome and annotation from related species |
| Liftoff                | annotation transfer | transcriptome | high quality genome and annotation from related species |

Below is a decision tree for picking an annotation method, based upon our evaluation of the performance of 12 different methods in our forthcoming paper in *Genome Research.
   
<center>
    <img src="../../../../img/tutorials/genome_annotation_decision_chart.png" alt="Genome annotation method decision tree" />
</center>

The dashed lines that indicate "optional integration" refer to the combining of more than one genome annotation method, which we elaborate upon below.

A few examples are worthwhile to understand how to read the annotation tool decision tree.

#### EXAMPLE 1: RNA-seq data available and whole transcriptome desired

This represents a fairly straightforward path through the decision tree. You should run our Snakemake workflow ([see below](#workflows-for-generating-individual-annotations)) for assembling transcripts with Stringtie and annotating CDS and UTRs with TransDecoder.

#### EXAMPLE 2: no closely related genome with annotation and no RNA-seq data

This represents another straightforward path through the decision tree, leading you to use BRAKER2, an implementation of the *ab initio* tool suite that only uses proteins from OrthDB to estimate HMM model parameters and provide hints for locations of splice sites for CDS. Note that, without a closely related genome or RNA-seq data, there is no way to annotate ncRNAs, *i.e.* you are restricted to predicting protein-coding features, hence why "None available" is the terminus of the path on the left side of the graph.

### Caveats: plants!

For plant genomes, especially larger ones with high repeat content, obtaining a high-quality  whole-genome alignment with other species (even those closely related to it) can be challenging. This can lead to poorer performance in annotation transfer tools (TOGA, Liftoff) than other approaches. Thus, for any path through the decision tree that ends with an annotation transfer method, one should confirm through a number of quality assessment metrics, in particular BUSCO scores (see below) that the annotation is of reasonably good quality.

### Integrating methods: a work in progress
It may be that after choosing a particular method based upon the above decision tree, the outputs may lead you to suspect that the annotation is not as complete as it should be. For example, after assigning gene symbols to protein coding transcripts with a tool such as [eggNOG-mapper :octicons-link-external-24:](http://eggnog-mapper.embl.de/){:target="_blank"}, you may discover that genes that you are certain should be in the annotation are absent. Or, your new annotations recovers fewer conserved single-copy orthologs (i.e. BUSCOs) than you'd hoped. [see this paper :octicons-link-external-24:](https://academic.oup.com/bioinformatics/article/31/19/3210/211866){:target="_blank"} for more details. By extension, this would suggest that a number of less-conserved genes that should be in your annotation are also missing. In scenarios such as this, you might consider integrating annotations from multiple methods. This does not simply mean taking the union of two or more methods, as that would lead to much redundancy. In an ideal world,you'd select the highest quality predictions that represent the best reflection of the underlying genes, transcripts, exons, etc. The current challenge is *how* to go about doing this. There are few currently maintained tools for combining an arbitrary number of gtf/gff3 files into a unified annotation. One example is [Mikado :octicons-link-external-24:](https://github.com/EI-CoreBioinformatics/mikado){:target="_blank"} although our initial exploration of it a few years ago indicated that the scoring scheme for picking high quality transcripts may lead to the erroneous removal of real transcripts, and a subsequent loss of BUSCOs. At a future date we will explore the integration problem more deeply, and perhaps even come up with a solution! In the meantime, Mikado is worth looking at. A simpler, different approach that will not lead to any data loss would be to add annotations from one method that are non-overlapping with a "base" annotation (the entirety of which you will retain) to that base annotation:

1. Given two annotation files for your genome, set one as the "base", i.e the one you want to which you want to add additional annotations
2. Use [bedtools :octicons-link-external-24:](https://bedtools.readthedocs.io/en/latest/){:target="_blank"} to identify unique annotations in your second annotation method, i.e. those that do not overlap the genomic coordinates of your "base" annotation. 
3. Add those non-overlapping annotations to the "base". In principle, one does this at the gene-level, adding non-overlapping genes and their respective child features to the "base" annotation. 
4. If you have more than two annotations to integrate, set the initially integrated annotation as your base, and follow the steps above with the next annotation.

Whichever method you use for integrating annotations from multiple methods, a closer look at the decision tree to understand recommended combinations of tools to integrate is warranted. These decisions reflect a desire to avoid redundancy between tools that either use the same type of evidence, or make the same sort of predictions, yet with one tools clearly having poorer performance at achieving the same task. Options are as follows:

* If your goal was to annotate the entire transcriptome, and you have RNA-seq data, you would generate annotations with TransDecoder. However, BUSCO scores may indicate you are missing a non-trivial fraction of them. If that is the case, it also means you are also missing many features that are less conserved. One reason why features may be missing is if your RNA-seq data are only derived from a small subset of tissues, e.g. if you only have libraries from muscle, chances are you will fail to properly assemble (or assemble at all) genes whose expression is restricted to the brain. If a closely related genome (and annotation were available), you could then integrate annotations from TOGA to your Stringtie-TransDecoder annotation. In the absence of closely related genome, one could add BRAKER3 annotations, with the caveat that the BRAKER annotation would need to be heavily filtered to avoid a potentially high rate of intergenic false positive predictions. As an annotation transfer tool, we have found that TOGA outperforms Liftoff, and since you would have already recovered non-coding features with your Stringtie annotations, choosing Liftoff over TOGA as a second method would not be the best choice.

* If your primary focus was the proteome, and you had access to a genome and annotation of a closely related species, you would consider supplementing a TOGA annotation with Stringtie-TransDecoder. We found that, in comparing 12 different annotation methods, the recovery and accuracy of protein-coding predictions was usually highest for TOGA, which justifies using it as the base annotation, to which to add annotations from Stringtie-TransDecoder.  

## Workflows for generating individual annotations.

We have developed Snakemake workflows for *TOGA*, *BRAKER*, and assembly of genes and transcripts directly from RNA-seq reads with *Stringtie* and *TransDecoder*. Those workflows can be found here: 

* [Snakemake TOGA :octicons-link-external-24:](https://github.com/harvardinformatics/AnnotationTOGA){:target="_blank"} 
* [Snakemake BRAKER :octicons-link-external-24:](https://github.com/harvardinformatics/AnnotationBRAKER){:target="_blank"} 
* [Snakemake Stringtie-TransDecoder :octicons-link-external-24:](https://github.com/harvardinformatics/AnnotationRNAseqAssembly){:target="_blank"}

While we do not provide a Snakemake workflow for Liftoff, it is a straightforward one-line execution that can be reconstructed from the documentation, or following our implementation in our forthcoming paper in *Genome Research*, using parameters to span varying degrees of evolutionary divergence, as described [here :octicons-link-external-24:](https://github.com/harvardinformatics/GenomeAnnotation/tree/master/GenomeResearch/Liftoff){:target="_blank"}.

## Assesing genome annotation quality

For a new genome assembly, quality metrics will need to be used that don't rely on a "truth set", such as aa well-curated set of protein sequences for the species whose genome you have just assembled. Relevant metrics should be able to assess sensitivity (the ability to recover the real underlying transcripts in a genome) and accuracy, *i.e.* how well the predicted features recapitulate the true sequences. Again, in the absence of a truth set for one's species, there are metrics that employ useful proxies. A few of these are as follows:

* BUSCO score, which is simply (1 - number of recovered BUSCOs)/total number of BUSCOs in the searched database. The best way for obtaining the count of recovered BUSCOs is to use [compleasm :octicons-link-external-24:](https://github.com/huangnengCSU/compleasm){:target="_blank"} to perform sequence searches.

* A global score of proteome accuracy obtained with [psauron :octicons-link-external-24:](https://github.com/salzberg-lab/PSAURON){:target="_blank"}. psauron is a machine-learning approach, the underlying model of which was trained on  > 1000 species. It not only provides a global accuracy score for a proteome, but also provides transcript scores, which are potentially useful for post-annotation filtering of low-quality predictions

* If there is a high-quality annotation of a reasonably closely related species, looking at BLASTX coverage of the predicted proteins from your annotation against the proteome of that species. If your annotation has generated a large proportion of high-quality, complete or near-complete protein predicttions, The median BLASTX coverage of the reference species proteins by your predicted proteins should be very high.

* RNA-seq read alignment rate. An acceptable rate will depend upon whether downstream gene expression analyses will conducted, as low alignment rates may reduce precisions of expression counts and reduce power of differential expression analyses.

* Frequency of single-exon transcripts. For example, an annotation comprised mostly of short single-exon transcripts would suggest a highly fragmented annotation, with "genes" likely representing fragments of the true gene intervals. 

* Length distribution of transcripts. If the median transcript length of your annotation is 30% of the median length of a well-annotated closely related species, this would point to your annotation being comprised of fragmented transcript models. 

## A final thought: filtering
Although we have discussed annotation method types and provided a framework for choosing which methods to use, and some straightforward metrics for checking annotation quality, in most instances, your annotation will be improved with some filtering. For example, extremely short single-exon transcripts with near-zero expression (after mapping RNA-seq reads to the transcripts) are likely to be enriched for false positives. In particular, we know from our evaluation of annotation methods, that HMM-based ab initio tools can predict large numbers of protein-coding transcripts that fall outside of known protein-coding gene intervals, and that are almost certainly dominated by false positives. Setting filters to remove as much of this detritus as possible while minimizing the removal of real transcript will requires some data exploration and fine-tuning, as there is unlikely to be a one-size-fits all set of filters for all method-species combinations.

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
