!!! info "Choosing the Cactus image with `cactus_path`"

    The pipelines run Cactus from a Singularity image, set with `cactus_path`. It can be:

    * `download`: prep downloads the latest Cactus release.
    * A version tag, such as `v3.3.0` or `3.3.0`: prep downloads that version. Always give all three parts of the version. An unquoted `3.3` is read by YAML as a number, and prep fails.
    * The path to a Cactus Singularity image you already have.

    Cactus v3.0.0 or later is required.

    When `cactus_path` is `download` or a version tag, prep downloads the image only once. It's saved as `cactus_vX.Y.Z.sif` in the directory you run prep from, and every later run uses that exact image.

    In the Cactus alignment pipelines (all except Minigraph-Cactus), `use_gpu` decides which build of Cactus is used. With `use_gpu: True`, `download` or a version tag gets the GPU build of that version, saved as `cactus_vX.Y.Z-gpu.sif`. Don't add `-gpu` to the version tag yourself. If you give a file path with `use_gpu: True`, it must point to a GPU image. The Minigraph-Cactus pipeline doesn't use a GPU image.
