---
title: Frequently asked questions
---

# Frequently Asked Questions


!!! tip "Click on each question to reveal the answer"

## General

??? question "What's the difference between Informatics and Research Computing?"

    ##### What's the difference between Informatics and Research Computing?

    [Research Computing :octicons-link-external-24:](https://www.rc.fas.harvard.edu/){:target="_blank"} manages the Cannon cluster, among other things, and provides advice and support on HPC and related hardware and software questions. The Informatics Group supports specific software and analysis needs, including providing support for core facility software via the Software Operations group, and providing training, consultation, and collaborative project work for bioinformatics needs through the Bioinformatics group. 

    You can contact Research Computing via their [contact page :octicons-link-external-24:](https://www.rc.fas.harvard.edu/about/contact/){:target="_blank"} for any questions related to HPC hardware or software environments. You can contact FAS Informatics for questions related to bioinformatics support via our [contact page](../contact/index.md).

??? question "How can I know about future workshops?"

    ##### How can I know about future workshops?

    We post upcoming workshops on our [Events & Workshops page](../events-workshops/index.md). You can also subscribe to our [newsletter :octicons-link-external-24:](https://mailchi.mp/g/informatics-newsletter){:target="_blank"} to receive updates on upcoming workshops and events.

??? question "Can you run a workshop on X?"

    ##### Can you run a workshop on X?

    We are always looking to run workshops that people are interested in! Please [contact us](../contact/index.md) with your suggestions. We can also run a workshop just for your lab group or department if you have a specific need.

??? question "Can I install command line software on Windows?"

    ##### Can I install command line software on Windows?

    While its true that most command line software for scientific computing is built for Linux (and therefore Mac) operating systems, it's now actually very easy to install and run such software on Windows as well.

    Newer versions of Windows can install the **Windows Subsystem for Linux (WSL)**, which basically installs a Linux file system and shell (bash) within Windows. Installing WSL should be relatively easy (one command in PowerShell). Follow the instructions here: [Microsoft: How to install Linux on Windows with WSL :octicons-link-external-24:](https://learn.microsoft.com/en-us/windows/wsl/install){:target="_blank"}.

    With WSL installed, you can run a Linux shell by finding the WSL app in your list of programs, or by starting the shell from within PowerShell with the command `wsl` or `bash`.

## Bioinformatics

??? question "Do you charge for services?"

    ##### Do you charge for services?

    Training and consultations are provided free-of-charge to the Harvard FAS community. While we do not require funding for short-term collaborations with the Harvard FAS community on a trial basis, extended projects do require a funding arrangment if staff time will be devoted to the collaboration. Please [contact us](../contact/index.md) to discuss your needs.

??? question "How do I arrange a consultation?"

    ##### How do I arrange a consultation?

    Consultations involving sequencing at the Bauer Core should be requested [here :octicons-link-external-24:](https://bauercore.fas.harvard.edu/consultation-request-form){:target="_blank"}. For other projects, please use our [contact form](../contact/index.md)

??? question "What trainings are available?"

    ##### What trainings are available?

    We post trainings on our [Events & Workshops page](../events-workshops/index.md). We are also available to develop specialized trainings for your lab group or department. Please [contact us](../contact/index.md) for more details. 

??? question "How do I join the FAS Bioinformatics Slack?"

    ##### How do I join the FAS Bioinformatics Slack?

    Go to [fas-bioinformaticspub.slack.com :octicons-link-external-24:](https://fas-bioinformaticspub.slack.com){:target="_blank"} and click "Request Invite."

??? question "What's the best way to contact the Bioinformatics team?"

    ##### What's the best way to contact the Bioinformatics team?

    For all questions, you can use the [contact form](../contact/index.md). For possibly quicker answers, you can try our public slack channel (FAS Bioinformatics Public). For hands-on help, come to our office hours in Northwest Labs B227 (see [Events & Workshops](../events-workshops/index.md#office-hours) for times).

??? question "How can I run a Snakemake workflow on the Cannon cluster?"

    ##### Snakemake on the Cannon cluster

    We have developed a [Snakemake plugin for the Cannon cluster :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/cannon.html){:target="_blank"}, based on the [generic SLURM plugin :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/slurm.html){:target="_blank"}. See [the documentation :octicons-link-external-24:](https://snakemake.github.io/snakemake-plugin-catalog/plugins/executor/cannon.html){:target="_blank"} for information on how to install and use it, and feel free to report [issues or questions on the github repo :octicons-link-external-24:](https://github.com/harvardinformatics/snakemake-executor-plugin-cannon){:target="_blank"}.


## Bauer Core Sequencing

??? question "How can I download my sequencing data?"

    ##### How can I download my sequencing data?

    See our tutorial [here](../resources/tutorials/how-can-i-download-my-sequencing-data.md).

---

<!-- --------------------------------- -->
<!-- Page specfic CSS -->

<style>
/* FAQ styles */
    details > h5 {
        display: none;
    }
    article h3 {
        display: none;
    }
    summary {
        font-size: larger;
    }
</style>