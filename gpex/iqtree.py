"""iqtree interface."""

from gpex.utils import shell


def infer(phylip_path, bootstrap_count, seed):
    shell(
        f"iqtree -m JC -wbt -redo -o outgroup -s {phylip_path} -seed {seed} -bb {bootstrap_count}"
    )
