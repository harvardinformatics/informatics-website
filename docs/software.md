---
hide:
    - navigation
    - toc
---

# Software

The informatics group develops methods and software for various genomics tasks with an emphasis on reproducibility and ease of use. We aim to provide tools that fill gaps in the current genomics software ecosystem. We also collaborate both within and outside of Harvard to develop new methods.

# Software

## 
<div class="software-logo-cont">
    <a href="https://phyloacc.github.io/" target="_blank">
        <img class="software-logo" src="../img/phyloacc-link-logo.png">
    </a>
</div>

[PhyloAcc](https://phyloacc.github.io/) is a program to detect shifts of DNA substitution rates in noncoding, conserved genomic regions. It can be used to identify genomic elements that have experienced accelerated rates along certain lineages in a phylogeny. This can be used, for example, to identify convergent rate shifts that coincide with phenotypic convergence. 

We have developed this in conjunction with the [Edwards Lab](https://edwards.oeb.harvard.edu/) in the Organismic and Evolutionary Biology department and the Museum of Comparative Zoology and the [Liu Lab](https://sites.harvard.edu/junliu/) in the Department of Statistics.

---

##
<div class="software-logo-cont">
    <a href="https://github.com/harvardinformatics/snpArcher" target="_blank">
        <img class="software-logo" src="../img/snparcher-link-logo.png">
    </a>
</div>

[snpArcher](https://github.com/harvardinformatics/snpArcher) is a reproducible workflow optimized for nonmodel organisms and comparisons across datasets, built on the [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html#) workflow management system. It provides a streamlined approach to dataset acquisition, variant calling, quality control, and downstream analysis.

---

##
<div class="software-logo-cont">
    <a href="https://github.com/harvardinformatics/degenotate" target="_blank">
        <img class="software-logo" src="../img/degenotate-link-logo.png">
    </a>
</div>

[degenotate](https://github.com/harvardinformatics/degenotate) degenotate takes as input either a genome FASTA file and a corresponding annotation file (GFF or GTF) OR file or directory of files that contain coding sequences in FASTA format and outputs a bed-like file that contains the degeneracy score (0-, 2-, 3-, or 4-fold) of every coding site.

If given a corresponding VCF file with specified outgroup samples, degenotate can also count synonymous and non-synonymous polymorphisms and fixed differences for use in MK tests (McDonald and Kreitman 1991).

The program also offers coding sequence extraction from the input genome and extraction of sequences by degeneracy (e.g. extract only the 4-fold degenerate sites).