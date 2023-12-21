---
hide:
    - navigation
---

<style>
    .md-sidebar--secondary {
        order: 0;
    }
</style>

# Research

Research in the Bioinformatics Group is primarily driven by collaborative projects with faculty on campus, and by grant-funded internal projects. We also conduct some best practices and methdological research to fill gaps in current knowledge and solve challenging bioinformatics problems. 

## Collaborations

### Assembling Difficult and Repetitive Genomes

A major focus of the group recently has been to assist with the assembly of complex genomes with long-read sequencing data. In collaboration with the Bauer Core, we support assembly with both PacBio HiFi and Nanopore technologies. Some recent examples include our work helping to assemble:
- the 6 Gb genome of *Phlox drummondii* (collaboration with the [Hopkins lab](https://hopkins-lab.org/))
- a variety of parasitic plant genomes (collaboration with the [Davis lab](https://davislab.oeb.harvard.edu/))
- a variety of undersampled invertebrate phyla (collaboration with the [Giribet lab](https://giribetgroup.oeb.harvard.edu/))

We are always excited to work on new and challenging genomes.

### Methods for the analysis of single-cell RNA-seq data

Another focus of the group is developing methods related to cell type identification in the context of single cell RNA sequencing. This includes method development to assess the stablity of cell clustering, done in collaboration with the [Dulac Lab](https://www.dulaclab.com/), and work to develop new methods of cross-species comparison, funded by a collaborative agreement with Boehringer Ingelheim.

## Best practices and methodological research

### Genome annotation and RNA-seq analysis

A major focus of our recent best practices research has been to develop and test approaches for genome annotation. As genome assembly becomes more feasible for a diverse range of organisms, the need to understand how to best predict gene models in newly assembled organisms is only increasing. We have tested a variety of different commonly used methods for genome annotation in a number of different plant and animal species, with a goal of identifying robust, high-qualty methods that can be widely applied. This research has grown out of our longstanding interests in assesssing best practices for RNA-seq assembly, particularly in the context of transcriptome assembly in non-model species. 

While this work is ongoing we are always happen to discuss new annotation projects and share preliminary results. 

### snpArcher

Variant calling is an extremely common task in a wide variety of fields. However, this remains a complicated pipeline many researchers, especially given the lack of readily avilable resources describing how to optimize and efficienctly run common variant calling pipelines, such as GATK, in non-human contexts. To aid researchers working in non-human species, we have developed a flexible snakemake pipeline, [snpArcher](https://snparcher.readthedocs.io/en/latest/), that is designed to facilitate plug-and-play variant calling for a wide range of species. 

## Grant funded research

The group is also supported by several research grants, which fund postdoctoral research in the Bioinformatics group. Our major research interests revolve around understanding the genomic basis of convergent evolution.

### Convergent evolution

Convergent evolution describes the phenomenon where a similar or identical phenotype evolves in multiple independent lineages. Classic examples include diverse traits such as the evolution of echolocation in bats, cetaceans, and some species of birds; the recurrent evolution of crab-like body plans in crustaceans (carcinisation); and loss of limbs in snakes and caecilians. 

Our work in this area - funded by NSF and NIH grants - has focused on using comparative and population genomics to understand genomic correlates of convergent phenotypes in birds. Along with a wide range of collaborators, we are working on population genetics of brood parasitic birds; genomic changes associated with morphological evolution towards shorter tarsi in a variety of bird clades; and the genomics of nectarivory in hummingbirds, honeyeaters, parrots, and sunbirds. 