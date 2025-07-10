---
title: "[Tutorial] Download sequence data from Bauer Core"
description: "A walkthrough describing the various ways to download raw sequence data from Harvard's Bauer Sequencing Core"
authors: 
    - Nathan Weeks
---

# How to download sequencing data from the Bauer Core

{{ author_row(page) }}

List of recommended software tools for downloading sequencing data from the Bauer Core.

## Supported Protocols

Several protocols are available for downloading a sequencing run directory.
The following table contains a partial listing of software tools for each protocol.

speed | protocol | software tools | FAS RC account required
---|---|---|---
fastest | local file copy | __fpsync*__, rsync, cp | yes
| Globus | __Globus web app*__ | no
| SCP/SFTP   | __FileZilla*__, rsync, scp | yes
 slowest | HTTPS      | __rclone*__, wget | no

__*__ _recommended_

_Excluding BCL files_

The `Data/` subdirectory contains the raw BCL files from the sequencer.
These can take almost as much disk space as the demultiplexed FASTQ files, increasing transfer times and local storage requirements.
Each transfer mechanism downloads the entire sequencing run directory by default, but can be adapted to exclude the `Data/` subdirectory if desired.

## Verifying downloaded .fastq.gz files

Occasionally, large files become corrupted during download, causing errors during decompression or when using the .fastq.gz files directly in a workflow.
You can determine whether this has occurred by comparing the [checksum :octicons-link-external-24:](https://en.wikipedia.org/wiki/Checksum){:target="_blank"} of a file before and after download.
!!! note

    Globus automatically verifies file checksums after transfer by default, unless explicitly disabled before transfer (by checking the "do NOT verify file integrity after transfer" in the Globus web interface Transfer settings).

We have placed checksums for your fastq.gz files in your run directory in a file called md5sum.txt.
Compare the values in this file to new checksums calculated on your downloaded files.

To calculate a checksum for a file called myfile.fastq.gz (on Linux or WSL), use the [md5sum :octicons-link-external-24:](https://en.wikipedia.org/wiki/Md5sum){:target="_blank"} utility:

    md5sum myfile.fastq.gz
    
On macOS, use the `md5` utility:

    md5 myfile.fastq.gz

If the checksum for a file differs from the value in the md5sum.txt, then the file is corrupt or incomplete and should be downloaded again.

To calculate and compare the checksums of all FASTQ files listed in md5sum.txt (using `md5sum` on Linux/WSL):

    md5sum -c md5sum.txt

## Local file copy

Users with a [FAS RC account :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/){:target="_blank"} who intend to copy the sequencing run directory (`/n/ngsdata/<run_name>`) to another file system on the FAS RC cluster may [connect to the cluster via ssh :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/terminal-access/){:target="_blank"} and perform a local file copy using one of several software tools.

### rsync

_**What**_

[rsync :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/rsync/){:target="_blank"} is a command-line utility for copying/synchronizing a source directory with a destination.
Unlike `cp` or `scp`, `rsync` can be efficiently resumed if transfer is interrupted.

`rsync` is installed by default on macOS.


_**Who**_

All users with a [FAS RC account :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/){:target="_blank"} who either:

* Intend to copy the sequencing run directory from `/n/ngsdata/<run_dir>` to another FAS RC Cluster file system directory, _or_
* Download to a local server / workstation, _and_ prefer a command-line utility

_**How**_

If you logeged into the FAS RC cluster via SSH, to copy files to another directory mounted on the FAS RC cluster:

    rsync -av /n/ngsdata/<run_name> /path/to/my/directory

*Note: adding a trailing slash to `<run_name>/` will cause only the contents of `<run_name>` to be copied, excluding the `<run_name>` directory itself.*

_Excluding BCL files_

Add the `--exclude=Data` option:
    
    rsync --exclude=Data -av /n/ngsdata/<run_name> /path/to/my/directory

### fpsync

[fpsync :octicons-link-external-24:](https://www.fpart.org/fpsync/){:target="_blank"} can be used to parallelize rsync transfers (see FAS RC [Transferring Data on the Cluster :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/transferring-data-on-the-cluster/){:target="_blank"} guide).
By default, fpsync uses 2 (rsync) workers to copy the directory.
The `-n <number_of_workers>` option can be used to increase the number of concurrent rsync transfers:

    fpsync -v -n 4 /n/ngsdata/<run_name> /path/to/my/directory/<run_name>

*Note: `fpsync` copies the **contents** of `<run_name>` to the destination path; specify `<run_name>` at the end of the destination path to copy the contents into a directory called `<run_name>`.*

---

## Globus

_**What**_

[Globus :octicons-link-external-24:](https://www.globus.org/data-transfer){:target="_blank"} provides a user-friendly web interface and the fastest and most-reliable mechanism for transfer sequencing data files off the FAS RC cluster.

There is also a [Globus Command Line Interface :octicons-link-external-24:](https://docs.globus.org/cli/){:target="_blank"} (not discussed here).

_**Who**_

All users with:

1. A Harvard Key or other supported [organizational login :octicons-link-external-24:](https://app.globus.org/){:target="_blank"}; or a Google account, ORCID iD, or [Globus ID :octicons-link-external-24:](https://www.globusid.org/what){:target="_blank"}; 

    _and_

2. A destination Globus [endpoint :octicons-link-external-24:](https://docs.globus.org/faq/globus-connect-endpoints/#what_is_an_endpoint){:target="_blank"}; either:
    - A workstation or standalone server with [Globus Connect Personal :octicons-link-external-24:](https://www.globus.org/globus-connect-personal/){:target="_blank"} installed (available for Windows, macOS, and Linux), 
    
    _or_
    
    - A data transfer node (maintained by your organization's system administrators) with Globus Connect Server
        - _FAS RC Cluster users_: See FAS RC [Globus File Transfer :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/globus-file-transfer/){:target="_blank"} guide; note [destination path restrictions apply for FAS RC Holyoke and Boston endpoints :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/globus-file-transfer/#Using_the_Harvard_FAS_RC_Holyoke_or_Boston_Endpoints){:target="_blank"}.

_**How**_

1. In the demultiplex summary email, click on direct link to the run directory in the Globus web app.
   You will be prompted to authenticate using your chosen identity provider (Harvard users: select "Harvard University" in the "Look up your organization..." dropdown menu)
    - Alternatively, you may first log in to the [Globus web app :octicons-link-external-24:](https://app.globus.org){:target="_blank"}, then search for the "Harvard Bauer Core Sequencing Results" Collection, and finally double-click on the run folder that was listed in the demultiplex summary email.
2. In the other Collection box, search for your destination endpoint (which may be a Globus Connect Personal endpoint created during installation to a local workstatio/server).
   Choose or create an appropriate destination folder.
3. Select all files/folders to transfer (a checkbox in the top-left corner of the file selector can be used to select all), and select "Start" to begin the transfer.

_Excluding BCL files_

Uncheck the box next to the `Data` subdirectory before clicking the "Start" button to initiate the transfer.

---
## SSH

Users with a FAS RC account who intend to intend to transfer data off the FAS RC cluster can use one of several software tools that use the SSH protocol.

### FileZilla

_**What**_

[FileZilla :octicons-link-external-24:](https://filezilla-project.org/){:target="_blank"} is a graphical SFTP/FTPS utility.

_**Who**_

All users with a [FAS RC account :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/){:target="_blank"} who intend to download to a local workstation.

_**How**_

1. Follow the [FAS RC SFTP file transfer using Filezilla :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/sftp-file-transfer/){:target="_blank"} to install/configure FileZilla.
2. Specify `/n/ngsdata/<run_dir>` for the "Remote site"
3. Select all files/directories; drag & drop to an appropriate "Local Site" directory

_Excluding BCL files_

Unselect the `Data` subdirectory in the remote site window before dragging & dropping the selected files/folders to the local site window.


### rsync

In addition to local copies, `rsync` can also be used to push/pull data from the FAS RC cluster to a local file system or remote server that has SSH enabled.

__If you are logged into a local workstation / server, to pull data via rsync over ssh__

    rsync -av <fasrc_username>@login.rc.fas.harvard.edu:/n/ngsdata/<run_name> /path/to/my/directory

__If you are logged into the FAS RC cluster, to push data via rsync over ssh to a remote server that you have an account on__

    rsync -av /n/ngsdata/<run_name> <remote_username>@<remote_host>:/path/to/my/remote/directory

### scp

_**What**_

* The `scp` and `sftp` command-line utilities are installed by default on [Windows :octicons-link-external-24:](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_overview){:target="_blank"}, macOS, and most Linux distributions.

_**Who**_

* All users with a [FAS RC account :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/how-do-i-get-a-research-computing-account/){:target="_blank"} who intend to download to a local workstation or another server.

_**How**_

[scp or sftp :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/copying-data-to-and-from-cluster-using-scp/){:target="_blank"} can be used to a run directory to a local computer; e.g., the following `scp` command invoked from your local computer:

    scp -rp <fasrc_username>@login.rc.fas.harvard.edu:/n/ngsdata/<run_name> /path/to/my/local/directory

From an SSH session on the FAS RC cluster, to a copy files to a remote server that you have SSH access to:

    scp -rp /n/ngsdata/<run_name> <user_name>@<remote_hostname>:/path/to/my/remote/directory


In all cases, replace &lt;run_name&gt; above with the name of the your sequencing run (e.g., 140523_D02345_1234_AH132DADXX), and &lt;user_name&gt; with your RC user name.

_Excluding BCL files_

scp does not provide an option to exclude directories.


---
## HTTPS

If you do not have login access to the FAS RC cluster, sequencing data can be downloaded via HTTPS from https://data.rc.fas.harvard.edu/ngsdata/ with one of several softare tools, including:

### rclone

__**What**__

[rclone :octicons-link-external-24:](https://rclone.org/){:target="_blank"} is an open-source command-line utility that can be used to transfer files over a number of storage protocols, including [HTTP directory listings :octicons-link-external-24:](https://rclone.org/http/){:target="_blank"}.
While much slower than Globus, rclone is more-performant than `wget` for transferring data from https://data.rc.fas.harvard.edu/ngsdata/ due to its ability to transfer multiple files concurrently.

__**Who**__

* Users who do not have login access to the FAS RC cluster, and would prefer to pull sequencing data from a web server via HTTPS; _or_
* Users who have a FAS RC account, who would like to push data from the FAS RC cluster to cloud storage (see [rclone – transfer files to/from cloud storage :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/rclone/){:target="_blank"} for an example of how to configure rclone to push data to Google Drive).

__**How**__

To download https://data.rc.fas.harvard.edu/ngsdata/`<run_name>`

    rclone copy --progress --http-url https://data.rc.fas.harvard.edu/ngsdata/ :http:<run_name> <destpath>

e.g., to transfer the contents of 211007_A00794_0504_AHLMC5DSX2 locally to into a directory of the same name (creating if it doesn't already exist)

    rclone copy --progress --http-url https://data.rc.fas.harvard.edu/ngsdata/ :http:211007_A00794_0504_AHLMC5DSX2 211007_A00794_0504_AHLMC5DSX2

_Excluding BCL files_

Add the `--exclude='Data/**'` option:

    rclone copy --exclude='Data/**' --progress --http-url https://data.rc.fas.harvard.edu/ngsdata/ :http:<run_name> <destpath>

### wget

_**What**_

If downloading to your local computer, [wget :octicons-link-external-24:](https://www.gnu.org/software/wget/){:target="_blank"} (installed by default on some Linux distributions, and available for Windows using [WSL :octicons-link-external-24:](https://learn.microsoft.com/en-us/windows/wsl/){:target="_blank"}, as well as macOS through package managers such as [conda :octicons-link-external-24:](https://anaconda.org/conda-forge/wget){:target="_blank"} and [brew :octicons-link-external-24:](https://formulae.brew.sh/formula/wget){:target="_blank"}) can be used to transfer files over HTTPS:

_**Who**_

Users without a FAS RC account, _and_ who prefer to not use rclone (faster) or Globus (fastest).

_**How**_

    wget -r -nH --cut-dirs=1 --no-parent -e robots=off  --no-check-certificate --reject="index.htm*" https://data.rc.fas.harvard.edu/ngsdata/<run_name>/

*NOTE: the trailing slash (`<run_name>/`) is necessary to download only `<run_name>` and not the entire contents of `/ngsdata/*`*

We use InCommon certificates that may or may not be part of the trusted authorities on your local machine, so --no-check-certificate may be necessary.

_Excluding BCL files_

Add the `--exclude-directories=Data` option to the `wget` command.

---