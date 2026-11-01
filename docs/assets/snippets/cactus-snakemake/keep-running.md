!!! tip "Be sure you have a way to keep the main Snakemake process running."

    Remember, that some of these steps can take a long time, or your jobs may be stuck in the queue for a while. That means the Snakemake job must have a persistent connection in order to keep running and submitting jobs. There are a few ways this can be accomplished, some better than ~~others~~:

    1. ~~Keep your computer on and connected to the cluster. This may be infeasible and you may still suffer from connection issues.~~

    2. ~~Run the Snakemake job in the background by using `nohup <run command> &`. This will run the command in the background and persist even if you disconnect. However, it makes it difficult to check on the status of your command.~~

    3. Submit the `./cactus_snakemake run` command itself as a SLURM job. This will require [preparing and submitting a job script :octicons-link-external-24:](https://docs.rc.fas.harvard.edu/kb/running-jobs/){:target="_blank"}. This is a good solution.

    4. Use a [terminal multiplexer :octicons-link-external-24:](https://en.wikipedia.org/wiki/Terminal_multiplexer){:target="_blank"} like [GNU Screen :octicons-link-external-24:](https://en.wikipedia.org/wiki/GNU_Screen){:target="_blank"} or [tmux :octicons-link-external-24:](https://en.wikipedia.org/wiki/Tmux){:target="_blank"}. These programs allow you to open a sub-terminal within your currently connected terminal that remains even after you disconnect from the server. This is also a good solution.
