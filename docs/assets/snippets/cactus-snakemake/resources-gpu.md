!!! warning "Using GPUs"

    Only the blast rules request GPUs, and only when `use_gpu: True` is set. With `use_gpu: True`, the other rules also run from the GPU image, but they don't request GPUs.

    * **Allocate the proper partition based on `use_gpu`.** If `use_gpu: True`, the `partition` in the `blast` entry of `rule_resources` must be one with GPUs. If not, the pipeline will fail to run.
    * Set **exactly one** of `gpus` or `gres` in the `blast` entry:
        * `gpus`: the number of GPUs to request, through Snakemake's `gpu` resource.
        * `gres`: a SLURM GRES request in any of these forms: `1`, `a100:2`, `gpu:1`, or `gpu:a100:2`. If the `gpu:` prefix is left off, the pipeline adds it before submitting the request.
    * If `use_gpu: False`, both `gpus` and `gres` are ignored.
