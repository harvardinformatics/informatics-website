---
title: Installing command line software with conda/mamba
authors: 
    - Gregg Thomas
---

{{ author_row(page) }}


Many scientific software packages are run by text commands via the **command line**. For installing command line software and managing environments, either on your local computer or on a remote server, we recommend **conda** and **mamba**.

**conda** is a cross-platform package manager, as well as the name of the command-line tool to access conda channels.

**mamba** is a re-implementation of the conda command-line tool and is generally much faster than the conda version.

!!! note "mamba vs. conda"

    We recommend using **mamba** as the command-line tool and will do so through this tutorial, but you can use **conda** if you prefer. Simply replace `mamba` with `conda` in all the commands. Likewise, anywhere in the text we refer to **mamba** you could substitute with **conda**.

## 1. Installing mamba

!!! tip "Check if mamba/conda is already installed"

    If you are on an institutional server or cluster, it is possible they already have mamba (or conda) installed and activated. You can check this by running the command `mamba --version`. If you see the text **mamba X.X.X**, with each X being a number, then mamba is already installed and you can skip to step 2! If you see some form of the error message **Command not found**, then you will have to install mamba.

To install mamba, first navigate to the [Miniforge3 repository page :octicons-link-external-24:](https://github.com/conda-forge/miniforge){:target="_blank"}. Miniforge is a minimal installer for conda and mamba. On this page, scroll down to the **Install** section and follow the instructions for your operating system.

### Mac/Linux

<center>
  <img src="../../img/mamba-install1.png" alt="A screenshot of the miniforge repository's installation instructions" />
</center>

On Mac and Linux machines (the [Harvard cluster runs a version of Linux :octicons-link-external-24:](https://www.rc.fas.harvard.edu/about/cluster-architecture/){:target="_blank"}), you'll want to open your Terminal or login to the server to type the download and install commands.

#### Download the installation script

For downloading, Miniforge provides two example commands using different programs to download the installation script (`curl` and `wget`). **You only need to run one of these commands!** If you get an error along the lines of **Command not found**, try the other command. This should download the installation script to your current folder.

#### Install

Once the script is downloaded, run the second command to execute it. This will start the installation process. You will have to agree to the terms of service by using the spacebar or the down arrow to scroll to the bottom of the text and then hitting enter. You will also be prompted to initialize mamba, which we recommend you do.

After the installation process is complete, restart your terminal or reconnect to the server to activate mamba.

### Windows

For windows, we recommend installing the **Windows Subsystem for Linux (WSL)**. This will install a Linux environment within your Windows machine that can run concurrently with Windows. Importantly, it will install a Linux shell program called **bash** that will allow you to run the commands above.

* **[Install WSL :octicons-link-external-24:](https://learn.microsoft.com/en-us/windows/wsl/install){:target="_blank"}**

If necessary, Miniforge does provide an explicit Windows installer for conda/mamba that you may install instead per the instructions on their page.

## 2. Environments

Once you have followed the above instructions and **restarted your terminal or reconnected to the server**, you should now see that mamba is activated because the `(base)` environment prefix appears before your prompt:

<center>
    <img src="../../img/prompt1.png" alt="A screenshot of a command prompt with (base) prepended to it" />
</center>

mamba can be used to manage environments. **Environments** modify aspects of a user's file system that make it easier to install and run software, essentially giving the user full control over their own software and negating the need to access critical parts of the file system.

When working on a project one may install all the software for that project in a particular environement, or one may have multiple environments for a given project, especially if a single environment becomes too big.

!!! warning "Don't install software in the (base) environment"

    It is important to manage environments cleanly. Because the `(base)` environment contains software related to the functioning of mamba, do not install other software while it is active because the dependencies for those programs may conflict with the base programs. Additionally, larger `(base)` environments will take longer to load on start-up.

### Creating environments

For a given task or project that requires new software to be installed, you will want to create an environment:

```bash
mamba create -n project-env
```

The `-n` option allows you to pick a name for your environment. It can be anything descriptive that you want.

### Activating environments

After creating an environment, you can't immediately install software. You must first **activate** that environment:

```bash
mamba activate project-env
```

!!! note "Activating your first environment with mamba"

    The first time you activate an environment with `mamba` after installing it, you may get a message that `mamba` needs to be initialized. Run the command it suggests and restart your terminal and you should be able to use `mamba` to activate environments going forward.

Here, you use the name specified after `-n` when you created the environment to activate it. In case you end up creating a lot of environments, you can see a list of all of them with the command:

```bash
mamba env list
```

Once you are in an environment, your prompt should be updated to be pre-fixed with that environment's name:

<center>
    <img src="../../img/prompt2.png" alt="A screenshot of a command prompt with (project-env) prepended to it" />
</center>

!!! tip "Environments must be activated every time you log on"

    If you shutdown your terminal or disconnect from the server, upon reconnection you will again be in the `(base)` environment. You will need to use `mamba activate` each time to get back to the desired environment.

### Switching between environments

In order to switch from one environment to another, first deactivate your current environment:

```bash
mamba deactivate
```

Then simply run the `mamba activate` command with the desired environment name to switch to.

!!! warning "Deactivating the (base) environment"

    If you accidentally run `mamba deactivate` while in the `(base)` environment, you will need to re-activate it. The easiest way to do this is to disconnect and then reconnect or restart your terminal.

## 3. Installing software

With mamba installed and within an activted environment, we are almost ready to install software from conda (the package repository).

### Channels

The conda package repository has various **channels** in which software packages can be found. A channel is essentially a sub-repository for similarly themed software. For example, **bioconda** is used for software related to bioinformatics. **conda-forge** is also a popular channel that offers more general software (in fact Miniforge which we used to install conda/mamba is a part of conda-forge).

In the likely event that you'll be using the [bioconda :octicons-link-external-24:](https://bioconda.github.io/){:target="_blank"} channel, they provide additional commands to set-up your conda configuration for ease of use:

```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

This ensures that when you install a package, both the conda-forge and bioconda channels are searched for a package matching that name.

### Searching for packages

While it is certainly possible to type "[software name] conda package" into your favorite search engine and get results, it may be better to directly search the websites of each channel:

* [bioconda :octicons-link-external-24:](https://bioconda.github.io/){:target="_blank"}
* [conda-forge :octicons-link-external-24:](https://conda-forge.org/packages/){:target="_blank"}
* [Anaconda :octicons-link-external-24:](https://anaconda.org/){:target="_blank"}

Anaconda will search all conda channels so it may be the most direct way to search, but be wary of false positives (anyone can create a channel). Additionally, each page should give a short summary of the software and relevant links and, importantly, installation commands for software packages.

### Installation commands

After you've searched the links above for your software of interest, you should be able to copy and paste the command into your terminal, *e.g.* if you're interested in the software [GRAMPA :octicons-link-external-24:](https://bioconda.github.io/recipes/grampa/README.html#package-package%20&#x27;grampa&#x27;){:target="_blank"}:

```bash
mamba install grampa
```

In some cases, you may want to explicitly specify the name of the channel from which you want to install the software. This can be done in two ways:

```bash
mamba install -c bioconda grampa
```

or

```bash
mamba install bioconda::grampa
```

Then, you should be able to run the software! Usually, the package name and the software name are the same (*i.e.* to run the grampa package you should be able to type `grampa` in the terminal), though this may not be true for every package out there. Hopefully the package is documented well and explains how to run it after installing...

!!! success "Dependencies"

    A **dependency** is a piece of software or code that is used by another program. Traditionally, ensuring one had all the dependencies to run a given program was a big challenge when installing software. Conda negates this by automatically installing dependencies for any package you install! This is why you may see a long list of software when you run `mamba install`.

## 4. Exporting and re-creating environments

### Exporting an environment to a file

It may sometimes be necessary to share your environment in its current state with others, or to back up the environment at a certain point in a project.  This can be done by **exporting your environment to a file**. This means that the packages currently installed and the versions that are being used are recorded in a text file that can be used later to create an identical environment. This ensures reproducible code and results.

To export a conda environment, make sure the desired environment is activated and run:

```bash
mamba env export > environment.yml
```

The `>` operator redirects the output to the file `environment.yml`. You could name this file whatever you want, but it should be something descriptive so you remember what it is -- maybe it would be a good idea to use the same name as the environment you just exported along with the date!

??? example "An example conda environment yml file"

    `.yml` or `.yaml` stands for "[YAML ain't markup language :octicons-link-external-24:](https://en.wikipedia.org/wiki/YAML){:target="_blank"}" files, and is a basic nested text format that is easily parseable. In the context of conda, it may look something like this:

    ```
    name: example_env
    channels:
    - defaults
    - conda-forge
    dependencies:
    - python=3.8
    - numpy=1.21
    - pandas=1.3
    - scipy=1.7
    - matplotlib=3.4
    - pip:
        - some-package==0.1.0
    ```

    This outlines the name of the environment, the channels in which to look for the specified packages, as well as the packages to install (here listed as "dependencies"). Note also that another package is installed instead with the `pip` package manager for Python.

### Creating an environment from a file

If you ever want to re-create an environment you exported previously to a file or that has been shared with you, run the command:

```bash
mamba env create -f environment.yml -n env-recreated
```

Here, we use `mamba env create` instead of just `mamba create` since we are loading an environment from a file. We then specify the file that contains the exported environment with `-f` and we can name our environment something descriptive with `-n`.

This should create and automatically install all the software that was in the exported environment. Depending on the size of the environment, this may take some time. Don't forget to `mamba activate` your new environment to use the software installed within it!

## Troubleshooting

??? question "1. What if I encounter an error like `mamba: command not found`?"

    ##### 1. `mamba: command not found`

    If you see the `mamba: command not found` error when trying to install software or run any of the above commands, it likely means one of two things:

    1. mamba isn't yet installed on the computer you're using. Follow the instructions in [1. Installing mamba](#1-installing-mamba)
    2. mamba hasn't been initialized. If you didn't indicate Yes to the final prompt when installing Miniforge, your shell hasn't been setup yet. You may need to run `mamba init` and restart your shell. If you try to run `mamba init` and get the same error, you'll have to provide the full path to the mamba executable, which should be something like: `/where/you/installed/miniforge3/bin/mamba`.

??? question "2. What if mamba cannot solve the environment or is taking a very long time to install a package?"

    ##### 2. mamba cannot solve the environment or is taking a long time to install a package

    If `mamba install` fails or hangs for a long time, the program might be struggling with installing dependencies given the current settings. This can happen if your dependency graph is too large because you have too many packages installed in one environment. **The easiest solution to this problem is to try to install your package in a fresh environment.** If that still doesn't work, or you need to install it in the current environment, try to update mamba and conda:

    Make sure mamba and conda are up to date. First, ensure that you are in the **(base)** environment by running the command:

    ```bash
    mamba activate base
    ```

    Then, to update mamba, run the command:

    ```bash
    mamba update mamba
    ```

    In this case you may also want to update conda (recall that mamba is installed on top of conda, so conda is still there in the background):

    ```bash
    conda update -n base -c defaults conda
    ```

    Also, if you're using bioconda, make sure your [channels are set up to give bioconda priority](#channels).

??? question "3. What if, after I install the package, I try to run it and see `[package name]: command not found`?"

    ##### 3. `[package name]: command not found`

    If you see a `command not found` error for a package you successfully ran `mamba install` on previously, it likely means you aren't in the same environment as where you installed the package. Make sure you [activate the correct environment](#activating-environments).

    Otherwise, read the package's documentation on how to call the program. In most cases it will be the same as the package name, but for some reason others choose to name their package something different than their executable.

??? question "4. What can I do if the package I want to install isn't available through conda? :("

    ##### 4. The package I want to install isn't available through conda

    First, search for your package on other software repositories. For Python packages (though most of these should be on conda), there is the [PyPI repository :octicons-link-external-24:](https://pypi.org/){:target="_blank"} which uses the [pip :octicons-link-external-24:](https://pypi.org/project/pip/){:target="_blank"} command line tool to install packages. pip should be installed with Python. For R packages, [CRAN :octicons-link-external-24:](https://cran.r-project.org/){:target="_blank"} is the repository, and these packages can be installed within R with the `install.packages()` command. Depending on your OS or what programming language you want to install software from, there is likely a repository to search and associated command line tool. For example, MacOS has [Homebrew :octicons-link-external-24:](https://brew.sh/){:target="_blank"}, run with the `brew` command, and JavaScript packages can be found in the [npm registry :octicons-link-external-24:](https://www.npmjs.com/){:target="_blank"}. There are many other repositories out there, and the program you're interested in should have documentation telling you where it can be found.

    If you've searched repositories for your OS or programming language of interest and haven't found the program you want available on any of them, you may be stuck **building from source**. This can be as simple as downloading a script from github with no dependencies. But this can also be a very difficult task: it means you are also responsible for installing any dependencies and specifying paths to libraries that the program uses, which, on shared compute systems (like institutional clusters) where one doesn't have full access to all folders, can be unmanageable. Hopefully the authors of the program have left very good documentation about how to handle these things...

---

<!-- --------------------------------- -->
<!-- Page specfic CSS -->

<style>
    h2 {
        text-align: center !important;
        border-bottom: 2px solid #333333 !important;
        border-top: 2px solid #333333 !important;
        font-weight: 500 !important;
    }
    
    details > h5 {
        font-size: 0.01em !important;       /* almost invisible but still present! */
        color: transparent !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    /* Hide all 2nd-level navs */
    .md-nav--secondary .md-nav__item .md-nav {
        display: none !important;
    }

    /* Show when parent has .expanded class */
    .md-nav--secondary .md-nav__item.expanded > .md-nav {
        display: block !important;
    }    
</style>