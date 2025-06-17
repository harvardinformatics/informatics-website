
# Research & Publications

The FAS Informatics group conducts a variety of research:

-  On bioinformatics methods and best practices in aid of our service mission
-  As part of ongoing collaborations with research labs at Harvard
-  On topics supported by research grants awarded to the Informatics group

We are a broad group with diverse expertise in the computational analysis of sequencing data, software and pipeline development, experimental design, troubleshooting bioinformatics workflows, data visualization, and analysis and management of biological big data. Although we have experience in a broad range of topics, we've focused particularly on genome assembly and annotation; bulk and single-cell RNA-seq analysis; and population and comparative genomics. We've also worked extensively on methods related to phylogenetic models of sequence evolution, and have been supported by multiple grants related to comparative genomics and convergent evolution.

|     |     |     |     |
| --- | --- | --- | --- |
| :fontawesome-regular-handshake:{ .research-icon } = Collaboration | :fontawesome-solid-hand-holding-dollar:{ .research-icon } = Grant supported | :material-lan-check:{ .research-icon } = Best practices | :material-vector-polyline-plus:{ .research-icon } = Methods development |
| :fontawesome-solid-graduation-cap: = Group alumni |    |    |

## Genome Assembly and Annotation

A major focus of recent work in the group has been to assist with the assembly and annotation of diverse genomes, often complex and difficult, using long-read sequencing technologies (e.g., Oxford Nanpore and PacBio sequencing). In collaboration with the [Bauer Sequencing Core :octicons-link-external-24:](https://bauercore.fas.harvard.edu/){:target="_blank"}, we support assembly and annotation from sample to finished genome. Our recent work in this area includes both collaborations on the genomes of diverse species, and best practices research to assess methods used to produce gene annotations across the tree of life. 


### Panther worm (*Hofstenia*) genomics &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformaticians**: Danielle Khost and Adam Freedman

**Collaborators**: [Srivastava Lab :octicons-link-external-24:](http://www.srivastavalab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"})

The lab needed to come up with an approach to integrate genome annotations from two different methods: direct assembly of transcripts from RNA-seq reads aligned to the genome, and de novo transcriptome assembly. There was also a question as to why functionally validated single-exon transcripts in the latter failed to be assembled in the former. We came up with a sensible integration strategy that also filters out lowly expressed single-exon transcripts that might be false positives.

### Performance assessment of genome annotation methods across the tree of life &nbsp; :material-lan-check:{ .research-icon }

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

(old text was for the wrong project)

!!! abstract "Publication"

    * **Freedman AH**, **Sackton TB**. 2025. Building better genome annotations across the tree of life. *Genome Research*. 35:1261-1276. [Link :octicons-link-external-24:](https://www.genome.org/cgi/doi/10.1101/gr.280377.124){:target="_blank"}


### Genomics of *Phlox* wildflowers &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Hopkins Lab :octicons-link-external-24:](https://hopkins-lab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [Arnold Arboretum :octicons-link-external-24:](https://arboretum.harvard.edu/){:target="_blank"})

We helped the Hopkins lab sequence and assemble the genomes of four species of *Phlox* wildflowers using Oxford Nanopore sequencing, as well as scaffolding into chromosome-scale reference assemblies using optical mapping and genetic maps. These samples were particularly challenging due to the large genome sizes (>6 Gbase) and highly repetitive nature of the genomes (~90% repeats). For comparative analysis, we also helped construct whole-genome alignments for the scaffolded genomes, a task that is also challenging for large plant genomes.

### Assembling difficult worm genomes &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Giribet Lab :octicons-link-external-24:](https://giribetgroup.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"})

We worked with several members of the Giribet lab to sequence and assemble genomes for a variety of unusual species from areas of the tree of life that are poorly represented with sequencing data, such as velvet worms and marine priapulid worms. The experimental design, sequencing, and assembly for these projects was difficult due to the small size of the organisms and the scarcity of samples.

!!! abstract "Publications"

    * Lord A, Cunha TJ, de Medeiros BAS, Sato S, **Khost D**, **Sackton TB**, Giribet G. 2023. Expanding on Our Knowledge of Ecdysozoan Genomes: A Contiguous Assembly of the Meiofaunal Priapulan *Tubiluchus corallicola*. *Genome Biology and Evolution*. 15(6):evad103 [Link :octicons-link-external-24:](https://doi.org/10.1093/gbe/evad103){:target="_blank"}

    * Sato S, Cunha TJ, de Medeiros BAS, **Khost D**, **Sackton TB**, Giribet G. 2023. Sizing Up the Onychophoran Genome: Repeats, Introns, and Gene Family Expansion Contribute to Genome Gigantism in *Epiperipatus broadwayi*. *Genome Biology and Evolution*. 15(3):evad021 [Link :octicons-link-external-24:](https://doi.org/10.1093/gbe/evad021){:target="_blank"}


### Assembling the genome of a parasitic plant &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformaticians**: Danielle Khost, Brian Arnold :fontawesome-solid-graduation-cap:, and Tim Sackton

**Collaborators**: [Davis Lab :octicons-link-external-24:](https://davislab.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"}

*Sapria himalayana* is a parasitic plant in the family Rafflesiaceae, which includes the species with the largest flower in the world. The Davis Lab had worked on these plants for many years, but had not produced a usable genome assembly of this fascinating plant. Several members of the Informatics group collaborated with the Davis Lab to assemble a genome of *S. himalayana* and identify unusual features of this species, including the loss of 44% of conserved plant genes and the presence of horizontally transfered genetic elements from the host species. 

!!! abstract "Publication"

    * Cai L, Arnold BJ :fontawesome-solid-graduation-cap:, Xi Z, **Khost DE**, Patel N, Hartmann CB, ... Mathews S, **Sackton TB**, Davis CD, 2021. Deeply Altered Genome Architecture in the Endoparasitic Flowering Plant Sapria himalayana Griff. (Rafflesiaceae). *Current Biology* 31:1002-1011. [Link :octicons-link-external-24:]( https://doi.org/10.1016/j.cub.2020.12.045){:target="_blank"}


### Assembling the genome of the extinct moa &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformaticians**: Tim Sackton

**Collaborators**: [Edwards Lab :octicons-link-external-24:](https://edwards.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"})

The little bush moa, *Anomalopteryx didiformis*, is one of approximately nine species of extinct flightless birds from Aotearoa, New Zealand. As part of a collaboration with the Edwards Lab, the Informatics group helped to assemble and analyze the genome of this species. 

!!! abstract "Publication"

    * Edwards SV, Cloutier A, Cockburn G, Grayson P, Katoh K, Baldwin MW, **Sackton TB**, Baker AJ. 2024.A nuclear genome assembly of an extinct flightless bird, the little bush moa. *Science Advances* 10:21. [Link :octicons-link-external-24:]( https://doi.org/10.1126/sciadv.adj6823){:target="_blank"}


## Bulk and Single-cell RNA-seq

The group has a long-standing interest in the analysis of RNA-seq data, both traditional bulk data from whole organisms or tissues, and single-cell data. In this area, we have primarily worked on methods and best practices, as well as contributed to collaborations. 

### Deep sea tubeworm transcriptomics &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformatcian**: Adam Freedman

**Collaborators**: [Girguis lab :octicons-link-external-24:](https://www.girguislab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"})

Most autotrophic organisms possess a single carbon fixation pathway. The chemoautotrophic symbionts of the hydrothermal vent tubeworm *Riftia pachyptila*, however, possess two functional pathways: the Calvin–Benson–Bassham (CBB) and the reductive tricarboxylic acid (rTCA) cycles. How these two pathways are coordinated is unknown. The Girguis lab investigated these pathways with a combination of bulk RNA-seq, and estimates of carbon fixation rates. Our role was to disentangle host (tubeworm) and symbiont (bacterium) reads in the sequence libraries, and generate gene expression counts used for downstream analyses.

!!! abstract "Publication"

    * Mitchell JH, **Freedman AH**, Delaney JA, Girguis PR. 2024. Co-expression analysis reveals distinct alliances around two carbon fixation pathways in hydrothermal vent symbionts. *Nature Microbiology*. 9:1526-1539. [Link :octicons-link-external-24:]( https://doi.org/10.1038/s41564-024-01704-y){:target="_blank"}

### Limb regeneration in axolotls &nbsp; :fontawesome-regular-handshake:{ .research-icon }

**Lead Bioinformatician**: Adam Freedman, Tim Sackton

**Collaborators**: [Whited Lab :octicons-link-external-24:](https://www.whitedlab.com/){:target="_blank"} ([SCRB :octicons-link-external-24:](https://hscrb.harvard.edu/){:target="_blank"})

The Whited lab is investigating the genetic architecture of regeneration in axolotls using single-cell RNA-seq. We provided guidance for the data analysis pipeline, particularly at the data cleanup, filtering, and quality control stage.

!!! abstract "Publication"

    * Payzin-Dogru D, Blair SJ, ..., **Freedman AH**, ..., **Sackton TB**, Whited JL, 2024. Peripheral nervous system mediates body-wide stem cell activation for limb regeneration. *bioRxiv*. [Link :octicons-link-external-24:](https://doi.org/10.1101/2021.12.29.474455){:target="_blank"}


### Assessing errors and biases in *de novo* transcriptome assembly &nbsp; :material-lan-check:{ .research-icon }

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

At the time we launched this study, approximately 60,000 published papers had relied on *de novo* transcriptome assembly. Yet, in the published literature and in the case of Harvard researchers seeking guidance, transcriptomes seemed to be highly fragmented, consisting of  hundreds of thousands (sometimes over one million) putative transcripts, the median length of which was rarely more than 400-500 base pairs. We investigated the extent of bias and errors in expression estimates and population genetic parameters derived from *de novo* transcriptome assemblies.

!!! abstract "Publication"

    * **Freedman AH**, Clamp M :fontawesome-solid-graduation-cap:, **Sackton TB**. 2021. Error, noise and bias in *de novo* transcriptome assemblies. *Molecular Ecology Resources*. 21:18-29. [Link :octicons-link-external-24:](https://doi.org/10.1111/1755-0998.13156){:target="_blank"}

### Comparing efficacy of short paired-end versus longer single-end reads in bulk RNA-seq experiments &nbsp; :material-lan-check:{ .research-icon }

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

Typical experimental design advice for expression analyses using RNA-seq generally assumes that single-end reads provide robust gene-level expression estimates in a cost-effective manner, and that the additional benefits obtained from paired-end sequencing are not worth the additional cost. However, in many cases (e.g., with Illumina NextSeq and NovaSeq instruments), shorter paired-end reads and longer single-end reads can be generated for the same cost, and it is not obvious which strategy should be preferred. Using publicly available data, we test whether short-paired end reads can achieve more robust expression estimates and differential expression results than single-end reads of approximately the same total number of sequenced bases.

!!! abstract "Publication"

    * **Freedman AH**, Gaspar JM :fontawesome-solid-graduation-cap:, **Sackton TB**. 2020. Short paired-end reads trump long single-end reads for expression analysis. *BMC Bioinformatics*. 21(149). [Link :octicons-link-external-24:](https://doi.org/10.1186/s12859-020-3484-z){:target="_blank"}


### The impact of single cell RNA-seq techniques on ecological genomics &nbsp; :material-lan-check:{ .research-icon }

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

***Invited Review***

Based on our experience with the increasing feasibility of single-cell RNA-seq experiments in diverse organisms beyond the usual model organism context, we wrote a review outlining our perspective on how gene expression studies in ecological genetics could adapt, change, and benefit from the technological revolution in sequencing. 

!!! abstract "Publication"

    * **Freedman AH**, **Sackton TB**. 2024. Rethinking eco‐evo studies of gene expression for non‐model organisms in the genomic era. *Molecular Ecology*. e17378. [Link :octicons-link-external-24:](https://doi.org/10.1111/mec.17378){:target="_blank"}


## Population Genetics

The group has worked on a variety of topics related to population genetics. These include novel methodological approaches, including a large collaborative project to create a comparative pangenome for scrub jays; and work to make variant calling best practices more accessible. We have also been involved in helping provide empirical examples and datasets in the aid of development of new theorectical coalescent models. 

### Scrub jay pangenomes &nbsp; :fontawesome-regular-handshake:{ .research-icon } &nbsp; :fontawesome-solid-hand-holding-dollar:{ .research-icon }

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Edwards Lab :octicons-link-external-24:](https://edwards.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"}), [Chen Lab :octicons-link-external-24:](https://chenlab.oeb.harvard.edu/){:target="_blank"} ([University of Rochester, Department of Biology :octicons-link-external-24:](https://www.sas.rochester.edu/bio/index.html){:target="_blank"}), [Erik Garrison :octicons-link-external-24:](http://hypervolu.me/~erik/erik_garrison.html){:target="_blank"} ([University of Tennessee Health Science Center :octicons-link-external-24:](https://www.uthsc.edu/){:target="_blank"})

<img class="inline-icon" src="../img/icons/nih-logo.svg" width="40" alt="NIH logo"> **Funded by an [NIH :octicons-link-external-24:](https://www.nih.gov/){target="_blank"} grant awarded to the Edwards and Informatics groups**

We helped generate high quality genome assemblies for 46 individual scrub jays across four species using HiFi PacBio sequencing. We developed the pipeline for assembly and scaffolding of the individual genomes, and then used those assemblies to construct a pangenome graph for the sample. This allowed us to characterize population and species level structural variation. In addition to developing the pipelines and generating the data, we also assisted with genome annotation and some downstream population genetic analysis.

!!! abstract "Publication"

    * Edwards SV, Fang B, **Khost D**, Kolyfetis GE, Cheek RG, DeRaad DA, Chen N, Fitzpatrick JW, McCormack JE, Funk WC, Ghalambor CK, Garrison E, Guarracino A, Li H, **Sackton TB**. 2025. Comparative population pangenomes reveal unexpected complexity and fitness effects of structural variants. *bioRxiv*. [Link :octicons-link-external-24:](https://doi.org/10.1101/2025.02.11.637762){:target="_blank"}


### Population genomics with snpArcher &nbsp; :fontawesome-regular-handshake:{ .research-icon } &nbsp; :material-vector-polyline-plus:{ .research-icon }

**Lead Bioinformaticians**: Tim Sackton and Gregg Thomas

Variant calling is an extremely common task in a wide variety of fields. However, this remains a complicated pipeline for many researchers, especially given the lack of readily avilable resources describing how to optimize and efficienctly run common variant calling pipelines, such as GATK, in non-human contexts. To aid researchers working in non-human species, we have developed a flexible snakemake pipeline, snpArcher, that is designed to facilitate plug-and-play variant calling for a wide range of species. 

**Software**: [snpArcher :octicons-link-external-24:](https://snparcher.readthedocs.io/en/latest/){:target="_blank"}, [degenotate :octicons-link-external-24:](https://github.com/harvardinformatics/degenotate){:target="_blank"}

!!! abstract "Publication"

    * Mirchandani CD, Shultz AJ :fontawesome-solid-graduation-cap:, **Thomas GWC**, Smith SJ :fontawesome-solid-graduation-cap:, Baylis M, Arnold B :fontawesome-solid-graduation-cap:, Corbett-Detig R, Enbody E, **Sackton TB**. 2024. A fast, reproducible, high-throughput variant calling workflow for population genomics. *Molecular Biology and Evolution*. 41(1):msad270. [Link :octicons-link-external-24:](https://doi.org/10.1093/molbev/msad270){:target="_blank"}


## Phylogenetic Methods

The Informatics group has been part of a long term collaboration to develop methods to study the molecular evolution of non-coding DNA, focusing on the software package [PhyloAcc](https://phyloacc.github.io/). We have also worked on other methods related to phylogenetic models of molecular evolution. 


### PhyloAcc: using phylogenies to detect substitution rate shifts in non-coding regions &nbsp; :fontawesome-regular-handshake:{ .research-icon } &nbsp; :fontawesome-solid-hand-holding-dollar:{ .research-icon } &nbsp; :material-vector-polyline-plus:{ .research-icon }

**Lead Bioinformaticians**: Gregg Thomas and Tim Sackton

**Collaborators**: [Edwards Lab :octicons-link-external-24:](https://edwards.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"}), [Liu Lab :octicons-link-external-24:](https://sites.harvard.edu/junliu/){:target="_blank"} ([Statistics :octicons-link-external-24:](https://statistics.fas.harvard.edu/){:target="_blank"})

<img class="inline-icon" src="../img/icons/nih-logo.svg" width="40" alt="NIH logo"> **Funded by an [NIH :octicons-link-external-24:](https://www.nih.gov/){target="_blank"} grant awarded to the Liu, Edwards, and Informatics groups**

PhyloAcc is software that was developed in the Edwards, Liu, and Informatics labs to study molecular evolution of non-coding genomic regions in a phylogenetic context. Version 1 was used to study convergent substitution rate accelerations in marine mammals and flightless birds to identify possible changes in regulatory regions that may lead to the adaptations of those respective groups. Version 2 of PhyloAcc expanded on version 1 by accounting for phylogenetic discordance and providing a friendlier user interface and batching via Snakemake.

**Software**: [PhyloAcc :octicons-link-external-24:](https://phyloacc.github.io/){:target="_blank"}

!!! abstract "Publications"

    * **Thomas GWC**, Gemmell P, Shakya SB :fontawesome-solid-graduation-cap:, Hu Z, Liu JS, **Sackton TB**, Edwards SV. 2024. Practical guidance and workflows for identifying fast evolving non-coding genomic elements using PhyloAcc. *Integrative and Comparative Biology*. 64(5):1513-1525. [Link :octicons-link-external-24:](https://doi.org/10.1093/icb/icae056){:target="_blank"}

    * Gemmell P, **Sackton TB**, Edwards SV, Liu JS. 2024. A phylogenetic method linking nucleotide substitution rates to rates of continuous trait evolution. *PLoS Computational Biology*. 20(4):e1011995. [Link :octicons-link-external-24:](https://doi.org/10.1371/journal.pcbi.1011995){:target="_blank"}

    * Yan H, Hu Z, **Thomas GWC**, Edwards SV, **Sackton TB**, Liu JS. 2023. PhyloAcc-GT: A Bayesian method for inferring patterns of substitution rate shifts on targeted lineages accounting for gene tree discordance. *Molecular Biology and Evolution*. 40(9):msad195. [Link :octicons-link-external-24:](https://doi.org/10.1093/molbev/msad195){:target="_blank"}

    * Hu Z, **Sackton TB**, Edwards SV, Liu JS. 2019. Bayesian detection of convergent rate changes of conserved noncoding elements on phylogenetic trees. *Molecular Biology and Evolution*. 36(5):1086-1100. [Link :octicons-link-external-24:](https://doi.org/10.1093/molbev/msz049){:target="_blank"}

    * **Sackton TB**, Grayson P, Cloutier A, Hu Z, Liu JS, Wheeler NE, Gardner PP, Clarke JA, Baker AJ, Clamp M, Edwards SV. 2019. Convergent regulatory evolution and loss of flight in paleognathous birds. *Science*. 364(6435):74-78. [Link :octicons-link-external-24:](https://doi.org/10.1126/science.aat7244){:target="_blank"}



## Comparative Genomics and Convergent Evolution

Convergent evolution describes the phenomenon where a similar or identical phenotype evolves in multiple independent lineages. Classic examples include diverse traits such as the evolution of echolocation in bats, cetaceans, and some species of birds; the recurrent evolution of crab-like body plans in crustaceans (carcinisation); and loss of limbs in snakes and caecilians.

Our work in this area has been funded by research grants from both the National Institutes of Health and the National Science Foundation, with a focus on using comparative and population genomics to understand genomic correlates of convergent phenotypes in birds. Along with a wide range of collaborators, we are working on population genetics of brood parasitic birds; genomic changes associated with morphological evolution towards shorter tarsi in a variety of bird clades; and the genomics of nectarivory in hummingbirds, honeyeaters, parrots, and sunbirds.

## Misc Topics

We have also worked on a variety of other topics as needed to assist with projects ranging from addressing fundamental questions about the evolution of sex to developing methods for the analysis of ATAC-seq data to providing bioinformatics support for complex proteomics projects. Some of the addtional projects Informatics team members have contributed to are listed here. 

<style>
    .inline-icon {
        vertical-align: middle;
        /* margin-bottom: 2px; /* Uncomment and tweak if needed */
    }

    .md-typeset__table {
        width: 100% !important;
        max-width: 1280px !important;
    }
    /* Ensure table takes full width */
    
    .md-typeset__table table {
        width: 100% !important;
        table-layout: fixed;
    }
    /* Ensure table takes full width and has fixed layout */

    .md-typeset th, .md-typeset td {
    white-space: normal;
    overflow-wrap: break-word;
    word-break: break-word;
    }
    /* Ensure text wraps in table cells */

    table thead { display: none; }
    .md-typeset table, 
    .md-typeset th, 
    .md-typeset td {
        border: none !important;
        background-color: #ffffff !important;
        font-size: 1em !important;
    }
    /* Remove borders from table, th, and td */

    .research-icon {
        /* color: #FAA85C; */
        /* color: #74A58E; */
        /* color: #265D80; */
        /* color: #26805E; */
        /* color: #62C375; */

        /* color: #ffffff;
        background-color: #0A2240 !important;
        border-radius: 15% !important; */

        /* color: #34BD78; */
        color: #8996A0;
        /* background-color: #0A2240;
        border: 1px solid #a41c30;
        padding: 0.1em !important;
        border-radius: 15% !important; */

        font-size: 1.2em !important;
        vertical-align: middle !important;
    }

</style>