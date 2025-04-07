---
title: Genome annotation
---

<style>
/* FAQ styles */
    details > h5 {
        display: none;
    }
</style>

With the rapid increase in the number of new genomes being assembled, the strigent input data requirements for publicly available resources for automating genome annotation (e.g. Ensembl and NCBI), and inevitable increasing wait times for the production of new annotations by those resources, researchers will be increasingly faced with having to generate annotations for their new genome builds themselves. The two immediate challenges they face are:

1. Deciding which tools are best suited for generating a high-quality annotation, and 
2. Actually running those tools on an HPC cluster.

Here, we provide a brief overview of the three dominant flavors of genome annotation represented by current state-of-the-art tools, provide guidance for picking the right tools, and briefly describe and point to [Snakemake](https://snakemake.readthedocs.io/en/stable/) worfklows that can, with a modest amount of parameter specification, automate the generation of genome annotations in gff/gtf format. If you are unfamiliar with this file format, take a look at [this file format definition](http://useast.ensembl.org/info/website/upload/gff.html) found at *Ensembl*.

## Three major approaches to genome annotation
### 1. Model-based approaches
The current state-of-the-art tools for genome annotation can be divided into three categories. The first of these is the model-based approach that uses a Hidden Markov Model (HMM) to scan a genome sequence, classify particular segments as protein-coding, and group these coding sequence (i.e CDS) intervals into transcripts, and to aggregate those transcripts into genes. Among the several tools that use this approach, the most well-known and widely used is [AUGUSTUS](https://github.com/Gaius-Augustus/Augustus), the first version of which was published in 2003. Widely used optimized versions of AUGUSTUS are implemented in [BRAKER](https://github.com/Gaius-Augustus/BRAKER), which can take extrinsic evidence in the form of protein sequences or RNA-seq data which are aligned to the genome to provide hints as to where splicing takes place, and to parameterize the underlying HMMs; BRAKER also generates annotations with [Genemark](https://github.com/gatech-genemark). Model-based approaches typically only predict protein-coding features, such that non-coding RNAs and UTRs are not included in their output.  

### 2. Assembly of RNA-seq reads
The second general approach is evidence-forward, with transcript and gene models being constructed from splice graphs that are built from spliced alignments of RNA-seq reads to the genome. Given a minimal amount of read coverage over a genomic interval, tools that implement this approach will assemble transcripts. The current state-of-the-art for this approach is represented by [Stringtie](https://ccb.jhu.edu/software/stringtie/) and [Scallop](https://github.com/Kingsford-Group/scallop). These methods do not classify exons as protein-coding (CDS), such that, in order to add CDS annotations to their output, one must use a tool that detects and annotates open reading frames (ORFs) such as [TransDecoder](https://github.com/TransDecoder/TransDecoder).

### 3. Annotation transfer
Annotation transfer or "liftover" is an approach where, through a whole genome alignment between a high-quality genome assembly (and a similarly high-quality annotation) and an unannotated target genome, annotations are transferred to homologous intervals in the target genome. One top-performing approach is [TOGA](https://github.com/hillerlab/TOGA), which transfers (only) protein-coding annotations in an exon-aware fashion, making adjustments to maximize the retention of complete ORFs. Another is [Liftoff](https://github.com/agshumate/Liftoff) which transfers both coding and non-coding annotations. The quality of annotations output for the target genome depend upon the completeness and quality of the source annotation and the quality of the whole-genome alignment. The latter of these is determined in large part by the extent of evolutionary divergence between the source and target genomes, such that performance declines with increasing divergence and it is recommended to use, when possible, a closely related source genome. The quality of the whole-genome alignment is also impacted by genome complexity and organization, such that liftover tools may run into problems with large, complex plant genomes that contain a large proportion of repeat elements.

## Choosing an annotation method
How to choose a genome annotation method should be based upon three factors:

1. Your research objectives. For example,are you only interesting protein coding genes, or even just extracting the CDS portion of transcripts, or are you also interested in ncRNAs and the UTRs of protein-coding transcripts? In other words, are you intersted in the entire transcriptome, or is your primary focus the proteome (either in nucleodide or amino acid space).  

2. Availability or ability to generate paired-end RNA-seq data  

3. Availability of a high quality genome and annotation from a reasonably closely related species (relative to your target genome) 

4. Annotation method performance, with respect to your research objectives 

While the first of these points is dependent upon your research program, the second depends upon the feasibility of obtaining RNA-seq data, and the third depends upon the history of past genomic research in the portion of the tree of life where your research program is focused, we have answered the fourth of these with a comprehesive review of genome annotation method performance. An earlier version of the manuscript resulting from this work is on bioRxiv at ["Building better genome annotations across the tree of life"](https://www.biorxiv.org/content/10.1101/2024.04.12.589245v1), and the final version (that includes two additional methods) will appear in the May 2025 issue of *Genome Research*. Our findings have led us to recommend the following decision tree for picking an annotation method.
   
<center>
![Genome annotation method decision tree](../img/genome_annotation_decision_chart.png)
</center>

The dashed lines that indicate "optional integration" refer to the combining of more than one genome annotation method. For example, after testing a few different methods, you might discover that there is some degree of complementarity in the recovery of conserved single-copy orthologs, i.e. BUSCOs [see this paper](https://academic.oup.com/bioinformatics/article/31/19/3210/211866) for more details. The current challenge is *how* to go about doing this. There are few currently maintained tools for combining an arbitrary number of gtf/gff3 files into a unified annotation. One example is [Mikado](https://github.com/EI-CoreBioinformatics/mikado) although our initial exploration of it a few years ago indicated that the scoring scheme for picking high quality transcripts may lead to the erroneous removal of real transcripts, and a subsequent loss of BUSCOs. At a future date we will explore the integration problem more deeply, and perhaps even come up with a solution! In the meantime, Mikado is worth looking at. A simpler, different approach that will not lead to any data loss would be to add annotations from one method that are non-overlapping with a "base" annotation (the entirety of which you will retain) to that base annotation

1. Given two annotation files for your genome, set one as the "base", i.e the one you want to which you want to add additional annotations
2. Use [bedtools](https://bedtools.readthedocs.io/en/latest/) to identify unique annotations in your second annotation method, i.e. those that do not overlap the genomic coordinates of your "base" annotation. 
3. Add those non-overlapping annotations to the "base". In principle, one does this at the gene-level, adding non-overlapping genes and their respective child features to the "base" annotation. 
4. If you have more than two annotations to integrate, set the initially integrated annotation as your base, and follow the steps above with the next annotation.

## Workflows for generating individual annotations.
We have developed Snakemake workflows for *TOGA*, *BRAKER*, and assembly of genes and transcripts directly from RNA-seq reads with *Stringtie* and *TransDecoder*. Those workflows can be found here: 

* [Snakemake TOGA](https://github.com/harvardinformatics/AnnotationTOGA) 
* [Snakemake BRAKER](https://github.com/harvardinformatics/AnnotationBRAKER) 
* [Snakemake Stringtie-TransDecoder](https://github.com/harvardinformatics/AnnotationRNAseqAssembly)

While we do not provide a Snakemake workflow for Liftoff, it is a straightforward one-line execution that can be reconstructed from the documentation, or following our implementation in our forthcoming paper in *Genome Research*, using parameters to span varying degrees of evolutionary divergence, and is described [here](https://github.com/harvardinformatics/GenomeAnnotation/tree/master/GenomeResearch/Liftoff).
