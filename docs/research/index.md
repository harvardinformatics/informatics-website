
<style>
    .inline-icon {
    vertical-align: middle;
    /* margin-bottom: 2px; /* Uncomment and tweak if needed */
    }
</style>

# Research & Publications

Research in the Bioinformatics Group is primarily driven by collaborative projects with faculty on campus, and by grant-funded internal projects. We also conduct best practices and methdological research to fill gaps in current knowledge and solve challenging bioinformatics problems.

:fontawesome-solid-graduation-cap: = Group alumni

## Collaborations

### Scrub jay pangenomes

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Edwards Lab :octicons-link-external-24:](https://edwards.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"}), [Chen Lab :octicons-link-external-24:](https://chenlab.oeb.harvard.edu/){:target="_blank"} ([University of Rochester, Department of Biology :octicons-link-external-24:](https://www.sas.rochester.edu/bio/index.html){:target="_blank"}), [Erik Garrison :octicons-link-external-24:](http://hypervolu.me/~erik/erik_garrison.html){:target="_blank"} ([University of Tennessee Health Science Center :octicons-link-external-24:](https://www.uthsc.edu/){:target="_blank"})

<img class="inline-icon" src="../img/icons/nih-logo.svg" width="40" alt="NIH logo"> **Funded by an [NIH :octicons-link-external-24:](https://www.nih.gov/){target="_blank"} grant awarded to the Edwards and Informatics groups**

We helped generate high quality genome assemblies for 46 individual scrub jays across four species using HiFi PacBio sequencing. We developed the pipeline for assembly and scaffolding of the individual genomes, and then used those assemblies to construct a pangenome graph for the sample. This allowed us to characterize population and species level structural variation. In addition to developing the pipelines and generating the data, we also assisted with genome annotation and some downstream population genetic analysis.

!!! abstract "Publication"

    * Edwards SV, Fang B, **Khost D**, Kolyfetis GE, Cheek RG, DeRaad DA, Chen N, Fitzpatrick JW, McCormack JE, Funk WC, Ghalambor CK, Garrison E, Guarracino A, Li H, **Sackton TB**. 2025. Comparative population pangenomes reveal unexpected complexity and fitness effects of structural variants. *bioRxiv*. [Link :octicons-link-external-24:](https://doi.org/10.1101/2025.02.11.637762){:target="_blank"}

Panther worm (*Hofstenia*) genomics

**Lead Bioinformaticians**: Danielle Khost and Adam Freedman

**Collaborators**: [Srivastava Lab :octicons-link-external-24:](http://www.srivastavalab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"})

The lab needed to come up with an approach to integrate genome annotations from two different methods: direct assembly of transcripts from RNA-seq reads aligned to the genome, and de novo transcriptome assembly. There was also a question as to why functionally validated single-exon transcripts in the latter failed to be assembled in the former. We came up with a sensible integration strategy that also filters out lowly expressed single-exon transcripts that might be false positives.

### Deep sea tubeworm transcriptomics

**Lead Bioinformatcian**: Adam Freedman

**Collaborators**: [Girguis lab :octicons-link-external-24:](https://www.girguislab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"})

Most autotrophic organisms possess a single carbon fixation pathway. The chemoautotrophic symbionts of the hydrothermal vent tubeworm *Riftia pachyptila*, however, possess two functional pathways: the Calvin–Benson–Bassham (CBB) and the reductive tricarboxylic acid (rTCA) cycles. How these two pathways are coordinated is unknown. The Girguis lab investigated these pathways with a combination of bulk RNA-seq, and estimates of carbon fixation rates. Our role was to disentangle host (tubeworm) and symbiont (bacterium) reads in the sequence libraries, and generate gene expression counts used for downstream analyses.

!!! abstract "Publication"

    * Mitchell JH, **Freedman AH**, Delaney JA, Girguis PR. 2024. Co-expression analysis reveals distinct alliances around two carbon fixation pathways in hydrothermal vent symbionts. *Nature Microbiology*. 9:1526-1539. [Link :octicons-link-external-24:]( https://doi.org/10.1038/s41564-024-01704-y){:target="_blank"}

### Genomics of *Phlox* wildflowers

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Hopkins Lab :octicons-link-external-24:](https://hopkins-lab.org/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [Arnold Arboretum :octicons-link-external-24:](https://arboretum.harvard.edu/){:target="_blank"})

We helped the Hopkins lab sequence and assemble the genomes of four species of *Phlox* wildflowers using Oxford Nanopore sequencing, as well as scaffolding into chromosome-scale reference assemblies using optical mapping and genetic maps. These samples were particularly challenging due to the large genome sizes (>6 Gbase) and highly repetitive nature of the genomes (~90% repeats). For comparative analysis, we also helped construct whole-genome alignments for the scaffolded genomes, a task that is also challenging for large plant genomes.

### Assembling difficult worm genomes

**Lead Bioinformaticians**: Danielle Khost and Tim Sackton

**Collaborators**: [Giribet Lab :octicons-link-external-24:](https://giribetgroup.oeb.harvard.edu/){:target="_blank"} ([OEB :octicons-link-external-24:](https://www.oeb.harvard.edu/){:target="_blank"} / [MCZ :octicons-link-external-24:](https://www.mcz.harvard.edu/){:target="_blank"})

We worked with several members of the Giribet lab to sequence and assemble genomes for a variety of unusual species from areas of the tree of life that are poorly represented with sequencing data, such as velvet worms and marine priapulid worms. The experimental design, sequencing, and assembly for these projects was difficult due to the small size of the organisms and the scarcity of samples.

!!! abstract "Publications"

    * Lord A, Cunha TJ, de Medeiros BAS, Sato S, **Khost D**, **Sackton TB**, Giribet G. 2023. Expanding on Our Knowledge of Ecdysozoan Genomes: A Contiguous Assembly of the Meiofaunal Priapulan *Tubiluchus corallicola*. *Genome Biology and Evolution*. 15(6):evad103 [Link :octicons-link-external-24:](https://doi.org/10.1093/gbe/evad103){:target="_blank"}

    * Sato S, Cunha TJ, de Medeiros BAS, **Khost D**, **Sackton TB**, Giribet G. 2023. Sizing Up the Onychophoran Genome: Repeats, Introns, and Gene Family Expansion Contribute to Genome Gigantism in *Epiperipatus broadwayi*. *Genome Biology and Evolution*. 15(3):evad021 [Link :octicons-link-external-24:](https://doi.org/10.1093/gbe/evad021){:target="_blank"}

### Limb regeneration in axolotls

**Lead Bioinformatician**: Adam Freedman

**Collaborators**: [Whited Lab :octicons-link-external-24:](https://www.whitedlab.com/){:target="_blank"} ([SCRB :octicons-link-external-24:](https://hscrb.harvard.edu/){:target="_blank"})

The Whited lab is investigating the genetic architecture of regeneration in axolotls using single-cell RNA-seq. We provided guidance for the data analysis pipeline, particularly at the data cleanup, filtering, and quality control stage.

!!! abstract "Publication"

    * Payzin-Dogru D, Blair SJ, ..., **Freedman AH**, ..., **Sackton TB**, Whited JL, 2024. Peripheral nervous system mediates body-wide stem cell activation for limb regeneration. *bioRxiv*. [Link :octicons-link-external-24:](https://doi.org/10.1101/2021.12.29.474455){:target="_blank"}


## Best practices and methodological research

### Performance assessment of genome annotation methods across the tree of life

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

Recent technological advances in long-read DNA sequencing accompanied by reduction in costs have made the production of genome assemblies financially achievable and computationally feasible, such that genome assembly no longer represents the major hurdle to evolutionary analysis for most non-model organisms. Now, the more difficult challenge is to properly annotate a draft genome assembly once it has been constructed. The primary challenge to annotations is how to select from the myriad gene prediction tools that are currently available, determine what kinds of data are necessary to generate high-quality annotations, and evaluate the quality of the annotation. To determine which methods perform the best and to determine whether the inclusion of RNA-seq data is necessary to obtain a high-quality annotation, we generated annotations with 12 different methods for 21 different species spanning vertebrates, plants, and insects. We found that the annotation transfer method TOGA, BRAKER3, and the RNA-seq assembler StringTie were consistently top performers across a variety of metrics including BUSCO recovery, CDS length, and false-positive rate, with the exception that TOGA performed less well in some monocots with respect to BUSCO recovery. The choice of which of the top-performing methods will depend upon the feasibility of whole-genome alignment, availability of RNA-seq data, importance of capturing noncoding parts of the transcriptome, and, when whole-genome alignment is not feasible, the relative performance in BUSCO recovery between BRAKER3 and StringTie. When whole-genome alignment is not feasible, inclusion of RNA-seq data will lead to substantial improvements to genome annotations.

!!! abstract "Publication"

    * **Freedman AH**, **Sackton TB**. 2025. Building better genome annotations across the tree of life. *Genome Research*. 35:1261-1276. [Link :octicons-link-external-24:](https://www.genome.org/cgi/doi/10.1101/gr.280377.124){:target="_blank"}

### Population genomics with snpArcher

**Lead Bioinformaticians**: Tim Sackton and Gregg Thomas

Variant calling is an extremely common task in a wide variety of fields. However, this remains a complicated pipeline for many researchers, especially given the lack of readily avilable resources describing how to optimize and efficienctly run common variant calling pipelines, such as GATK, in non-human contexts. To aid researchers working in non-human species, we have developed a flexible snakemake pipeline, snpArcher, that is designed to facilitate plug-and-play variant calling for a wide range of species. 

**Software**: [snpArcher :octicons-link-external-24:](https://snparcher.readthedocs.io/en/latest/){:target="_blank"}, [degenotate :octicons-link-external-24:](https://github.com/harvardinformatics/degenotate){:target="_blank"}

!!! abstract "Publication"

    * Mirchandani CD, Shultz AJ :fontawesome-solid-graduation-cap:, **Thomas GWC**, Smith SJ :fontawesome-solid-graduation-cap:, Baylis M, Arnold B :fontawesome-solid-graduation-cap:, Corbett-Detig R, Enbody E, **Sackton TB**. 2024. A fast, reproducible, high-throughput variant calling workflow for population genomics. *Molecular Biology and Evolution*. 41(1):msad270. [Link :octicons-link-external-24:](https://doi.org/10.1093/molbev/msad270){:target="_blank"}

### PhyloAcc: using phylogenies to detect substitution rate shifts in non-coding regions

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

### Assessing errors and biases in *de novo* transcriptome assembly

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

*De novo* transcriptome assembly is a powerful tool, and has been widely used over the last decade for making evolutionary inferences. However, it relies on two implicit assumptions: that the assembled transcriptome is an unbiased representation of the underlying expressed transcriptome, and that expression estimates from the assembly are good, if noisy approximations of the relative abundance of expressed transcripts. Using publicly available data for model organisms, we demonstrate that, across assembly algorithms and data sets, these assumptions are consistently violated. Bias exists at the nucleotide level, with genotyping error rates ranging from 30% to 83%. As a result, diversity is underestimated in transcriptome assemblies, with consistent underestimation of heterozygosity in all but the most inbred samples. Even at the gene level, expression estimates show wide deviations from map-to-reference estimates, and positive bias at lower expression levels. Standard filtering of transcriptome assemblies improves the robustness of gene expression estimates but leads to the loss of a meaningful number of protein-coding genes, including many that are highly expressed. We demonstrate a computational method, length-rescaled CPM, to partly alleviate noise and bias in expression estimates. Researchers should consider ways to minimize the impact of bias in transcriptome assemblies.

!!! abstract "Publication"

    * **Freedman AH**, Clamp M, **Sackton TB**. 2021. Error, noise and bias in de novo transcriptome assemblies. *Molecular Ecology Resources*. 21:18-29. [Link :octicons-link-external-24:](https://doi.org/10.1111/1755-0998.13156){:target="_blank"}

### Comparing efficacy of short paired-end versus longer single-end reads in bulk RNA-seq experiments

**Lead Bioinformaticians**: Adam Freedman and Tim Sackton

Typical experimental design advice for expression analyses using RNA-seq generally assumes that single-end reads provide robust gene-level expression estimates in a cost-effective manner, and that the additional benefits obtained from paired-end sequencing are not worth the additional cost. However, in many cases (e.g., with Illumina NextSeq and NovaSeq instruments), shorter paired-end reads and longer single-end reads can be generated for the same cost, and it is not obvious which strategy should be preferred. Using publicly available data, we test whether short-paired end reads can achieve more robust expression estimates and differential expression results than single-end reads of approximately the same total number of sequenced bases.

!!! abstract "Publication"

    * **Freedman AH**, Gaspar JM, **Sackton TB**. 2020. Short paired-end reads trump long single-end reads for expression analysis. *BMC Bioinformatics*. 21(149). [Link :octicons-link-external-24:](https://doi.org/10.1186/s12859-020-3484-z){:target="_blank"}





